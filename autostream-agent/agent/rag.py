import json

def load_knowledge():
    with open("data/knowledge_base.json", "r") as f:
        return json.load(f)

def retrieve_answer(query):
    kb = load_knowledge()

    pricing = kb["pricing"]

    response = (
        "Here are our pricing plans:\n\n"
        f"🔹 Basic Plan – {pricing['basic']['price']}\n"
        f"   • {pricing['basic']['videos']}\n"
        f"   • {pricing['basic']['resolution']} resolution\n\n"
        f"🔹 Pro Plan – {pricing['pro']['price']}\n"
        f"   • {pricing['pro']['videos']}\n"
        f"   • {pricing['pro']['resolution']} resolution\n"
        f"   • AI captions\n\n"
        "Let me know if you'd like to try any plan 😊"
    )

    return response

