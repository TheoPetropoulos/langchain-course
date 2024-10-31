# General Documentation
The open-source framework that we will be using is called [LangChain](https://python.langchain.com/docs/introduction/). It is a framework designed to facilitate the development of applications powered by large language models (LLMs). It provides tools and abstractions that help developers build complex applications by integrating LLMs with other data sources and computational resources.

### Setting up Local Large Language Model (LLM)
There are two ways in which you can create GenAI Applications (also known as AI Agents):
1. Have a paid API service, that provides access to closed-source LLMs:
    - [Abacus.AI](https://apps.abacus.ai/chatllm) (Provides access to all LLM's through an ecosystem)
    - [OpenAI](https://openai.com/api/)
    - [Anthropic](https://console.anthropic.com/) - This gives you access to Claude

2. Download a local model:
    - [Ollama](https://ollama.com/download)
        - This is what we will be using for this tutorial! It's super easy and allows you to download any flavor of Llama models: https://github.com/ollama/ollama
    - [HuggingFace](https://huggingface.co/models)
        - [Downloading Models](https://huggingface.co/docs/hub/en/models-downloading) 

Once Ollama is installed, you will be able to run below command:
`ollama pull llama3.2:3b`

This will pull the specific model and install it on your machine. Ollama will then serve this model locally, basically creating a local API for you! You need to be running the application so that you can call the model though.

### Clone the repository and navigate to the directory
`git clone https://github.com/TheoPetropoulos/langchain-course.git`

`cd langchain-course`

#### Create a virtual environment using venv
`python3 -m venv langchain-env`

# Activate the virtual environment
### On Windows
`langchain-env\Scripts\activate`
### On macOS and Linux
`source langchain-env/bin/activate`

### Install the required packages
`pip install --upgrade pip`
`pip install -r requirements.txt`

### Running Exercises

#### Navigate to the `exercises` directory and run the Python scripts
`cd exercises`

`python3 exercises/[choose_exercise].py`

### Notes
- You might not need to use python3. This has to do with your current environment setup.
- I am using python3.12