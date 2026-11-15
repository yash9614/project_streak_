import os
from dotenv import load_dotenv
from openai import OpenAI
from models import TravelItinerary

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"


def generate_itinerary(messages: list[dict]) -> TravelItinerary:
    """
    messages: list of {"role": "user"|"assistant", "content": "..."}
    Called only when the user clicks Generate Final Itinerary.
    """
    response = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """You are an expert travel planner.
Return a complete, realistic, and practical itinerary.
Use real places, reasonable costs, and clear day-by-day structure.
Always respond with valid structured data matching the TravelItinerary schema."""
            },
            *messages
        ],
        response_format=TravelItinerary,
    )
    return response.choices[0].message.parsed
