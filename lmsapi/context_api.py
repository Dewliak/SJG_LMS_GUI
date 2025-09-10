class Context:
    def __init__(self, creds: str = "credentials.json", secrets: str = "secrets.json"):
        self.creds = creds
        self.secrets = secrets
