from sqlalchemy.orm import Session

from core.db import models


def create_user(db: Session, user_id: str):
    db_user = models.User(fb_id=user_id, last_intent=None, state="CONTINUE", last_used_key=None)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def user_exist(db: Session, user_id: str):
    user = db.query(models.User).filter(models.User.fb_id == user_id).first()
    if user:
        return user
    else:
        return False


def get_user(db: Session, user_id: str):
    user = user_exist(db, user_id)
    if user is not False:
        return user
    else:
        return create_user(db, user_id)


def get_user_last_intent(db: Session, user_id: str):
    user = get_user(db, user_id)
    return user.last_intent


def update_user_last_intent(db: Session, user_id: str, last_intent: str):
    user = get_user(db, user_id)
    user.last_intent = last_intent
    db.commit()
    return user


def update_user_last_used_key(db: Session, user_id: str, last_used_key: str):
    user = get_user(db, user_id)
    user.last_used_key = last_used_key
    db.commit()
    return user


def update_user_state(db: Session, user_id: str, state: str):
    user = get_user(db, user_id)
    user.state = state
    db.commit()
    return user


def user_key_exists(db: Session, user_id: str):
    user = get_user(db, user_id)
    if len(user.keys) > 0:
        key = user.keys[0]
        return key
    else:
        False


def delete_user_key(db: Session, user_id: str):
    user = get_user(db, user_id)
    if len(user.keys) > 0:
        key = user.keys[0]
        db.delete(key)
        db.commit()


def create_user_key(db: Session, user_id: str):
    delete_user_key(db, user_id)
    db_key = models.Key(owner_id=user_id)
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    return db_key


def get_user_key(db: Session, user_id: str):
    user = get_user(db, user_id)
    if len(user.keys) > 0:
        key = user.keys[0]
        return key.key, "OLD"
    else:
        return create_user_key(db, user_id).key, "NEW"


def get_user_state(db: Session, user_id: str):
    user = get_user(db, user_id)
    if user.state == None:
        return "CONTINUE"
    else:
        return user.state
