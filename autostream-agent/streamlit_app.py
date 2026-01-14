# streamlit_app.py
import streamlit as st

from agent.intent import detect_intent
from agent.rag import retrieve_answer
from agent.state import AgentState
from agent.tools import mock_lead_capture
from utils.llm import get_llm

# ---------------- CONFIG ----------------
AGENT_NAME = "Inflx Assistant"
PRODUCT_NAME = "AutoStream"

st.set_page_config(
    page_title="AutoStream AI Agent",
    page_icon="🎬",
    layout="centered"
)

# ---------------- INIT SESSION ----------------
if "state" not in st.session_state:
    st.session_state.state = AgentState()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hey! 👋 How can I help you today?"
        }
    ]

if "llm" not in st.session_state:
    st.session_state.llm = get_llm()

state = st.session_state.state
llm = st.session_state.llm

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align:center;'>🎬 AutoStream</h1>
    <h4 style='text-align:center; color:gray;'>Powered by Inflx Assistant</h4>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["content"])

# ---------------- CHAT INPUT ----------------
user_input = st.chat_input("Ask about pricing, plans, or getting started…")

if user_input:
    # Add user message (RIGHT side)
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    intent = detect_intent(user_input)
    state.intent = intent

    # -------- GREETING --------
    if intent == "greeting":
        reply = "Hello! 😊 How can I help you?"

    # -------- PRICING --------
    elif intent == "product_inquiry":
        reply = retrieve_answer(user_input)

    # -------- CONFIRMATION --------
    elif intent == "confirmation":
        state.awaiting_plan_choice = True
        reply = "Great! Which plan would you like to try — **Basic** or **Pro**?"

    # -------- PLAN CHOICE --------
    elif state.awaiting_plan_choice and intent == "high_intent":
        state.awaiting_plan_choice = False
        state.lead_step = "name"
        reply = "Perfect! Let’s get you started 😊\n\nWhat’s your **name**?"

    # -------- LEAD CAPTURE STEPS --------
    elif state.lead_step == "name":
        state.name = user_input
        state.lead_step = "email"
        reply = "Thanks! What’s your **email address**? 📧"

    elif state.lead_step == "email":
        state.email = user_input
        state.lead_step = "platform"
        reply = "Got it 👍 Which platform do you use? (Instagram / WhatsApp / YouTube)"

    elif state.lead_step == "platform":
        state.platform = user_input
        mock_lead_capture(state.name, state.email, state.platform)
        state.lead_step = None
        reply = (
            f"Thank you, **{state.name}** 🎉\n\n"
            "Your details have been recorded successfully.\n"
            "Our team will reach out to you shortly.\n\n"
            "Have a great day 😊"
        )

    # -------- GOODBYE --------
    elif intent == "goodbye":
        reply = "Thank you for visiting AutoStream 😊 Have a great day!"

    # -------- FALLBACK --------
    else:
        prompt = (
            f"You are {AGENT_NAME}, a polite AI assistant for a SaaS product called {PRODUCT_NAME}. "
            "You should ONLY help with pricing, plans, or getting started. "
            "If the question is unrelated, politely redirect the user.\n\n"
            f"User: {user_input}\n{AGENT_NAME}:"
        )
        try:
            response = llm.invoke(prompt)
            reply = response.content
        except Exception:
            reply = (
                "I can help you with AutoStream pricing, plans, or getting started. "
                "Let me know how I can assist 😊"
            )

    # Add assistant message (LEFT side)
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    st.rerun()
