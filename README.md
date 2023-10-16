# 🚀 OSGPT: File Content Discovery & Dynamic Folder Access and Enhanced Chat for Command Line" (ChatGPT 4 Plugin)
#### checked 14.10.2023 (works well)


OSGPT is a powerful plugin designed to dynamically load documents from specified folders and create searchable vector databases. Not only does it offer a quick way to query from your documents, but it also allows you to execute CLI commands on the host system, be it Linux/Unix or Windows.

⚠️ Please note that this is a plugin for ChatGPT Plus! In order to use it, you'll need access to ChatGPT Plus Account. As with all powerful tools, remember to use this responsibly and always be mindful of the potential security and privacy implications.

See [OSGPT in ChatGPT Plus with GPT4](img/shellmaster0.png)


## 🎥 Demo Video

[![Demo Video](https://img.youtube.com/vi/Xy6vNqoW2wk/hqdefault.jpg)](https://www.youtube.com/watch?v=Xy6vNqoW2wk)


## Features

### Chat Your Way Through File Management
Imagine having a conversation with your operating system, where you can effortlessly search and manage your info from your files just by chatting. With OSGPT, you can do exactly that. It transforms file management into a dynamic, interactive experience. No more shifting through multiple directories or using complex search queries; OSGPT's advanced search capabilities simplify the often cumbersome task of finding info from documents across multiple directories. Plus, its auto-loading feature automatically loads documents from specified directories into a searchable vector database, making your files instantly accessible.

### CLI Capabilities
Full Control: Execute any CLI command directly from the chat interface.
Multiple commands: Handle multiple commands simultaneously with asynchronous execution.
Configuration support: Configure the working directory for command execution for flexibility and security.

### Unleashing the power of Interactive Computing
With OSGPT, you get the best of both worlds—a chatbot that understands your tasks and a powerful CLI engine that performs them. Say goodbye to the days of juggling multiple windows and hello to the interactive computing.

## Useful custom instructions
- [Custom Instructions for better working of plugin](https://github.com/Ravi-Teja-konda/OSGPT/blob/main/prompts/Custom_Instructions.md)

  
## Installation
1. Clone the repository:
 ```bash
 git clone https://github.com/Ravi-Teja-konda/OSGPT.git
```
2. Navigate to the project directory:
```bash
cd OSGPT
```
3.Install the required Python libraries:
```bash
pip install -r requirements.txt
```

## Configuration Settings in settings.json

### Working Directory for Commands
working_directory_unix: This is the working directory where commands will be executed when running OSGPT on a Unix/Linux system. The default directory is /tmp, which is recommended for its safety and security.

working_directory_windows: Similar to the Unix setting, this is the directory where commands will be executed when running OSGPT on a Windows system. The default is %TEMP%.

Note: Ensure that the directory you choose has a minimum chmod of 700 for Unix/Linux and appropriate permissions for Windows to maintain security.

### OpenAI API Key
OPENAI_API_KEY: This is the API key for OpenAI, which is essential for utilizing the GPT models. Replace the placeholder with your actual API key.

### Metadata File Path
METADATA_FILE_PATH: This is where the metadata for the indexed database will be stored.

### Host and Port
HOST: This is the host IP address where the OSGPT server will run. The default is 0.0.0.0, which means it will be accessible from any IP address.
PORT: This is the port number on which the OSGPT server will listen for incoming requests. The default port is 5004.

## Additional Info
If there is a change in the host address, make sure to update the following files:

1. ai-plugin.json
Update the url field under the api key with the new OpenAPI URL.
Update the logo_url field with the new logo URL if applicable.
2. openapi.yaml
Update the url field under servers with the new host address.

## Usage
To get started, run the plugin using the following command:

```python
python3 main.py
```
Next, navigate to your ChatGPT Plus Account. Under Settings, enable the Developer Tools ([see image for reference](img/settings.png)). Switch to the GPT-4 tab and then proceed to the Plugin Store. At the bottom of the Plugin Store page, you'll find a link titled "Develop your own plugin" ([see image](img/pluginshop.png)). Click on this link and enter your information as required.

In my example, I used localhost:5004. You can use another port such as 2323 or 8080, but please ensure that your firewall or security software isn't blocking the connection ([see image](img/load.png)).

To use this plugin, you'll need to send a POST request to the /command endpoint of the server. The request should contain a JSON body with a command field, representing the command you wish to execute.

### Command execution

Example:
```json
{
  "command": "echo 'Hello, World!'"
}
```
Alternatively, you can simplify your workflow by directly instructing ChatGPT, saying: "You have access to my CLI, please execute ...". The rest will be taken care of for you!

### Using OS GPT to Load Datasets and Query Information

Loading Datasets
OS GPT offers the ability to dynamically load documents from specified folders and create searchable vector databases. You can use this feature to, for example, load a folder named technical_files as a dataset and then query it for specific information.

How to Load a Dataset
To load a dataset, you need to send a POST request to the /load_data endpoint. The request should contain a JSON body specifying the folder_path and dataset_name.

Here's an example request to load the folder located at /home/runner/OSGPT/OSGPT/technical_files as data set "technical_files"

```json
{
  "folder_path": "/home/runner/OSGPT/OSGPT/technical_files",
  "dataset_name": "technical_files"
}
```
Upon successful execution, you should receive a response like:

```json
{
  "Database for technical_files created successfully!"
}
```
Note: If your folder size is so huge the load_data will take much time to complete the database.Which may throw the error in your chatgpt interface
But the database will be created, Once the database is created you see the info from the settings.json file

### Querying for Specific Information
Once the dataset is loaded, you can query it for specific information. For example, if you want to find documents or files related to "langchain" within the technical_files database, you can do so by sending a POST request to the /query_data endpoint.

The request should contain a JSON body specifying the query and dataset_name.

Example Query:
To search for "langchain" in the technical_files database, your JSON body would look like this:

```json
{
  "query": "ravi teja",
  "dataset_name": "personal_files"
}
```

Upon successful execution, OS GPT will search the technical files database for any files or documents related to "langchain" and return the relevant results.

## Security
Please be aware that this plugin executes commands as-is, without any sanitization or security checks. Make sure to only use it in a secure and controlled environment, and do not expose the server to the public internet. This ChatGPT Plugin is designed for developers, and should not be deployed on production servers! Use it only on localhost!

## 🚀 Future Enhancements
### GPT Vision Capabilities
We're incredibly excited about the imminent release of the GPT Vision API. As soon as it becomes available, we plan to integrate image analysis features into OSGPT. This will enable users to query not just text-based documents but also images, unlocking a whole new dimension of usability. Please note that as of the current version, ChatGPT doesn't support the simultaneous use of plugins and vision capabilities. We're looking forward to this integration as future releases allow.

### Advanced Data Analysis
We understand the value of data, and we're committed to providing advanced analysis features in the coming days. Whether you're working with Excel spreadsheets or CSV files, OSGPT will offer the tools you need to make sense of your data. Stay tuned for updates!

## Contributing
Contributions are welcome! Please feel free to submit a pull request.

## ❤️ Thank you for your support!
If you appreciate my work, please consider supporting me:
- :star: my projects: Starring projects on GitHub helps increase their visibility and can help others find my work.

## References
This repo is an extended version of ChatGPT-ShellMaster which adds the features of file searching and dynamic loading of file capabilities.

### Copyright
- [Volkan Kücükbudak //NCF](https://gihub.com/volkansah)
- [Link to ChatGPT Shellmaster](https://github.com/VolkanSah/ChatGPT-ShellMaster/)

### License
This project is licensed under the "Help the World Grow [💔](https://jugendamt-deutschland.de) " License . See the [LICENSE](LICENSE) file for details 
