# Wayfarer — AI-Powered Travel Itinerary Planner

Wayfarer is a personalized AI-powered travel itinerary planner that helps users create travel plans based on their destination, travel dates, budget, number of travellers, and personal interests.

## 🌍 Live Demo

**Website:** https://wayfarer-travel-itinerary-planner.onrender.com

**GitHub Repository:** https://github.com/tanishkaofficial0908-beep/wayfarer-travel-itinerary-planner

## ✨ Features

- **Personalized Travel Planning:** Enter your destination, departure date, return date, budget, and number of travellers.
- **Interest-Based Recommendations:** Customize your trip based on your selected interests and travel preferences.
- **AI-Generated Itineraries:** Generate a day-wise travel itinerary using AI.
- **Daily Activity Schedule:** Organize activities into morning, afternoon, and evening.
- **Budget Estimation:** View estimated activity costs and a budget summary.
- **Travel Tips:** Receive helpful suggestions for your trip.
- **Database Integration:** Save generated trip details and itineraries in Supabase.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| React | Frontend user interface |
| FastAPI | Backend REST API |
| Python | Backend development |
| Groq API | AI-powered itinerary generation |
| Supabase | Database for storing trip details |
| Render | Deployment and hosting |

## ⚙️ How It Works

1. The user enters trip details, including destination, travel dates, budget, and travellers.
2. The user selects interests and travel preferences.
3. The React frontend sends the trip request to the FastAPI backend.
4. The backend uses the Groq API to generate a personalized itinerary.
5. The generated itinerary is validated and processed by the backend.
6. Trip details and itinerary data are saved in Supabase when database integration is available.
7. The frontend displays the generated travel plan to the user.

## 🚀 Run Locally

### Prerequisites

- Python 3.10 or a compatible version
- Node.js and npm
- A Groq API key
- A Supabase project, if database functionality is required

### 1. Clone the repository

```bash
git clone https://github.com/tanishkaofficial0908-beep/wayfarer-travel-itinerary-planner.git
cd wayfarer-travel-itinerary-planner
```

### 2. Set up the backend

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root and configure your own credentials:

```env
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_SECRET_KEY=your_supabase_secret_key
```

**Never commit your actual `.env` file or API keys to GitHub.**

Start the backend from the project root:

```bash
python -m uvicorn backend.main:app --reload
```

The backend will be available at `http://127.0.0.1:8000`.

### 3. Set up the frontend

Open a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local frontend URL shown in the terminal, usually `http://localhost:5173`.

## 🔐 Security

- Store API keys and database credentials in environment variables.
- Keep secret credentials out of the public repository.
- Use appropriate database permissions and access controls.

## 🔮 Future Improvements

- Improve itinerary generation for longer trips.
- Enhance travel recommendations and budget optimization.
- Add more interactive travel-planning features.
- Improve error handling and itinerary validation.

## 👩‍💻 Project Information

**Project Name:** Wayfarer — AI-Powered Travel Itinerary Planner

**Category:** AI-Powered Web Application

**Purpose:** To simplify travel planning through personalized, AI-generated itineraries.

---

*Plan smarter. Travel better. Explore with Wayfarer.*
