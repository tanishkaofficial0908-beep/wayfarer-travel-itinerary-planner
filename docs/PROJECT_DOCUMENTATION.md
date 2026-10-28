# Wayfarer — Project Documentation

## 1. Project Overview

Wayfarer is an AI-powered travel itinerary planner designed to help users organize trips according to their destination, travel dates, budget, number of travellers, and personal interests.

The application uses an AI service to generate a structured, day-wise itinerary and provides estimated activity costs and travel suggestions.

## 2. Problem Statement

Planning a trip often requires researching destinations, organizing daily activities, estimating expenses, and considering individual preferences. This can be time-consuming when information is scattered across different sources.

Wayfarer aims to simplify this process by bringing personalized itinerary generation into a single web application.

## 3. Project Objectives

- Develop a user-friendly travel planning interface.
- Generate personalized travel itineraries using AI.
- Organize activities into morning, afternoon, and evening schedules.
- Provide estimated activity costs and a budget summary.
- Store trip details and generated itineraries in a database.
- Deploy the application so users can access it online.

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| React | Builds the interactive frontend interface |
| FastAPI | Provides backend API endpoints |
| Python | Implements backend application logic |
| Groq API | Supports AI-powered itinerary generation |
| Supabase | Stores trip information and itinerary data |
| Render | Hosts the deployed frontend and backend |

## 5. System Architecture

Wayfarer follows a frontend-backend architecture.

1. The user enters trip details through the React frontend.
2. The frontend sends a request to the FastAPI backend.
3. The backend processes the request and communicates with the Groq API.
4. The AI generates a proposed travel itinerary.
5. The backend validates and processes the generated data.
6. When database integration is available, trip details and itinerary data are stored in Supabase.
7. The backend returns the result to the frontend for display.

## 6. Main Features

### 6.1 Trip Details

Users can provide their destination, departure and return dates, total budget, and number of travellers.

### 6.2 Interest-Based Personalization

Users can select interests and travel preferences to personalize the generated itinerary.

### 6.3 AI Itinerary Generation

The application uses an AI model through the Groq API to generate a structured travel plan.

### 6.4 Day-Wise Schedule

The itinerary organizes activities into morning, afternoon, and evening sections.

### 6.5 Budget Estimation

The application processes estimated activity costs and provides a budget summary.

### 6.6 Travel Suggestions

The generated itinerary can include food recommendations, transportation advice, and practical travel tips.

### 6.7 Database Integration

Supabase is used to store trip details and generated itinerary data for supported requests.

## 7. Backend Responsibilities

The FastAPI backend is responsible for:

- Receiving and processing trip-generation requests.
- Validating trip information.
- Communicating with the Groq API.
- Processing and validating the generated itinerary.
- Calculating the estimated total cost.
- Saving trip data to Supabase when configured.
- Returning the generated itinerary to the frontend.

## 8. Frontend Responsibilities

The React frontend is responsible for:

- Displaying the application interface.
- Collecting trip details and user preferences.
- Sending requests to the backend API.
- Displaying the generated itinerary.
- Presenting activity schedules and budget information.

## 9. Database Design

The application uses a Supabase table named `trips`.

The table stores information such as:

| Field | Description |
|---|---|
| `id` | Unique trip identifier |
| `destination` | Selected travel destination |
| `start_date` | Trip departure date |
| `end_date` | Trip return date |
| `budget` | User-provided total budget |
| `travelers` | Number of travellers |
| `interests` | Selected travel interests |
| `travel_style` | Preferred travel style |
| `itinerary` | Generated itinerary stored as JSON data |
| `created_at` | Timestamp of record creation |

## 10. Security Considerations

- API keys and database credentials are configured through environment variables.
- Secret credentials must not be committed to the public repository.
- Database access should use appropriate permissions and access controls.
- Frontend and backend communication is configured through the API endpoint and CORS settings.

## 11. Deployment

The frontend and backend are deployed separately using Render.

- **Frontend:** https://wayfarer-travel-itinerary-planner.onrender.com
- **Backend:** https://wayfarer-travel-api.onrender.com

The source code is maintained in the GitHub repository:

https://github.com/tanishkaofficial0908-beep/wayfarer-travel-itinerary-planner

## 12. Limitations

- AI-generated itineraries may require verification and refinement.
- Estimated costs may differ from actual travel expenses.
- Long-duration trips may encounter incomplete AI responses.
- The application depends on external AI and hosting services.

## 13. Future Scope

Potential improvements include:

- More reliable generation for longer trips.
- Improved budget optimization.
- Integration of live weather and destination information.
- Interactive maps and route planning.
- Hotel and transportation recommendations.
- User accounts and saved-trip management.
- Enhanced error handling and itinerary validation.

## 14. Conclusion

Wayfarer demonstrates how frontend development, backend API design, AI integration, and database management can be combined to create a personalized travel planning application.

The project aims to make itinerary preparation more convenient by organizing travel preferences, daily activities, and estimated expenses within a single web application.

---

*Wayfarer — Plan smarter. Travel better. Explore with Wayfarer.*
