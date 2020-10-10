from fastapi import APIRouter, Query, Request, HTTPException, Depends
from sqlalchemy.orm import Session

from core.dialog.manager import DialogManager
from core.db import models
from core.db.database import SessionLocal, engine

from variables import (
    FB_VERIFY_TOKEN
)

models.Base.metadata.create_all(bind=engine)

router = APIRouter()
dialog_manager = DialogManager()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/facebook-webhook')
async def verify_token(token: str = Query(None, alias="hub.verify_token"),
 challenge: int = Query(None, alias="hub.challenge")):
    if token == FB_VERIFY_TOKEN:
        return challenge
    else:
        raise HTTPException(status_code=403, detail="Token invalid.")

@router.post('/facebook-webhook')
async def process_fb_requests(request: Request, db: Session = Depends(get_db)):
    output = await request.json()
    for event in output['entry']:
        messaging = event['messaging']
        for x in messaging:
            if x.get('message'):
                recipient_id = str(x['sender']['id'])
                if x['message'].get('text'):
                    message = x['message']['text']
                    dialog_manager.process_message(
                    message,
                    recipient_id,
                    db)

            elif x.get('postback'):
                recipient_id = str(x['sender']['id'])
                if x['postback'].get('title'):
                    message = x['postback']['title']
                    dialog_manager.process_message(message, 
                    recipient_id,
                    db)
    return "Success"
