import random

from core.nlp.engine import NLPEngine
from core.db import crud
from core.dialog import actions


class DialogManager:
    def __init__(self):
        self.engine = NLPEngine()
        
    def process_message(self, message, recipient_id, db):
        try:
            user_state = crud.get_user_state(db, recipient_id)
            print(user_state)
            if user_state == "CONTINUE":
                intent = self.engine.predict(message)
                print(intent)
                return self.get_response(intent, recipient_id, db)
            elif user_state == "WAIT_MESSAGE_CIPHER":
                actions.cipher(message, recipient_id, db)
                actions.reset_user_state(recipient_id, db)
            elif user_state == "WAIT_MESSAGE_DECIFER":
                actions.decipher(message, recipient_id, db)
                actions.reset_user_state(recipient_id, db)
            elif user_state == "WAIT_KEY":
                actions.confirm_pre_decipher(recipient_id, db)
        except Exception as err:
            print(err)
            actions.send_error(recipient_id, db)
    
    def get_response(self, intent, recipient_id, db):
        last_intent = crud.get_user_last_intent(db, recipient_id)
        if intent == "cipher":
            actions.pre_cipher(recipient_id, db)
        elif intent == "decipher":
            actions.pre_decipher_key(recipient_id, db)
        elif intent == "new_key":
            actions.generate_key(recipient_id, db)
        elif intent == "yes":
            if last_intent == "CONFIRM_USING_OLD_KEY":
                actions.confirm_pre_cipher(recipient_id, db)
            elif last_intent == "CONFIRM_CIPHER_AGAIN":
                actions.confirm_pre_cipher(recipient_id, db)
            elif last_intent == "CONFIRM_DECIPHER_AGAIN":
                actions.pre_decipher_message(recipient_id, db)
        elif intent == "no":
            if last_intent == "CONFIRM_USING_OLD_KEY":
                actions.generate_key(recipient_id, db)
            elif last_intent == "CONFIRM_CIPHER_AGAIN":
                pass
            elif last_intent == "CONFIRM_DECIPHER_AGAIN":
                pass
        else:
            return "Sorry I didn't get that."
