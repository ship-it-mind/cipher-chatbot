from cryptography.fernet import Fernet

from core.db import crud
from connector.facebook.bot import Bot

from variables import (
    FB_PAGE_ACCESS_TOKEN
)

fb_bot = Bot(FB_PAGE_ACCESS_TOKEN)

def pre_cipher(recipient_id, db):
    user = crud.get_user(db, recipient_id)
    key, key_state = crud.get_user_key(db, recipient_id)
    if key_state == "NEW":
        fb_bot.send_text_message(
            recipient_id,
            "I have created a new key. Keep it Safe!!"
        )
        fb_bot.send_text_message(
            recipient_id,
            key
        )
        fb_bot.send_text_message(
            recipient_id,
            "Now enter the message that you want to keep it safe."
        )
        crud.update_user_state(db, recipient_id, "WAIT_MESSAGE_CIPHER")
    elif key_state == "OLD":
        fb_bot.send_quick_replies(
        recipient_id,
        "It seems that you have an already generated key, Do you want to keep using it?",
        [
            {
                "content_type": 'text',
                "title": 'Yes',
                "payload": 'yes'
            },
            {
                "content_type": 'text',
                "title": 'No',
                "payload": 'no'
            }
        ]
    )
        crud.update_user_last_intent(db, recipient_id, "CONFIRM_USING_OLD_KEY")

def reset_user_state(recipient_id, db):
    crud.update_user_state(db, recipient_id, "CONTINUE")

def send_error(recipient_id, db):
    fb_bot.send_text_message(
            recipient_id,
            "Error"
        )

def generate_key(recipient_id, db):
    user = crud.get_user(db, recipient_id)
    key = crud.create_user_key(db, recipient_id)
    fb_bot.send_text_message(
        recipient_id,
        "I have created a new key. Keep it Safe!!"
    )
    fb_bot.send_text_message(
        recipient_id,
        key.key
    )
    fb_bot.send_text_message(
        recipient_id,
        "Now enter the message that you want to keep it safe."
    )
    crud.update_user_state(db, recipient_id, "WAIT_MESSAGE_CIPHER")

def confirm_pre_cipher(recipient_id, db):
    user = crud.get_user(db, recipient_id)
    fb_bot.send_text_message(
        recipient_id,
        "Great. Now enter the message that you want to keep safe."
    )
    crud.update_user_state(db, recipient_id, "WAIT_MESSAGE_CIPHER")

def confirm_pre_decipher(recipient_id, db):
    fb_bot.send_text_message(
        recipient_id,
        "Now enter the message that you want to decrypt."
    )
    crud.update_user_state(db, recipient_id, "WAIT_MESSAGE_DECIFER")

def cipher(message, recipient_id, db):
    key, _ = crud.get_user_key(db, recipient_id)
    key = key.encode()
    message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(message).decode()
    fb_bot.send_text_message(
        recipient_id,
        "This is the encrypted message. It'll only be decrypted using the key that you used"
    )
    fb_bot.send_text_message(
        recipient_id,
        encrypted_message
    )
    fb_bot.send_quick_replies(
        recipient_id,
        "Do you want to encrypt anything else?",
        [
            {
                "content_type": 'text',
                "title": 'Yes',
                "payload": 'yes'
            },
            {
                "content_type": 'text',
                "title": 'No',
                "payload": 'no'
            }
        ]
    )
    crud.update_user_last_intent(db, recipient_id, "CONFIRM_CIPHER_AGAIN")
    crud.update_user_state(db, recipient_id, "CONTINUE")

def pre_decipher_key(recipient_id, db):
    user = crud.get_user(db, recipient_id)
    fb_bot.send_text_message(
        recipient_id,
        "Please enter the key that have been shared with you to decrypt the message"
    )
    crud.update_user_state(db, recipient_id, "WAIT_KEY")

def pre_decipher_message(message, recipient_id, db):
    user = crud.get_user(db, recipient_id)
    try:
        crud.update_user_last_used_key(db, recipient_id, message)
        fb_bot.send_text_message(
            recipient_id,
            "Now enter the message that you want to decrypt."
        )
        crud.update_user_state(db, recipient_id, "WAIT_MESSAGE_DECIFER")
    except Exception:
        fb_bot.send_text_message(
            recipient_id,
            "The key you've entered is not valid. Please make sure you have the correct key"
        )

def decipher(message, recipient_id, db):
    try:
        user = crud.get_user(db, recipient_id)
        key = user.last_used_key
        key = key.encode()
        message = message.encode()
        f = Fernet(key)
        decrypted_message = f.decrypt(message)
        fb_bot.send_text_message(
            recipient_id,
            "This is the decrypted message. Keep it safe and delete after you read it."
        )
        fb_bot.send_text_message(
            recipient_id,
            decrypted_message.decode()
        )
        fb_bot.send_quick_replies(
        recipient_id,
        "Do you want to decrypt anything else?",
        [
            {
                "content_type": 'text',
                "title": 'Yes',
                "payload": 'yes'
            },
            {
                "content_type": 'text',
                "title": 'No',
                "payload": 'no'
            }
        ]
    )
        crud.update_user_last_intent(db, recipient_id, "CONFIRM_DECIPHER_AGAIN")
        crud.update_user_state(db, recipient_id, "CONTINUE")
    except Exception:
        fb_bot.send_text_message(
            recipient_id,
            "The encrypted message you've entered is not valid. Please make sure you have the correct message"
        )
