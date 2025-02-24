import os
from deepseek import DeepSeekClient

class HubSpotClient:
    def __init__(self):
        self.api_key = os.getenv('HUBSPOT_API_KEY')
        # Initialize client

class DeepSeekClientWrapper(DeepSeekClient):
    def __init__(self):
        super().__init__(api_key=os.getenv('DEEPSEEK_API_KEY')) 