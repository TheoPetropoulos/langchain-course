from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool  # Make sure to import Tool
import datetime
import math

# Initialize chat model
chat_model = ChatOllama(model="llama3.2:3b")

# Create custom tools
def calculate_days_between_dates(dates: str) -> str:
  """Calculate the number of days between two dates in format YYYY-MM-DD"""
  try:
      # Split the input string into two dates
      date_str1, date_str2 = [d.strip() for d in dates.split(',')]
      
      date1 = datetime.datetime.strptime(date_str1, "%Y-%m-%d")
      date2 = datetime.datetime.strptime(date_str2, "%Y-%m-%d")
      days = abs((date2 - date1).days)
      return f"There are {days} days between {date_str1} and {date_str2}"
  except ValueError:
      return "Please provide dates in the format YYYY-MM-DD, YYYY-MM-DD"
  except Exception as e:
      return f"Error: {str(e)}. Please provide dates in the format YYYY-MM-DD, YYYY-MM-DD"

def calculate_circle_area(radius: float) -> str:
  """Calculate the area of a circle given its radius"""
  try:
      radius = float(radius)
      area = math.pi * (radius ** 2)
      return f"The area of a circle with radius {radius} is {area:.2f} square units"
  except ValueError:
      return "Please provide a valid number for the radius"

# When creating the tool, make the name more specific

# Initialize tools
search = DuckDuckGoSearchRun()
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

tools = [
  Tool(
      name="Search",
      func=search.run,
      description="Useful for searching current information on the internet",
      return_direct=True
  ),
  Tool(
      name="Wikipedia",
      func=wikipedia.run,
      description="Useful for getting detailed information from Wikipedia",
      return_direct=True
  ),
  Tool(
    name="DateCalculator",
    func=calculate_days_between_dates,
    description="Calculate days between two dates. Input should be two dates in format YYYY-MM-DD separated by comma",
    return_direct=True
  ),
  Tool(
    name="CircleCalculator",
    func=calculate_circle_area,
    description="Calculate the area of a circle. Input should be just the radius number",
    return_direct=True
  )
]

# Create prompt template
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Remember to use the exact tool names when specifying an Action.
Only provide a Final Answer after you have used the necessary tools.

Begin!

Question: {input}
{agent_scratchpad}"""

prompt = PromptTemplate(
  template=template,
  input_variables=["input", "agent_scratchpad"],
  partial_variables={
      "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in tools]),
      "tool_names": ", ".join([tool.name for tool in tools])
  }
)

# Create agent
agent = create_react_agent(
  llm=chat_model,
  tools=tools,
  prompt=prompt
)

# Create agent executor
agent_executor = AgentExecutor(
  agent=agent,
  tools=tools,
  verbose=True,
  handle_parsing_errors=True,
  max_iterations=3 
)

def run_agent():
  print("Starting agent (type 'quit' to exit):")
  while True:
      user_input = input("\nYou: ")
      
      if user_input.lower() == 'quit':
          break
          
      try:
          response = agent_executor.invoke(
              {"input": user_input},
              {"callbacks": None}  # This can help reduce verbose output
          )
          # Only print the final output
          print(f"\nAI: {response['output']}")
          
      except Exception as e:
          print(f"Error occurred: {e}")
          break

if __name__ == "__main__":
  run_agent()

# Using the DateCalculator:
# "How many days are there between 2024-01-01 and 2024-12-25?"
# "Calculate the days between 2023-10-31 and 2024-04-15"
# Using the CircleCalculator:
# "What is the area of a circle with radius 5?"
# "Calculate the area of a circle with radius 7.5"
# Using the Wikipedia tool:
# "Who was Marie Curie and what were her main discoveries?"
# "What is the history of the Eiffel Tower?"
# Using the Search tool (DuckDuckGo):
# "What are the latest developments in artificial intelligence?"
# "What is the current weather in Paris?"