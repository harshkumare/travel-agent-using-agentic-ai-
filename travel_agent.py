import streamlit as st
import json
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langchain_community.chat_models import ChatOllama
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
import os

# Import agents
from agents import (
    generate_itinerary,
    recommend_activities,
    fetch_useful_links,
    weather_forecaster,
    packing_list_generator,
    food_culture_recommender,
    chat_agent,
)
from travel_tools import hotels_finder, cabs_finder, trains_finder  # NEW
from utils_export import export_to_pdf

# Load environment variables
load_dotenv()

# Initialize LLM
st.set_page_config(page_title="AI Travel Planner", layout="wide")
try:
    llm = ChatOllama(model="llama3.2", base_url="http://localhost:11434")
except Exception as e:
    st.error(f"LLM initialization failed: {str(e)}")
    st.stop()

# Initialize GoogleSerperAPIWrapper
try:
    search = GoogleSerperAPIWrapper()
except Exception as e:
    st.error(f"Serper API initialization failed: {str(e)}")
    st.stop()

# Define state
class GraphState(TypedDict):
    preferences_text: str
    preferences: dict
    itinerary: str
    activity_suggestions: str
    useful_links: list[dict]
    weather_forecast: str
    packing_list: str
    food_culture_info: str
    chat_history: Annotated[list[dict], "List of question-response pairs"]
    user_question: str
    chat_response: str
    hotels: list[dict]           # NEW
    cabs: dict                   # NEW
    trains: list[dict]           # NEW

# ------------------- LangGraph -------------------

workflow = StateGraph(GraphState)
workflow.add_node("generate_itinerary", generate_itinerary.generate_itinerary)
workflow.add_node("recommend_activities", recommend_activities.recommend_activities)
workflow.add_node("fetch_useful_links", fetch_useful_links.fetch_useful_links)
workflow.add_node("weather_forecaster", weather_forecaster.weather_forecaster)
workflow.add_node("packing_list_generator", packing_list_generator.packing_list_generator)
workflow.add_node("food_culture_recommender", food_culture_recommender.food_culture_recommender)
workflow.add_node("chat", chat_agent.chat_node)
workflow.set_entry_point("generate_itinerary")
workflow.add_edge("generate_itinerary", END)
workflow.add_edge("recommend_activities", END)
workflow.add_edge("fetch_useful_links", END)
workflow.add_edge("weather_forecaster", END)
workflow.add_edge("packing_list_generator", END)
workflow.add_edge("food_culture_recommender", END)
workflow.add_edge("chat", END)
graph = workflow.compile()

# ------------------- UI -------------------

st.markdown("# 🧳 AI-Powered Travel Itinerary Planner")

if "state" not in st.session_state:
    st.session_state.state = {
        "preferences_text": "",
        "preferences": {},
        "itinerary": "",
        "activity_suggestions": "",
        "useful_links": [],
        "weather_forecast": "",
        "packing_list": "",
        "food_culture_info": "",
        "chat_history": [],
        "user_question": "",
        "chat_response": "",
        "hotels": [],
        "cabs": {},
        "trains": []
    }

with st.form("travel_form"):
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("Destination")
        month = st.selectbox("Month of Travel", [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ])
        duration = st.slider("Number of Days", 1, 30, 7)
        num_people = st.selectbox("Number of People", ["1", "2", "3", "4-6", "7-10", "10+"])
    with col2:
        holiday_type = st.selectbox("Holiday Type", [
            "Any", "Party", "Skiing", "Backpacking", "Family",
            "Beach", "Festival", "Adventure", "City Break",
            "Romantic", "Cruise"
        ])
        budget_type = st.selectbox("Budget Type", [
            "Budget", "Mid-Range", "Luxury", "Backpacker", "Family"
        ])
        comments = st.text_area("Additional Comments")
    submit_btn = st.form_submit_button("Generate Itinerary")

if submit_btn:
    preferences_text = f"Destination: {destination}\nMonth: {month}\nDuration: {duration} days\nPeople: {num_people}\nType: {holiday_type}\nBudget: {budget_type}\nComments: {comments}"
    preferences = {
        "destination": destination,
        "month": month,
        "duration": duration,
        "num_people": num_people,
        "holiday_type": holiday_type,
        "budget_type": budget_type,
        "comments": comments,
    }
    st.session_state.state.update({
        "preferences_text": preferences_text,
        "preferences": preferences,
        "chat_history": [],
        "user_question": "",
        "chat_response": "",
        "activity_suggestions": "",
        "useful_links": [],
        "weather_forecast": "",
        "packing_list": "",
        "food_culture_info": "",
        "hotels": [],
        "cabs": {},
        "trains": []
    })
    with st.spinner("Generating itinerary..."):
        result = graph.invoke(st.session_state.state)
        st.session_state.state.update(result)
        if result.get("itinerary"):
            st.success("Itinerary Created ✅")
        else:
            st.error("Failed to generate itinerary ❌")

