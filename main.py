import asyncio
import json
import logging
import os
import subprocess
import quart
import quart_cors
from quart import request

# Document retrieval langchain imports
from langchain.document_loaders import (PyPDFLoader, Docx2txtLoader,
                                        TextLoader, CSVLoader,
                                        UnstructuredHTMLLoader)
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter

# Set up nltk and download required resources
import nltk
nltk.download('averaged_perceptron_tagger')


database_metadata = {}  # This will store the mapping of user-friendly names to DB paths

# Setup OS-specific configurations
if os.name == 'nt':
  asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load configuration from JSON
with open('settings.json', 'r') as config_file:
  config = json.load(config_file)

# Assign configuration settings to constants
OPENAI_API_KEY = config.get("OPENAI_API_KEY", '')
METADATA_FILE_PATH = config.get(
    "METADATA_FILE_PATH", 'database_metadata.json')
SETTINGS_FILE_PATH = config.get("SETTINGS_FILE_PATH", 'settings.json')
LOG_LEVEL = config.get("LOG_LEVEL", 'INFO')
HOST = config.get("HOST", '0.0.0.0')
PORT = config.get("PORT", 5004)

# Set the OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Determine the current working directory based on the platform
cwd = config.get("working_directory_unix", ".")
if os.name == 'nt':
  cwd = os.path.expandvars(config.get("working_directory_windows", "."))

# Set up quart app
app = quart_cors.cors(quart.Quart(__name__),
                      allow_origin="https://chat.openai.com")


# Function to save metadata to a file
def save_metadata():
  """Save metadata to the metadata file."""
  with open(METADATA_FILE_PATH, 'w') as file:
    json.dump(database_metadata, file, indent=4)

# Function to load metadata from a file
def load_metadata():
  """Load metadata from the metadata file."""
  global database_metadata
  try:
    with open(METADATA_FILE_PATH, 'r') as file:
      database_metadata = json.load(file)
  except (FileNotFoundError, json.JSONDecodeError):
    # If the file doesn't exist or is empty, initialize the dictionary as empty
    database_metadata = {}


# Function to load documents from a given directory
def load_documents_from_directory(directory_path: str) -> list:
  """
    Load documents from the specified directory.

    Parameters:
    - directory_path (str): Path to the directory containing documents.

    Returns:
    - list: A list of loaded documents.
    """
  loaded_documents = []

  #logging.info(f"\n\n ### Received path {directory_path} ### \n\n")
  for dirpath, dirnames, filenames in os.walk(directory_path):
    for file in filenames:
      file_path = os.path.join(dirpath, file)
      try:
        loader = None
        if file.endswith(".pdf"):
          loader = PyPDFLoader(file_path)
        elif file.endswith('.docx') or file.endswith('.doc'):
          loader = Docx2txtLoader(file_path)
        elif file.endswith('.txt'):
          loader = TextLoader(file_path)
        elif file.endswith('.csv'):
          loader = CSVLoader(file_path)
        elif file.endswith('.html'):
          loader = UnstructuredHTMLLoader(file_path)
        if loader:
          loaded_documents.extend(loader.load())
          #logging.info(f"\n\n ## Successfully loaded {file}: {file_path}")
      except Exception as e:
        logging.error(f"Error loading file {file_path}: {str(e)}")

  return loaded_documents


# Define endpoints


@app.get("/logo.png")
async def plugin_logo():
  """Serve the plugin logo."""
  filename = "logo.png"
  return await quart.send_file(filename, mimetype="image/png")


@app.post("/command")
async def command():
  """
    Execute a shell command and return the output.
    """
  data = await request.get_json()
  command = data.get("command")
  if not command:
    return quart.Response(response="No command provided", status=400)
  logging.info(f"Received command: {command}")

  # Determine the shell to use based on the operating system
  if os.name == 'nt':  # Windows
    try:
      result = subprocess.check_output(["cmd.exe", "/c", command],
                                       stderr=subprocess.STDOUT,
                                       text=True)
      return quart.Response(response=result, status=200)
    except subprocess.CalledProcessError as e:
      logging.error(f"Command error: {e.output}")
      return quart.Response(response=e.output, status=500)
  else:  # UNIX-like systems
    shell = True
    executable = None
    logging.error(f"Running linux command ##")
    # Use asyncio to execute the command
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=os.getcwd(),
        shell=shell,
        executable=executable)

    stdout, stderr = await process.communicate()

    # Check for errors
    if process.returncode != 0:
      logging.error(f"Command error: {stderr.decode('utf-8')}")
      return quart.Response(response=stderr.decode("utf-8"), status=500)
    else:
      return quart.Response(response=stdout.decode("utf-8"), status=200)


