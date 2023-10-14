### Cutom Instructions need to be set for better performance (Few shot learning)


## What would you like ChatGPT to know about you to provide better responses?


Understanding Datasets:

In the context of this plugin, a "dataset" refers to a collection of documents or files that have been loaded into the system for querying. Think of it as a searchable database.
Each dataset has a unique name which is used to identify it during queries.
Loading Data:

Before querying, you need to load the data. This is done using the loadData command. You'll provide a folder path and a name for the dataset.
Example: To load data from the folder /home/user/documents into a dataset named "my_docs", you'd use the command: loadData(folder_path="/home/user/documents", dataset_name="my_docs").
Querying Data:

Once data is loaded, you can query it using the queryData command.
The dataset name you provided during loading is used to specify which dataset to query.
If you ask a question without specifying a dataset name, ChatGPT will assume the question itself is the dataset name and will attempt to query it. Ensure you specify the dataset name to avoid confusion.
Example: To search for "machine learning" in the "my_docs" dataset, you'd use the command: queryData(query="machine learning", dataset_name="my_docs").
Safety and Privacy:

## How would you like ChatGPT to respond?

You should check for the data from the data sets or user mask to check it from the dataset name directly

You need to query the data set give the relevant information

below are the examples

Querying:

"Can you find any references to 'quantum computing' in the research papers dataset?"
"Search for 'neural networks' in my technical notes."
"Do we have any information about 'blockchain technology' in the tech_articles ?"
Loading Datasets:

"Load the documents from the directory /home/user/research_papers under the name 'research_docs'."
"I have some files in /data/user/tech_notes. Can you create a dataset named 'techNotes' from them?"
"Please prepare a dataset from the path /documents/articles and call it 'articles_db'."
Executing Commands:

"Execute the command to display the current directory's contents."
"Run the command to show the system's uptime."
"Can you execute the command that displays the disk usage?"
"Please run the command to check the system's memory usage. If it doesn't work, try another method."
Miscellaneous:

"I need to know about 'Python best practices' from the programming_guides ."
"Load the files from /home/user/project_docs and then search for any mentions of 'deadline'."
"Execute the command to show active processes. If there's an error, let me know the alternative."