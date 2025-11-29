from google.adk.tools.google_search_tool import google_search
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

llm = "gemini-2.0-flash"

# -----------------------search agent-----------------------
_search_agent = Agent(
    model=llm,
    name="google_search_wrapped_agent",
    description="An agent providing Google-search grounding capability",
    instruction="""
       Answer the user's question directly using the google_search grounding tool; provide a brief but concise response.
       Rather than a detailed answer, provide the immediate actionable item for a tourist or traveler, in a single sentence.
       Do not ask the user to check or look up information themselves; that's your role. Do your best to be informative.

       IMPORTANT:
        - Always return the response in bullet points.
        - Specify what matters to the user.
    """,
    tools=[google_search]
)

google_search_grounding = AgentTool(agent= _search_agent)

# -----------------------location search tool-----------------------
from google.adk.tools import FunctionTool
from geopy.geocoders import Nominatim
import requests

def find_nearby_places(query: str, location: str, radius: int = 3000, limit: int = 10) -> str:
    """
    Find nearby places for any text query using ONLY free OpenStreetMap APIs (no API key needed).

    Args:
    
        query (str): What you're looking for (e.g., "restaurants", "hotels", "gyms", "attractions", etc.)
        location (str): The city or area to search in.
        radius (int, optional): Search radius in meters (default: 3000).
        limit (int, optional): Number of results to show (default: 10).

    Returns:
        str: List of matching place names and addresses.
    """
    try:
        # step1: Geocode the location to get coordinates
        geolocator = Nominatim(user_agent="open_place_finder/travel_planner_adk_v1")
        loc_obj = geolocator.geocode(location)
        if not loc_obj:
            return f"Location not found: {location}"
        
        lat, lon = loc_obj.latitude, loc_obj.longitude

        # step2: Query Overpass API for matching places
        overpass_url = "https://overpass-api.de/api/interpreter"
        overpass_query = f"""
            [out:json][timeout:25];
            (
                node["name"~"{query}", i](around:{radius},{lat},{lon});
                node["amenity"~"{query}", i](around:{radius},{lat},{lon});
                node["shop"~"{query}", i](around:{radius},{lat},{lon});
                node["tourism"~"{query}", i](around:{radius},{lat},{lon});
                node["leisure"~"{query}", i](around:{radius},{lat},{lon});
                node["historic"~"{query}", i](around:{radius},{lat},{lon});
            );
            out body {limit};
        """
        response = requests.get(overpass_url, params={"data": overpass_query})
        
        if response.status_code == 200:
            data = response.json()
            elements = data.get("elements", [])
            if not elements:
                return f"No places found for {query} in {location}."
            
            # Step3: Format the response/Results
            output = [f"Top results for {query} near {location}:"]
            # Limit results manually since Overpass limit might return more nodes than expected if grouped
            for el in elements[:limit]:
                tags = el.get("tags", {})
                name = tags.get("name", "Unknown Place")
                street = tags.get("addr:street", "")
                city = tags.get("addr:city", "")
                # Some nodes might not have address details, just coordinates
                full_address = ", ".join(filter(None, [street, city]))
                
                output.append(f"- {name} | {full_address if full_address else 'Address details not available'} (Lat: {el.get('lat')}, Lon: {el.get('lon')})")
                
            return "\n".join(output)
        else:
            return f"Error querying Overpass API: {response.status_code}"

    except Exception as e:
        return f"Error occurred: {str(e)}"

# convert function to tool
location_search_tool = FunctionTool(func=find_nearby_places)