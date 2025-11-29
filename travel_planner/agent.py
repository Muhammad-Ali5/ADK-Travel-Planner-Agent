from google.adk.agents import Agent
from travel_planner.supporting_agents import Travel_inspiration_agent

llm = "gemini-2.0-flash"

root_agent = Agent(
    model= llm,
    name= "Travel_planner_main_agent",
    description= "A helpful travel planning assistant that helps users plan their trips by providing information and suggestions based on their preferences and requirements.", 
    instruction= """
        - You are an exclusive travel concierge agent
        - You help user to discover their dream holidays destination and plan their vacation.
        - Use the inspiration_agent to get the best destination, news, places nearby e.g hotels, cafes, restaurants, etc near attractions and points of interest for the user.
        - You cannot use any tool directly.
    """,
    sub_agents=[Travel_inspiration_agent]
)