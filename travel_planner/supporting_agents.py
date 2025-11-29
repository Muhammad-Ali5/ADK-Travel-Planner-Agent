from google.adk.agents import Agent
from travel_planner.tools import google_search_grounding, location_search_tool

from google.adk.tools.agent_tool import AgentTool


llm = "gemini-2.0-flash"
# -----------------------news agent-----------------------
news_agent = Agent(
    model=llm,
    name="news_agent",
    description="Suggests key travel events and news; uses search for current info.",
    instruction="""
        You are responsible for providing a list of events and news recommendations based on the user's query.
        Limit the choices to 10 results. You need to use the google_search_grounding agent tool to search the web for information.
    """,
    tools=[google_search_grounding]
)

# -----------------------places agent-----------------------
places_agent = Agent(
    model=llm,
    name="places_agent",
    description="Suggests locations based on the user preferences.",
    instruction="""
        You are responsible for making suggestions on actual places based on the user's query. Limit the choices to 10 results.
        Each place must have a name, address, and a short description.
        You can use the places_tool to find the latitude and longitude of the place and address
    """,
    tools=[location_search_tool]
)

# -----------------------travel inspiration agent-----------------------
Travel_inspiration_agent = Agent(
    model=llm,
    name="Travel_inspiration_agent",
    description="Inspires users with travel ideas. It may consult news and places agents",
    instruction="""
        You are a travel inspiration agent who helps users find their next big dream vacation destination.
        Your role and goal are to help the user identify a destination and a few activities at that destination the user is interested in.
        
        As part of that, the user may ask you for general history or knowledge about a destination. 
        In that scenario, answer briefly to the best of your ability, but focus on the goal by relating your answer back to the destination 
        and activities the user may be interested in.

        - You will call the two tools 'places_agent(inspiration query)' and 'news_agent(inspiration query)' when appropriate:
            - Use 'news_agent' to provide key events and news recommendations based on the user's query.
            - Use 'places_agent' to provide a list of locations or nearby places to famous locations when the user asks for it.
              For example, "find hotels near Eiffel Tower" should return hotels based on some user preferences.
    """,
    tools=[AgentTool(agent=news_agent), AgentTool(agent=places_agent)]
)