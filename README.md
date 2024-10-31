# General Documentation
The open-source framework that we will be using is called [LangChain](https://python.langchain.com/docs/introduction/). It is a framework designed to facilitate the development of applications powered by large language models (LLMs). It provides tools and abstractions that help developers build complex applications by integrating LLMs with other data sources and computational resources.

### Clone the repository and navigate to the directory
`git clone https://github.com/TheoPetropoulos/langchain-course.git`
`cd langchain-course`

#### Create a virtual environment using venv
`python -m venv langchain-env`

# Activate the virtual environment
### On Windows
`langchain-env\Scripts\activate`
### On macOS and Linux
`source langchain-env/bin/activate`

### Install the required packages
`pip install -r requirements.txt`

### Running Exercises

#### Navigate to the `exercises` directory and run the Python scripts
`cd exercises`

`python simple_exercise.py`

`python medium_exercise.py`

`python hard_exercise.py`

### Notes

- Ensure you have the necessary model files downloaded and placed in the correct directory as specified in the exercises.
- Modify the `model_path` in the scripts to point to your local model files.
