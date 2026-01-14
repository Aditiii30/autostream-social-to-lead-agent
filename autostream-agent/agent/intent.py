def detect_intent(user_message):
    msg = user_message.lower().strip()

    # Exit / goodbye
    if msg in ["exit", "quit", "bye", "thanks", "thank you"]:
        return "goodbye"

    # Confirmation
    if msg in ["yes", "yeah", "yep", "sure", "ok", "okay"]:
        return "confirmation"

    # High intent (IMPORTANT FIX HERE)
    if msg in ["basic", "pro", "basic plan", "pro plan"]:
        return "high_intent"

    if any(phrase in msg for phrase in [
        "i want to try",
        "buy",
        "subscribe",
        "sign up",
        "go with",
        "choose"
    ]):
        return "high_intent"

    # Product inquiry (STRICT – no generic 'plan')
    if any(phrase in msg for phrase in [
        "pricing",
        "price",
        "subscription",
        "autostream plans",
        "pricing plans"
    ]):
        return "product_inquiry"

    # Greeting
    if any(word in msg for word in ["hi", "hello", "hey", "hii"]):
        return "greeting"

    return "unknown"
