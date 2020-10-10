from wit import Wit

from variables import WIT_SERVER_TOKEN

class NLPEngine:
    def __init__(self):
        self.engine = Wit(WIT_SERVER_TOKEN)

    def predict(self, message):
        response = self.engine.message(message)
        try:
            intent = response["intents"][0]["name"]
        except:
            intent = "fallback"

        return intent
