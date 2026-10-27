
import os
import json
from datetime import date

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from pydantic import BaseModel, Field

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

app = FastAPI(
    title="Personalized Travel Itinerary Planner",
    description="An AI-powered travel planning application",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripRequest(BaseModel):
    destination: str = Field(min_length=2, max_length=100)
    start_date: date
    end_date: date
    budget: float = Field(gt=0)
    travelers: int = Field(default=1, ge=1, le=50)
    interests: list[str] = Field(min_length=1)
    travel_style: str = "balanced"


@app.get("/")
def home():
    return {
        "message": "Welcome to the Personalized Travel Itinerary Planner!",
        "status": "Backend is running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


def validate_dates(trip: TripRequest):
    if trip.end_date < trip.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date cannot be before start date.",
        )


@app.post("/api/trips/preview")
def preview_trip(trip: TripRequest):
    validate_dates(trip)

    return {
        "message": "Trip preferences received successfully!",
        "trip": trip.model_dump(mode="json"),
        "next_step": "Use /api/trips/generate to create an AI itinerary.",
    }


@app.post("/api/trips/generate")
def generate_itinerary(trip: TripRequest):
    validate_dates(trip)

    if client is None:
        raise HTTPException(
            status_code=500,
            detail="Groq API key not found. Check your .env file.",
        )

    duration = (trip.end_date - trip.start_date).days + 1

    prompt = f"""
You are a practical travel-planning assistant.

Create a personalized itinerary using these preferences:
Destination: {trip.destination}
Start date: {trip.start_date}
End date: {trip.end_date}
Number of travelers: {trip.travelers}
Total budget: {trip.budget}
Interests: {", ".join(trip.interests)}
Travel style: {trip.travel_style}
Number of calendar days: {duration}

Requirements:
- Return valid JSON only, without Markdown fences.

- Return exactly {duration} entries in the "days" array, no more and no fewer.
- The first day's date must be {trip.start_date}.
- Each following day's date must increase by exactly one calendar day.
- The last day's date must be {trip.end_date}.
- Set "duration_days" to exactly {duration}.
- Number the days consecutively from 1 to {duration}.
- Include morning, afternoon, and evening activities.
- Include a short description and estimated cost for each activity.
- Include food suggestions and practical transport advice.
- Keep the estimated total within the stated budget where feasible.
- Treat costs as estimates, not guaranteed prices.
- Do not invent precise opening hours or claim live availability.
- If information is uncertain, say that it should be verified.
- Include a budget summary and useful travel tips.

Use this JSON structure:
{{
  "destination": "{trip.destination}",
  "duration_days": {duration},
  "days": [
    {{
      "day": 1,
      "date": "YYYY-MM-DD",
      "morning": {{
        "activity": "Activity name",
        "description": "What to do",
        "estimated_cost": 0
      }},
      "afternoon": {{
        "activity": "Activity name",
        "description": "What to do",
        "estimated_cost": 0
      }},
      "evening": {{
        "activity": "Activity name",
        "description": "What to do",
        "estimated_cost": 0
      }},
      "food_suggestions": ["Suggestion"],
      "transport_advice": "Advice"
    }}
  ],
  "budget_summary": {{
    "estimated_total": 0,
    "currency": "INR",
    "notes": "Budget assumptions"
  }},
  "travel_tips": ["Tip"]
}}
"""

    try:
        response = client.chat.completions.create(
            # This model name must be available to your Groq account.
            
model="openai/gpt-oss-120b",

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You create useful, realistic travel itineraries. "
                        "Follow the requested JSON format."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        itinerary = json.loads(content)

        return {
            "message": "AI itinerary generated successfully!",
            "itinerary": itinerary,
        }

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="The AI returned an invalid JSON response. Please try again.",
        )
    except Exception as exc:
        # Keep API keys and internal error details out of the response.
        print(f"Groq itinerary generation error: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=502,
            detail=(
                "Could not generate the itinerary. Check your Groq API key, "
                "model availability, account limits, and terminal logs."
            ),
        )
