from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="llama3.2:3b")

# Run a simple inference
response = llm.invoke("What is the capital of France?")
print(response)