# Layout
if st.session_state.state.get("itinerary"):
    col_itin, col_chat = st.columns([3, 2])

    with col_itin:
        st.markdown("### 📍 Travel Itinerary")
        st.markdown(st.session_state.state["itinerary"])

        # Agent buttons
        col_btns = st.columns(8)
        with col_btns[0]:
            if st.button("Activities"):
                with st.spinner("Fetching activities..."):
                    result = recommend_activities.recommend_activities(st.session_state.state)
                    st.session_state.state.update(result)
        with col_btns[1]:
            if st.button("Links"):
                with st.spinner("Fetching links..."):
                    result = fetch_useful_links.fetch_useful_links(st.session_state.state)
                    st.session_state.state.update(result)
        with col_btns[2]:
            if st.button("Weather"):
                with st.spinner("Fetching weather..."):
                    result = weather_forecaster.weather_forecaster(st.session_state.state)
                    st.session_state.state.update(result)
        with col_btns[3]:
            if st.button("Packing"):
                with st.spinner("Generating packing list..."):
                    result = packing_list_generator.packing_list_generator(st.session_state.state)
                    st.session_state.state.update(result)
        with col_btns[4]:
            if st.button("Food & Culture"):
                with st.spinner("Fetching food & culture..."):
                    result = food_culture_recommender.food_culture_recommender(st.session_state.state)
                    st.session_state.state.update(result)
        with col_btns[5]:
            if st.button("Hotels"):
                with st.spinner("Finding hotels..."):
                    result = {"hotels": hotels_finder.invoke({
                        "params": {
                            "q": destination,
                            "check_in_date": "2024-06-22",
                            "check_out_date": "2024-06-28"
                        }
                    })}
                    st.session_state.state.update(result)
        with col_btns[6]:
            if st.button("Cabs"):
                with st.spinner("Finding cabs..."):
                    result = {"cabs": cabs_finder.invoke({
                        "params": {"origin": "Mumbai Airport", "destination": destination}
                    })}
                    st.session_state.state.update(result)
        with col_btns[7]:
            if st.button("Trains"):
                with st.spinner("Finding trains..."):
                    result = {"trains": trains_finder.invoke({
                        "params": {"origin": "Mumbai CST", "destination": destination}
                    })}
                    st.session_state.state.update(result)

        # Expanders
        if st.session_state.state.get("activity_suggestions"):
            with st.expander("🎯 Activities", expanded=False):
                st.markdown(st.session_state.state["activity_suggestions"])
        if st.session_state.state.get("useful_links"):
            with st.expander("🔗 Useful Links", expanded=False):
                for link in st.session_state.state["useful_links"]:
                    st.markdown(f"- [{link['title']}]({link['link']})")
        if st.session_state.state.get("weather_forecast"):
            with st.expander("🌤 Weather", expanded=False):
                st.markdown(st.session_state.state["weather_forecast"])
        if st.session_state.state.get("packing_list"):
            with st.expander("🎒 Packing List", expanded=False):
                st.markdown(st.session_state.state["packing_list"])
        if st.session_state.state.get("food_culture_info"):
            with st.expander("🍽 Food & Culture", expanded=False):
                st.markdown(st.session_state.state["food_culture_info"])
        if st.session_state.state.get("hotels"):
            with st.expander("🏨 Hotels", expanded=False):
                for h in st.session_state.state["hotels"]:
                    st.markdown(f"**{h.get('name','N/A')}** - {h.get('rate_per_night','N/A')} {h.get('currency','')}")
        if st.session_state.state.get("cabs"):
            with st.expander("🚖 Cabs", expanded=False):
                st.json(st.session_state.state["cabs"])
        if st.session_state.state.get("trains"):
            with st.expander("🚆 Trains", expanded=False):
                st.json(st.session_state.state["trains"])

        # Export PDF
        if st.button("Export as PDF"):
            pdf_path = export_to_pdf(st.session_state.state["itinerary"])
            if pdf_path:
                with open(pdf_path, "rb") as f:
                    st.download_button("⬇ Download Itinerary PDF", f, file_name="itinerary.pdf")

    # Chat
    with col_chat:
        st.markdown("### 💬 Chat About Your Trip")
        for chat in st.session_state.state["chat_history"]:
            with st.chat_message("user"):
                st.markdown(chat["question"])
            with st.chat_message("assistant"):
                st.markdown(chat["response"])

        if user_input := st.chat_input("Ask about your itinerary..."):
            st.session_state.state["user_question"] = user_input
            with st.spinner("Thinking..."):
                result = chat_agent.chat_node(st.session_state.state)
                st.session_state.state.update(result)
                st.rerun()
else:
    st.info("👆 Fill the form and generate an itinerary to begin.")
