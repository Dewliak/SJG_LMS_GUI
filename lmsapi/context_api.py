"""
   This is a singleton class the can be used between clients so it doesn't need to be
    reinitialized multiple times.
"""
class Context:
    def __init__(self, creds: str = "credentials.json", secrets: str = "secrets.json"):
        self.creds = creds
        self.secrets = secrets
