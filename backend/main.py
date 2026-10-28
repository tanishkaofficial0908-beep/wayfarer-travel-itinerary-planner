
import os
import json
from datetime import date
from math import isfinite

from supabase import create_client, Client
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from pydantic import BaseModel, Field

# Load environment variables from the root .env file
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SECRET_KEY")

supabase: Client | None = None

if supabase_url and supabase_key:
    supabase = create_client(supabase_url, supabase_key)

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
        "https://wayfarer-travel-itinerary-planner.onrender.com",
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


@app.get("/api/db-check")
def db_check():
    if supabase is None:
        raise HTTPException(
            status_code=503,
            detail="Supabase credentials are not configured",
        )

    try:
        supabase.table("trips").select("id").limit(1).execute()
        return {
            "status": "connected",
            "message": "Supabase connection successful",
        }
    except Exception as exc:
        print(f"Supabase connection error: {type(exc).__name__}")
        raise HTTPException(
            status_code=500,
            detail="Could not connect to Supabase or access the trips table",
        )


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


def normalize_budget(itinerary: dict, budget: float, duration: int):
    """
    Validate day-wise costs and calculate the overall total from them.
    Each time-slot cost represents the combined estimated expenses
    for that period, not just the entry ticket for an activity.
    """
    days = itinerary.get("days")

    if not isinstance(days, list) or len(days) != duration:
        raise HTTPException(
            status_code=502,
            detail="The AI returned an incomplete itinerary. Please try again.",
        )

    day_total = 0.0

    for index, day in enumerate(days, start=1):
        if not isinstance(day, dict):
            raise HTTPException(
                status_code=502,
                detail="The AI returned an invalid day entry. Please try again.",
            )

        for slot_name in ("morning", "afternoon", "evening"):
            slot = day.get(slot_name)

            if not isinstance(slot, dict):
                raise HTTPException(
                    status_code=502,
                    detail="The AI returned an incomplete daily schedule. Please try again.",
                )

            cost = slot.get("estimated_cost")

            if isinstance(cost, bool) or not isinstance(cost, (int, float)):
                raise HTTPException(
                    status_code=502,
                    detail="The AI returned an invalid expense estimate. Please try again.",
                )

            if not isfinite(cost) or cost < 0:
                raise HTTPException(
                    status_code=502,
                    detail="The AI returned an invalid expense estimate. Please try again.",
                )

            day_total += cost

        # Ensure day numbering remains consistent.
        day["day"] = index

    summary = itinerary.get("budget_summary")

    if not isinstance(summary, dict):
        summary = {}

    # Use one consistent source of truth for the displayed trip total.
    estimated_total = round(day_total, 2)

    summary["estimated_total"] = estimated_total
    summary["currency"] = "INR"

    remaining = round(max(budget - estimated_total, 0), 2)

    if estimated_total > budget:
        budget_note = (
            f"The estimated trip cost is ₹{estimated_total:,.2f}, "
            f"which exceeds the budget of ₹{budget:,.2f} by "
            f"₹{estimated_total - budget:,.2f}. "
            "Review the itinerary to reduce expenses."
        )
    elif estimated_total < budget * 0.80:
        budget_note = (
            f"The estimated trip cost is ₹{estimated_total:,.2f} "
            f"out of the ₹{budget:,.2f} budget. "
            f"Approximately ₹{remaining:,.2f} remains. "
            "Consider adding worthwhile activities, better-suited "
            "accommodation, or other useful experiences if appropriate."
        )
    else:
        budget_note = (
            f"The estimated trip cost is ₹{estimated_total:,.2f} "
            f"out of the ₹{budget:,.2f} budget. "
            f"Approximately ₹{remaining:,.2f} remains as a buffer. "
            "Actual prices may vary."
        )

    # Preserve any useful assumptions provided by the AI.
    existing_notes = summary.get("notes", "")
    if not isinstance(existing_notes, str):
        existing_notes = ""

    summary["notes"] = (
        f"{budget_note} "
        f"{existing_notes}".strip()
    )

    itinerary["budget_summary"] = summary

    return itinerary


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
You are a practical travel-planning assistant. Create a realistic,
personalized travel itinerary with a consistent and useful budget.

TRIP DETAILS
Destination: {trip.destination}
Start date: {trip.start_date}
End date: {trip.end_date}
Number of travelers: {trip.travelers}
TOTAL AVAILABLE BUDGET IN INR: ₹{trip.budget:,.2f}
Interests: {", ".join(trip.interests)}
Travel style: {trip.travel_style}
Number of calendar days: {duration}

