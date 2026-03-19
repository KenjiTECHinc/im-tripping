from google.adk.agents import LlmAgent, BaseAgent
from google.adk.tools import google_search

# ==========================================
# 1. Custom Tools
# ==========================================

def write_to_google_sheet(itinerary_data: str) -> dict:
    """
    Parses the compiled itinerary and writes it to a formatted Google Sheet.
    (Note: You will need to implement the actual gspread/Sheets API logic here later)
    """
    print("Formatting and pushing data to Google Sheets...")
    # TODO: Add Google Sheets API logic here to parse the string into rows/columns
    return {
        "status": "success", 
        "message": "Itinerary successfully written to Sheets.",
        "sheet_url": "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID" 
    }

# ==========================================
# 2. Specialized Sub-Agents
# ==========================================

locations_planner = LlmAgent(
    name="location_planner",
    model="gemini-2.5-flash",
    description="Finds interesting locations, activities, and local attractions.",
    instruction="""You are a location expert. Use google_search to find top-rated spots, 
    local events, operating hours, and reference links based on user preferences. 
    Return a detailed list of activities day-by-day.""",
    tools=[google_search],
)

logistics_planner = LlmAgent(
    name="logistics_planner",
    model="gemini-2.5-flash",
    description="Handles transportation, accommodations, and pricing estimates.",
    instruction="""You are a logistics expert. Use google_search to find realistic travel options 
    (flights/trains), hotel recommendations, and estimate costs. Always include links 
    to the booking sites or references you find.""",
    tools=[google_search],
)

# ==========================================
# 3. The Coordinator (Root Agent)
# ==========================================

# We recommend a 'Pro' model for the coordinator as it requires stronger reasoning to delegate tasks.
coordinator_agent = BaseAgent(
    name="trip_coordinator",
    model="gemini-2.5-pro", 
    description="Coordinates the trip planning process and outputs to Google Sheets.",
    instruction="""You are the master trip coordinator. Follow these steps:
    1. Analyze the user's trip request.
    2. Call 'location_planner' to build a day-by-day activity list.
    3. Call 'logistics_planner' to find flights, hotels, and prices for those days.
    4. Compile all this data into a highly structured itinerary (Dates, Transport, Locations, Accommodations, Prices, Links).
    5. Call 'write_to_google_sheet' with the compiled data to save it.
    6. Return a friendly summary to the user along with the Google Sheet link.
    """,
    tools=[locations_planner, logistics_planner, write_to_google_sheet], 
)