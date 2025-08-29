# 🧳 AI Travel Planner 

An AI-powered **Travel Planning Assistant** built with **Streamlit**, **LangGraph**, and **LangChain Agents**.  
Plan itineraries, find hotels, book cabs, check local trains, explore tourist spots, get weather forecasts, packing lists, food & culture info — all in one place 🚀.

---

## ✨ Features

- 📅 **Itinerary Generator** — AI-powered travel plan based on preferences (destination, budget, type, duration).  
- 🏨 **Hotels Agent** — fetches hotel options via Google Hotels (SerpAPI).  
- 🚖 **Cabs Agent** — helps with local cab booking search.  
- 🚆 **Local Trains Agent** — shows metro/local train info for Mumbai.  
- 🗺 **Tourist Spots Agent** — discovers top attractions at your destination.  
- 🌤 **Weather Forecast Agent** — provides destination weather.  
- 🎒 **Packing List Agent** — generates a checklist based on trip type & weather.  
- 🍽 **Food & Culture Agent** — highlights local cuisines & cultural experiences.  
- 💬 **Chat Agent** — ask follow-up questions about your trip.  
- 📄 **Export to PDF** — download your generated itinerary.

---

## 🛠 Tech Stack

- [Streamlit](https://streamlit.io/) – UI framework  
- [LangChain](https://www.langchain.com/) + [LangGraph](https://langchain-ai.github.io/langgraph/) – multi-agent workflow  
- [ChatOllama](https://ollama.com/) – Local LLM (Llama3)  
- [Google Serper API](https://serper.dev/) – for search & tourist spots  
- [SerpAPI](https://serpapi.com/) – for hotels API  
- [dotenv](https://pypi.org/project/python-dotenv/) – environment management  

---

## 📦 Installation

```bash
# Clone repo
git clone https://github.com/harsh kumare/ai-travel-planner.git
cd ai-travel-planner

# Create environment
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

# Install dependencies
pip install -r requirements.txt
🔑 Environment Variables
Create a .env file in the project root:

ini
Copy code
# For Hotels Agent
SERPAPI_API_KEY=your_serpapi_key

# For Tourist Spots Agent
SERPER_API_KEY=your_serper_key

# For Ollama LLM
# Ensure Ollama is running locally with llama3 model pulled
🚀 Run the App
bash
Copy code
streamlit run app.py
Then open: http://localhost:8501

📖 Usage
Fill out the form with destination, travel dates, duration, budget, etc.

Click Generate Itinerary → AI builds your base plan.

Use buttons to fetch:

🏨 Hotels

🚖 Cabs

🚆 Trains

🗺 Tourist Spots

🌤 Weather

🎒 Packing List

🍽 Food & Culture

Ask trip-specific questions via the chat sidebar.

Export your trip plan as a PDF.

📂 Project Structure
graphql
Copy code
ai-travel-planner/
│── app.py                  # Main Streamlit app
│── agents/                 # Multi-agent modules
│   ├── generate_itinerary.py
│   ├── recommend_activities.py
│   ├── fetch_useful_links.py
│   ├── weather_forecaster.py
│   ├── packing_list_generator.py
│   ├── food_culture_recommender.py
│   ├── chat_agent.py
│   ├── hotels_finder.py
│   ├── cabs_finder.py
│   ├── trains_finder.py
│   └── tourist_spots.py    # NEW Tourist Spots Agent
│── utils_export.py          # PDF export logic
│── requirements.txt
│── README.md
🛤 Roadmap
🔗 Integrate live cab APIs (Uber/Ola)

🚆 Real-time Mumbai local train timings

🗓 Add calendar export (Google/Outlook)

🌍 Multi-language support
