from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage
import time

# Define the state schema
class ChatState(TypedDict):
  input: str
  chat_history: List[HumanMessage | AIMessage]

# Initialize chat model
chat_model = ChatOllama(model="llama3.2:3b")

# Create prompt template
prompt = ChatPromptTemplate.from_messages([
  ("system", "You are a helpful AI assistant that remembers previous conversations."),
  MessagesPlaceholder(variable_name="chat_history"),
  ("human", "{input}"),
])

# Initialize the state graph with schema
workflow = StateGraph(state_schema=ChatState)

# Define the initial state
workflow.add_node("chat", {
  "input": lambda x: x["input"],
  "chat_history": lambda x: x.get("chat_history", [])
})

# Create the chat chain
chat_chain = (
  prompt 
  | chat_model
)

# Add the chain to the node
workflow.set_entry_point("chat")
workflow.add_edge("chat", "chat")

# Compile the graph
app = workflow.compile()

def chat_with_memory():
  print("Starting conversation (type 'quit' to exit):")
  chat_history = []
  
  while True:
      user_input = input("\nYou: ")
      
      if user_input.lower() == 'quit':
          break
          
      try:
          # Prepare the input for the graph
          config = {
              "input": user_input,
              "chat_history": chat_history
          }
          
          # Get response
          response = chat_chain.invoke({
              "input": user_input,
              "chat_history": chat_history
          })
          
          # Extract the content from the response
          response_content = response.content if hasattr(response, 'content') else str(response)
          
          # Update chat history
          chat_history.extend([
              HumanMessage(content=user_input),
              AIMessage(content=response_content)
          ])
          
          print(f"\nAI: {response_content}")
          time.sleep(1)
          
      except Exception as e:
          print(f"Error occurred: {e}")
          break

if __name__ == "__main__":
  chat_with_memory()