IMPORTANT BUDGET RULES
- Treat ₹{trip.budget:,.2f} as the total available budget for the entire
  group of {trip.travelers} traveler(s), not a per-person budget.
- Plan a satisfying, realistic trip that makes sensible use of the budget.
- When realistic for this destination, duration, and travel style, aim for
  an estimated total of approximately 85% to 95% of the available budget.
- Do not automatically create an unusually cheap trip just to stay below
  the budget.
- Do not inflate prices, invent expenses, or add unnecessary activities
  merely to consume the budget.
- If the destination, duration, or travel style makes that target unrealistic,
  provide a sensible estimate and explain why in the notes.
- Consider accommodation, food, local transport, activities, entry fees,
  and reasonable miscellaneous expenses wherever applicable.
- Avoid double-counting an expense.
- Costs must be in INR and must reflect the entire group, not one traveler.
- The estimated_cost in each morning, afternoon, and evening slot must
  represent the combined estimated trip expenses for that time period.
  Include relevant activities, food, local transport, and an appropriate
  share of accommodation or other trip expenses where applicable.
- Distribute expenses across the days and time slots realistically.
- Every estimated_cost must be a non-negative number.
- The budget_summary.estimated_total MUST equal the sum of every
  morning, afternoon, and evening estimated_cost across all days.
- Do not add separate expenses to the summary that are already counted
  in the day-wise estimates.
- Include the budget assumptions and any important exclusions in notes.
- The available budget is a limit and planning guide, not a requirement
  to spend every rupee.

ITINERARY RULES
- Return valid JSON only, without Markdown fences.
- Return exactly {duration} entries in the "days" array.
- The first day's date must be {trip.start_date}.
- Each following day's date must increase by exactly one calendar day.
- The last day's date must be {trip.end_date}.
- Set "duration_days" to exactly {duration}.
- Number the days consecutively from 1 to {duration}.
- Include morning, afternoon, and evening activities for every day.
- Include a short description and estimated cost for each time slot.
- Include food suggestions and practical transport advice.
- Treat costs as estimates, not guaranteed prices.
- Do not invent precise opening hours or claim live availability.
- If information is uncertain, say it should be verified.
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
        "description": "What to do and estimated expenses for this period",
        "estimated_cost": 0
      }},
      "afternoon": {{
        "activity": "Activity name",
        "description": "What to do and estimated expenses for this period",
        "estimated_cost": 0
      }},
      "evening": {{
        "activity": "Activity name",
        "description": "What to do and estimated expenses for this period",
        "estimated_cost": 0
      }},
      "food_suggestions": ["Suggestion"],
      "transport_advice": "Advice"
    }}
  ],
  "budget_summary": {{
    "estimated_total": 0,
    "currency": "INR",
    "notes": "Budget assumptions, inclusions, and exclusions"
  }},
  "travel_tips": ["Tip"]
}}
"""

    # Generate the itinerary with Groq.
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You create useful, realistic travel itineraries. "
                        "Follow the requested JSON structure exactly. "
                        "Ensure every cost is plausible and every budget "
                        "total matches the sum of day-wise costs."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content

        if not content:
            raise HTTPException(
                status_code=502,
                detail="The AI returned an empty response. Please try again.",
            )

        itinerary = json.loads(content)

        if not isinstance(itinerary, dict):
            raise HTTPException(
                status_code=502,
                detail="The AI returned an invalid itinerary. Please try again.",
            )

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="The AI returned an invalid JSON response. Please try again.",
        )

    except HTTPException:
        raise

    except Exception as exc:
        print(f"Groq itinerary generation error: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=502,
            detail=(
                "Could not generate the itinerary. Check your Groq API key, "
                "model availability, account limits, and terminal logs."
            ),
        )

    # Ensure the total matches the day-wise cost estimates.
    itinerary = normalize_budget(itinerary, trip.budget, duration)

    # Check database availability before saving.
    if supabase is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "The itinerary was generated, but the database "
                "is not configured and the trip was not saved."
            ),
        )

    # Prepare the database record.
    trip_record = {
        "destination": trip.destination,
        "start_date": trip.start_date.isoformat(),
        "end_date": trip.end_date.isoformat(),
        "budget": trip.budget,
        "travelers": trip.travelers,
        "interests": trip.interests,
        "travel_style": trip.travel_style,
        "itinerary": itinerary,
    }

    # Save the generated itinerary to Supabase.
    try:
        supabase.table("trips").insert(trip_record).execute()

    except Exception as exc:
        print(f"Supabase save error: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=500,
            detail=(
                "The itinerary was generated, but saving it "
                "to the database failed."
            ),
        )

    return {
        "message": "AI itinerary generated and saved successfully!",
        "itinerary": itinerary,
    }

