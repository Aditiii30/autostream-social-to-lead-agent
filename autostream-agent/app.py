import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from agent.intent import detect_intent
from agent.rag import retrieve_answer
from agent.state import AgentState
from agent.tools import mock_lead_capture
from utils.llm import get_llm


AGENT_NAME = "Inflx Assistant"

state = AgentState()
llm = get_llm()

print(f"{AGENT_NAME} started and ready to help 🚀")
print(f"{AGENT_NAME}: Hey! How can I help you?")

while True:
    user_input = input("User: ")

    intent = detect_intent(user_input)
    state.intent = intent

    # -------- GREETING --------
    if intent == "greeting":
        print(f"{AGENT_NAME}: Hello! How can I help you?")

    # -------- PRICING --------
    elif intent == "product_inquiry":
        response = retrieve_answer(user_input)
        print(f"{AGENT_NAME}:\n{response}")

    # -------- USER CONFIRMED INTEREST --------
    elif intent == "confirmation":
        state.awaiting_plan_choice = True
        print(
            f"{AGENT_NAME}: Great! Which plan would you like to try — "
            "Basic or Pro?"
        )

    # -------- PLAN CHOICE AFTER CONFIRMATION --------
    elif state.awaiting_plan_choice and intent == "high_intent":
        state.awaiting_plan_choice = False

        if not state.name:
            state.name = input(f"{AGENT_NAME}: Your name? ")
        if not state.email:
            state.email = input(f"{AGENT_NAME}: Your email? ")
        if not state.platform:
            state.platform = input(
                f"{AGENT_NAME}: Which platform do you use? "
            )

        if state.is_lead_ready():
            mock_lead_capture(
                state.name, state.email, state.platform
            )
            print(
                f"{AGENT_NAME}: Thank you, {state.name}! 🎉\n"
                "Your details have been recorded successfully.\n"
                "Our team will reach out to you shortly.\n"
                "Have a great day 😊"
            )
            break

    # -------- DIRECT HIGH INTENT --------
    elif intent == "high_intent":
        if not state.name:
            state.name = input(f"{AGENT_NAME}: Your name? ")
        if not state.email:
            state.email = input(f"{AGENT_NAME}: Your email? ")
        if not state.platform:
            state.platform = input(
                f"{AGENT_NAME}: Which platform do you use? "
            )

        if state.is_lead_ready():
            mock_lead_capture(
                state.name, state.email, state.platform
            )
            print(
                f"{AGENT_NAME}: Thank you, {state.name}! 🎉\n"
                "Your details have been recorded successfully.\n"
                "Our team will reach out to you shortly.\n"
                "Have a great day 😊"
            )
            break

    # -------- GOODBYE --------
    elif intent == "goodbye":
        print(f"{AGENT_NAME}: Thank you! Have a great day 😊")
        break

    # -------- FALLBACK --------
    else:
        prompt = (
            f"You are {AGENT_NAME}, a polite AI assistant for a SaaS product "
            "called AutoStream. You should ONLY help with pricing, plans, "
            "or getting started. If the question is unrelated, politely "
            "redirect the user.\n\n"
            f"User: {user_input}\n"
            f"{AGENT_NAME}:"
        )

        try:
            response = llm.invoke(prompt)
            print(f"{AGENT_NAME}: {response.content}")
        except Exception:
            print(
                f"{AGENT_NAME}: I can help you with AutoStream pricing, plans, "
                "or getting started. Let me know how I can assist 😊"
            )
