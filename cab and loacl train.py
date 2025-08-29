import os
from typing import Optional
import serpapi
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool


class CabsInput(BaseModel):
    origin: str = Field(description="Starting point")
    destination: str = Field(description="Destination")
    ride_type: Optional[str] = Field(
        "uber", description="Cab service type (uber/ola/local). Defaults to Uber-like fares"
    )


class CabsInputSchema(BaseModel):
    params: CabsInput


@tool(args_schema=CabsInputSchema)
def cabs_finder(params: CabsInput):
    """
    Get driving directions (cab travel). Uses Google Maps via SerpAPI.
    """
    query = {
        "api_key": os.environ.get("SERPAPI_API_KEY"),
        "engine": "google_maps_directions",
        "hl": "en",
        "origin": params.origin,
        "destination": params.destination,
        "mode": "driving",
    }

    search = serpapi.search(query)
    data = search.data

    try:
        route = data["directions"][0]
        distance_km = route["distance"]["value"] / 1000
        estimated_fare = round(distance_km * 20, 2)  # approx ₹20/km
        return {
            "summary": route["summary"],
            "duration": route["duration"]["text"],
            "distance": f"{distance_km:.1f} km",
            "estimated_fare_inr": f"₹{estimated_fare}",
        }
    except Exception as e:
        return {"error": str(e), "raw_data": data}
import os
from typing import Optional
import serpapi
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool


class TrainsInput(BaseModel):
    origin: str = Field(description="Starting station or location")
    destination: str = Field(description="Destination station or location")
    departure_time: Optional[str] = Field(
        None, description="Optional departure time in HH:MM (24hr)"
    )


class TrainsInputSchema(BaseModel):
    params: TrainsInput


@tool(args_schema=TrainsInputSchema)
def trains_finder(params: TrainsInput):
    """
    Get local train / metro directions using Google Maps transit.
    """
    query = {
        "api_key": os.environ.get("SERPAPI_API_KEY"),
        "engine": "google_maps_directions",
        "hl": "en",
        "origin": params.origin,
        "destination": params.destination,
        "mode": "transit",
        "transit_mode": "train",
    }
    if params.departure_time:
        query["departure_time"] = params.departure_time

    search = serpapi.search(query)
    data = search.data

    try:
        routes = []
        for route in data.get("directions", []):
            step_summary = [
                f"{step['travel_mode']} → {step.get('name', '')}"
                for step in route.get("steps", [])
            ]
            routes.append({
                "duration": route["duration"]["text"],
                "arrival_time": route.get("arrival_time", {}).get("text", "N/A"),
                "steps": step_summary,
            })
        return routes[:3]
    except Exception as e:
        return {"error": str(e), "raw_data": data}
