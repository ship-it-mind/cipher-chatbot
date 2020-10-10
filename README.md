# Build a Message Encryptor/Decryptor Chatbot on Messenger using Wit.ai, Messenger, FastAPI

## Overview
In this tutorial, we are going to learn what is wit and how can we use it to build a smart chatbot that can understand us and help us encrypt and decrypt messages using a secret key to help you transfer encrypted messages with your friends safely.

So these are the key points that we will cover:
*   Introduction about the tools used
*   Design the user interaction and cover the basic scenarios
*   Create and train a Wit app to do natural language processing (NLP)
*   Create a Facebook Page and Facebook App to host the chatbot
*   Create Web Application using FastAPI and Integrate with Messenger and Wit 
*   Deploy the Web Application using ngrok

## Prerequisites
*   Create a [Wit.ai](https://wit.ai/) account
*   Familiar with Python Programming
*   Familiar with Backend Development

## Introduction about the tools used
In this tutorial, We will create a chatbot on Messenger that will help users encrypt messages using a pre-generated key so they can share the encrypted message with their friends who will decrypt this message using the same pre-generated key. So we will start by giving a simple introduction to the frameworks and APIs we are going to use.

### Wit.ai
Wit is a natural language processing engine, It helps understand text and extract entities. And it makes the process of creating bots or apps that talk to people easier. In the scope of this project, we will use wit to understand the messages that will be sent by our users.

### FastAPI
FastAPI is a modern, fast (high-performance), web framework for building APIs. It’s very fast, intuitive, and easy to use. And it provides automatic swagger docs (Yaaaaay). 

## Design the user interaction and cover the basic scenarios

This is usually the most important step in building a chatbot because it has a big impact on the user experience with the chatbot. So this step needs to be every revisited every now and then to ensure a good conversation flow and experience. In this tutorial we will not focus on this part and we will use a basic conversation flow like below.


First Time Encrypting Scenario
```
Bot:  "Hi John, I'm Lockey. I can encrypt and decrypt messages for you to keep your secrets. What can I do for you?"

User: "I want to encrypt a message"

Bot:  "I have created a new key. Keep it Safe!!"

Bot:  "tkDJnol2UKThgJ_R8wVKVAl_iGwOoywvo45gXWD4v6c="

Bot:  "Now enter the message that you want to keep safe."

User: "I love you Lockey"

Bot:  "This is the encrypted message. It'll only be decrypted using the key that you used"

Bot: "gAAAAABfcNeVsjnOLuz0FuWCPZSNwuun2Emb4kmekRWDE9_Wh4mgqxPioS5zd86KdsI-ubTHD0wS1SdKJjRPhy04kmgbJbQizg=="

Bot:  "Do you want to encrypt anything else?"
```

Next Time Encrypting Scenario
```
Bot:  "Hi John, I'm Lockey. I can encrypt and decrypt messages for you to keep your secrets. What can I do for you?"

User: "I want to encrypt a message"

Bot:  "It seems that you have an already generated key, Do you want to keep using it?"

User:  "Yes"

Bot:  "Great. Now enter the message that you want to keep safe."

User: "I love you Lockey"

Bot:  "This is the encrypted message. It'll only be decrypted using the key that you used"

Bot: "gAAAAABfcNeVsjnOLuz0FuWCPZSNwuun2Emb4kmekRWDE9_Wh4mgqxPioS5zd86KdsI-ubTHD0wS1SdKJjRPhy04kmgbJbQizg=="

Bot:  "Do you want to encrypt anything else?"
```

Decrypting Scenario
```
Bot:  "Hi John, I'm Lockey. I can encrypt and decrypt messages for you to keep your secrets. What can I do for you?"

User: "I want to decrypt a message"

Bot:  "Please enter the key that has been shared with you to decrypt the message"

User:  "tkDJnol2UKThgJ_R8wVKVAl_iGwOoywvo45gXWD4v6c="

Bot:  "Now enter the message that you want to decrypt."

User: "gAAAAABfcNeVsjnOLuz0FuWCPZSNwuun2Emb4kmekRWDE9_Wh4mgqxPioS5zd86KdsI-ubTHD0wS1SdKJjRPhy04kmgbJbQizg=="

Bot:  "This is the decrypted message. Keep it safe and delete after you read it."

Bot:  "I love you Lockey"

Bot: "Do you want to decrypt anything else?"
```

## Create and train a Wit app to do natural language processing

* Create a new Wit App
    * Choose the name of your app
    * Choose the language of the app **English**
    * Choose whether you want the app **Open** or **Private**
    * Click **Import** if you have a previous wit app or if you want to export the wit app used in this tutorial press [here](https://storage.googleapis.com/iam-sultan/cipher-bot-2020-10-03-07-00-12.zip)
    * Click **Create**

![Create App](assets/create-app.png)

* We will be redirected to the understanding page where we will enter utterances or training data. And you'll notice that for every utterance we enter we will need to specify the intent of that utterance (Or create the intent in case if it doesn't exist) And after every utterance click on **Train and Validate**.

![Add utterance and create intent](assets/create-intent.png)

* You'll notice that over time Wit will automatically match the utterances that you enter with the correct intent and that indicates that we are on the right path.

![Auto detect intent](assets/auto-detect-intent.png)

* We will keep entering data and creating intents. We will mainly use 6 intents:
    * `greeting`
    * `cipher`
    * `decipher`
    * `new_key`
    * `yes`
    * `no`

* We can find all the utterances in the utterances page.

* We can also test the Wit App using a curl request that is generated automatically by going to the **Settings** page

![Auto predict intent](assets/test-api.png)

* In the same page we can get the **Server Access Token** as we will use it later when we build the app

![Get Server Access Token](assets/app-settings_censored.jpg)

## Create a Facebook Page and Facebook App to host the chatbot

For this part, we are going to create two things:

### 1. Facebook Page

* Go to this [page](https://www.facebook.com/pages/creation/?ref_type=comet_home) to start the process of creating the new page
* Then choose your page name and category and click on the create button (And yes that's it you now have a page)

![Create Facebook page](assets/create-page-1.png)

### 2. Facebook App

* Go to [Facebook for Developers](https://developers.facebook.com/) and create an account if you don't have one and click on the **Create App** Button
* Choose **Manage Business Integrations**

![Create App and choose category](assets/create-developer-app.png)

* Fill the required information and click on the **Create App ID**

![Create App](assets/create-fb-app-3.png)

* Then from the list of products shown, Click on **Set Up** on the Messenger card

![Create App](assets/create-fb-app-4.png)

* In the **Access Tokens** Section, Click on the **Add or Remove Pages** Button and choose the page that we created earlier and agree on the permissions needed.

![Create App](assets/create-fb-app-5.png)

* Then click on the **Generate Token** Button and keep the generated token safe as we will use it later.

![Create App](assets/create-fb-app-6.png)

## Create Web Application using FastAPI and Integrate with Messenger and Wit 

This section illustrates how can you use this repo to build the chatbot on your own page. You can find the source code in this [repo](https://github.com/Ahmed0Sultan/cipher-chatbot) so download it and follow these steps.

### Clone Project Repository

```
$ git clone https://github.com/Ahmed0Sultan/cipher-chatbot.git
$ cd cipher-chatbot
```

### This is a tree that demonestrates the files and directories in the project.

```
└── cipher-chatbot
    ├── api
    │   ├── api.py
    │   └── endpoints
    │       └── facebook.py
    ├── connector
    │   └── facebook
    │       ├── bot.py
    │       └── utils.py
    ├── core
    │   ├── db
    │   │   ├── crud.py
    │   │   ├── database.py
    │   │   └── models.py
    │   ├── dialog
    │   │   ├── actions.py
    │   │   ├── manager.py
    │   │   └── responses.py
    │   └── nlp
    │       └── engine.py
    ├── LICENSE
    ├── main.py
    ├── README.md
    ├── requirements.txt
    └── variables.py
```

### Create and Activate a Virtual Environment

```
$ python -m venv venv
$ source ./venv/bin/activate
```

### Install Requirements

```
$ pip install -r requirements.txt
```

### Set Environment Variables
Create a new file named `.env` which will contain the secret tokens that we will use to integrate with Wit and Messenger (That we have already got in earlier steps)

```env
FB_PAGE_ACCESS_TOKEN="Very_Secret_Token"
FB_VERIFY_TOKEN="Very_Secret_Token"
WIT_SERVER_TOKEN="Very_Secret_Token"
```

### Introduction to Fernet
So Fernet is a system for symmetric encryption/decryption. It also authenticates the message, which means that the recipient can tell if the message has been altered in any way from what was originally sent.

And we can find examples to use it below

#### Create a key
```python
from cryptography.fernet import Fernet

key = Fernet.generate_key()
```
#### Encrypting a message
```python
cipher = Fernet(key)

message = "Very Secret Message".encode('utf-8')
encrypted_message = cipher.encrypt(message)
```
#### Decrypting a message
```python
cipher = Fernet(key)

decrypted_message = cipher.decrypt(encrypted_message)
```

### Explore the DB Models in Our App

In [`core/db/database.py`](https://github.com/Ahmed0Sultan/cipher-chatbot/blob/master/core/db/database.py) , We can find that we create an instance of the DB and then create a session that we will use to do all the CRUD operations needed.

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./cipher_bot.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

Then in [`core/db/models.py`](https://github.com/Ahmed0Sultan/cipher-chatbot/blob/master/core/db/models.py), We will find the models that will be used through the app which will be translated into database tables.

```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from cryptography.fernet import Fernet

from core.db.database import Base


class User(Base):
    __tablename__ = "users"

    fb_id = Column(String, primary_key=True, unique=True, index=True)
    last_intent = Column(String)
    state = Column(String)
    last_used_key = Column(String)

    keys = relationship("Key", back_populates="owner")


class Key(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, default=Fernet.generate_key().decode())
    owner_id = Column(Integer, ForeignKey("users.fb_id"))

    owner = relationship("User", back_populates="keys")
```
So here we have two models (`User`, `Key`). 
* `User` Model
  * We can see that we use the `fb_id` as a primary key where we will save the ID of the user that we get from the Messenger API
  * `last_intent` will contain the last intent identified by Wit so that we can handle the context of the conversation
  * `state` will contain a predefined state that we will later map to a specific action
  * `last_used_key` will contain the last key that was used by the user to make it easy for the user to reuse a key that was generated before
* `Key` Model
  * `id` will contain an auto generated primary key 
  * `key` will contain the key that was generated to encrypt and decrypt and its default value will be a key generated like illustrated above
  *  `owner_id` a foreign key that will link the key generated to the user by using the `fb_id`

And in [`core/db/crud.py`](https://github.com/Ahmed0Sultan/cipher-chatbot/blob/master/core/db/crud.py) we will find all the CRUD (Create, Read, Update, Delete) operations that we are going to use like (creating a new user, checking if user exists, creating a new key, or updating a user state)

### Using Wit.ai in Our App
In [`core/nlp`](https://github.com/Ahmed0Sultan/cipher-chatbot/tree/master/core/nlp) directory, We can find the [`engine.py`](https://github.com/Ahmed0Sultan/cipher-chatbot/blob/master/core/nlp/engine.py) file as below
```python
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
```
In this file we create a class where we initialize an instance of `Wit` class with a server token that we get from the envrionment variables. Then we create a prediction function which takes a text message as an input and we try to extract the recognized intent from the response or return the fallback intent in the of nothing found

### Using Messenger APIs in Our App
To handle sending messages and other Messenger API calls we use the code in [Pymessenger](https://github.com/davidchua/pymessenger) library and modify it to have additional functionalities like sending messages with quick replies. You can find the modified code in [`connector/facebook/bot.py`](https://github.com/Ahmed0Sultan/cipher-chatbot/blob/master/connector/facebook/bot.py) and the [Messenger API Docs](https://developers.facebook.com/docs/messenger-platform).

In [`core/dialog`](https://github.com/Ahmed0Sultan/cipher-chatbot/tree/master/core/dialog) directory we will find two files:

* [`actions.py`](https://github.com/Ahmed0Sultan/cipher-chatbot/blob/master/core/dialog/actions.py)

    In this file, We will create the functions that will trigger the CRUD operations fucntion in `core/db/crud.py` file, and will also trigger the Messenger API functions in `connector/facebook/bot.py`.

* [`manager.py`](https://github.com/Ahmed0Sultan/cipher-chatbot/blob/master/core/dialog/manager.py)

    In this file, We will trigger the actions that we created based on the user current state, last intent, and the current intent identified by Wit.


### Our API Routes
So for our application to send and recieve requests it has to have routes. We can find the routes of the app in the [`api`](https://github.com/Ahmed0Sultan/cipher-chatbot/tree/master/api) directory. Let's start with the [`api/endpoints/facebook.py`](https://github.com/Ahmed0Sultan/cipher-chatbot/blob/master/api/endpoints/facebook.py) file, which is the only route we have.
```python
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
```
So the route name is `/facebook-webhook` and it has two methods:
* `GET`

    So the `GET` method is used to verify the bot’s token and thus connect the app with facebook messenger.

* `POST`

    The `POST` method is used by facebook to send the messages that are sent by users to our web application. And we can find here that we handle two types of messages normal text `message` and a `postback` message.

Then we import all the routes (Which in our case is only one) into another file [`api/api.py`](https://github.com/Ahmed0Sultan/cipher-chatbot/blob/master/api/api.py) which in turn gathers all the available routes under one instance of the `APIRouter` class.
```python
from fastapi import APIRouter

from api.endpoints import facebook

api_router = APIRouter()
api_router.include_router(facebook.router, tags=["verify_token"])
```

### Our Application Entry Point
So After explaining the logic that resides in the application, let's explain how will the app work.

We can find in the [`main.py`](https://github.com/Ahmed0Sultan/cipher-chatbot/blob/master/main.py) file that we initialize an instance of the `FastAPI` class which we will use later to run the app. Then we will import the instance of `APIRouter` that we created before and added to our app.
```python
from fastapi import FastAPI

from api.api import api_router

app = FastAPI()

app.include_router(api_router)
```

### Run Our App

To run the app just enter this command.
```sh
$ uvicorn main:app
```

## Deploy the Web Application using ngrok