# Endpoint to load data into the database
@app.post("/load-data")
async def load_data():
  """
    Load documents from the provided folder path and create a vector database for them.
    """
  global database_metadata
  data = await request.get_json()
  folder_path = data.get('folder_path')
  dataset_name = data.get('dataset_name')

  if not folder_path or not dataset_name:
    return quart.Response(
        response="folder_path and dataset_name are required.", status=400)


      # Check if the folder_path exists
  if not os.path.isdir(folder_path):
    return quart.Response(
      response=f"The provided folder path {folder_path} does not exist.", status=400)

  #logging.info(
   #   f"\n\n ## $$ Received request to load data from {folder_path} with dataset name {dataset_name}\n"
  #)

  # Load documents
  try:
    logging.info(f"\n\n### Loading documents from the Directory {folder_path} \n\n ###")
    documents = load_documents_from_directory(folder_path)
  except Exception as e:
    logging.error(f"Error loading documents: {str(e)}")
    return quart.Response(response=f"Error loading documents: {str(e)}",
                          status=500)

  # Split documents into chunks
  text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
  documents = text_splitter.split_documents(documents)

  # Create and persist vector database
  try:
    db_path = os.path.join("databases", dataset_name)
    vectordb = Chroma.from_documents(
        documents,
        embedding=OpenAIEmbeddings(disallowed_special=()),
        persist_directory=db_path)
    vectordb.persist()

    # Store the database path in our metadata dictionary
    database_metadata[dataset_name] = db_path

    # Store the database path and the actual file path in our metadata dictionary
    database_metadata[dataset_name] = {
        "db_path": db_path,
        "folder_path": folder_path
    }

    save_metadata()
    #logging.info(f"\n\n ### Storing the db_path {db_path} ### \n\n")
  except Exception as e:
    logging.error(f"Error creating vector database: {str(e)}")
    return quart.Response(response=f"Error creating vector database: {str(e)}",
                          status=500)

  return quart.Response(
      response=f"Database for {dataset_name} created successfully!",
      status=200)



# Endpoint to query the database
@app.post("/query-data")
async def query_data():
  """
    Query the database using a given query string and dataset name.
  """
  global database_metadata  # Declare the global variable to use it inside the function
  data = await request.get_json()

  # Validate the input data
  query = data.get('query')
  dataset_name = data.get('dataset_name')

  if not query or not dataset_name:
    logging.warning("Both 'query' and 'dataset_name' are required.")
    return quart.Response(
        response="Both 'query' and 'dataset_name' are required.", status=400)

  #Get dataset info from database_metadata
  dataset_info = database_metadata.get(dataset_name, {})

  if not dataset_info:
    logging.warning(f"No database found for {dataset_name}")
    return quart.Response(response=f"No database found for {dataset_name}",
                          status=404)

  # Extract db_path from dataset_info
  db_path = dataset_info.get('db_path', None)
  if not db_path:
    logging.warning(f"No db_path found for {dataset_name}")
    return quart.Response(response=f"No db_path found for {dataset_name}",
                          status=404)

  #logging.info(f"\n\n ### Query recieved data base path: {db_path}")

  try:
    # Load the specific database
    embedding = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=db_path, embedding_function=embedding)

    # Query the database
    results = vectordb.similarity_search(query, k=5)

    #Format and return the results
    formatted_output = f"Based on your query '{query}', the following relevant sections from {dataset_name} we've identified the following relevant sections from our documents. Please review them to gather the necessary information from all segments and summarize all to one before submitting it to user\n"
    for idx, doc in enumerate(results, 1):
      formatted_output += f"\n---\nSegment {idx}:\n{doc}\n---\n"

    return quart.Response(response=formatted_output, status=200)

  except Exception as e:
    logging.error(f"Error querying the database for {dataset_name}: {str(e)}")
    return quart.Response(
        response=f"An error occurred while querying the database.", status=500)


# Endpoint to get database information
@app.post("/get-db-info")
async def get_db_info():
  
    '''Get database information based on the dataset name and query type.'''

    global database_metadata  # Declare the global variable to use it inside the function
    data = await request.get_json()

    dataset_name = data.get('dataset_name')
    query_type = data.get('query_type')  # Can be 'db_path' or 'folder_path'

    if not dataset_name or not query_type:
        logging.warning("Both 'dataset_name' and 'query_type' are required.")
        return quart.Response(
            response="Both 'dataset_name' and 'query_type' are required.",
            status=400
        )

    dataset_info = database_metadata.get(dataset_name, {})

    if not dataset_info:
        logging.warning(f"No database found for {dataset_name}")
        return quart.Response(
            response=f"No database found for {dataset_name}",
            status=404
        )

    result = dataset_info.get(query_type, None)

    if not result:
        logging.warning(f"No {query_type} found for {dataset_name}")
        return quart.Response(
            response=f"No {query_type} found for {dataset_name}",
            status=404
        )

    return quart.Response(
        response=json.dumps({query_type: result}),
        status=200,
        mimetype='application/json'
    )



@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
  """
    Serve the plugin manifest.

    This function reads the ai-plugin.json file and returns it to the client.
    """
  with open("./.well-known/ai-plugin.json") as f:
    text = f.read()
    return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
  """
    Serve the OpenAPI specification.

    This function reads the openapi.yaml file and returns it to the client.
    """
  with open("openapi.yaml") as f:
    text = f.read()
    return quart.Response(text, mimetype="text/yaml")


# Run the Quart app
if __name__ == "__main__":
  load_metadata()
  logging.info(f"{database_metadata}")
  app.run(debug=True, host=HOST, port=PORT)
