from wit import Wit

class NLPEngine:
    def __init__(self):
        self.engine = Wit("FQYILCTR5WYC7VZNAT4M5WDM7D5ZECYD")

    def predict(self, message):
        response = self.engine.message(message)
        print(response)
        try:
            intent = response["intents"][0]["name"]
        except:
            intent = "fallback"

        return intent
