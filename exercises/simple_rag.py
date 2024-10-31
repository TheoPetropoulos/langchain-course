from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Initialize Ollama
llm = OllamaLLM(model="llama3.2:3b")
embeddings = OllamaEmbeddings(model="llama3.2:3b")

# Sample documents (in real application, this could be loaded from files)
documents = [
  "LangChain is a framework for developing applications powered by language models.",
  "It provides many modules that can be used to build language model applications.",
  "Vector stores are used to store and retrieve embeddings of text.",
  "Embeddings convert text into numerical vectors that capture semantic meaning.",
  "RAG (Retrieval Augmented Generation) combines retrieval and generation for better responses.",
  "Chain in LangChain allows combining multiple components into a single pipeline.",
  "Agents can use tools and make decisions on which tools to use to accomplish a task.",
  "Memory in LangChain allows storing and retrieving information from past interactions.",
]

# Split documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
splits = text_splitter.create_documents(documents)

# Create vector store
vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)

# Create retriever
retriever = vectorstore.as_retriever()

# Create prompt template
template = """Answer the question based only on the following context:

Context: {context}

Question: {question}

Answer: """

prompt = ChatPromptTemplate.from_template(template)

# Create RAG chain
def format_docs(docs):
  return "\n\n".join(doc.page_content for doc in docs)

chain = (
  {"context": retriever | format_docs, "question": RunnablePassthrough()}
  | prompt
  | llm
  | StrOutputParser()
)

# Example usage
if __name__ == "__main__":
  # Test the RAG system
  questions = [
      "What is LangChain?",
      "What is RAG?",
      "How does memory work in LangChain?",
  ]
  
  print("Testing RAG System with Multiple Questions:\n")
  for question in questions:
      print(f"Question: {question}")
      print(f"Answer: {chain.invoke(question)}\n")