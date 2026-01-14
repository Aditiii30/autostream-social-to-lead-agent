class AgentState:
    def __init__(self):
        self.intent = None
        self.name = None
        self.email = None
        self.platform = None
        self.awaiting_plan_choice = False

    def is_lead_ready(self):
        return self.name and self.email and self.platform
