import os
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from Alice.server.utils import *
from Alice.server.database import *
from prompt_injection import *

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
PORT = int(os.getenv('PORT', 7000))

client = MongoClient(MONGODB_URI, PORT)
qnaCollection = client.ALICE_MEMORY.qna
qnaBackupCollection = client.ALICE_MEMORY.backupQna

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatbotData(BaseModel):
    user_phone_number_Value: int
    user_nickname_Value: str
    user_middle_name_Value: str
    userAddressValue: str
    userBirthdateValue: str
    user_family_name_Value: str
    usergenderValue: str
    user_given_name_value: str
    user_locale_Value: str
    persona: str
    userName: str
    userEmail: str
    task: str
    external_data: str
    conversation: str
    query: str
    instructions: str
    user_email_verified_Value: bool
    memory_use: bool = True
    latest_data: bool = False

class DavinciData(BaseModel):
    prompt: str

@app.get("/")
async def homepage(request: Request):
    return {"connection": "connected"}

@app.post("/chatbot")
@limiter.limit("20/minute")
async def chatbot(data: ChatbotData, request: Request, response: Response):
    main_instructions = """
    1. You must act and Pretend as Persona specified above.
    2. If web results are provided then you can reference all the web result to come up with one single perfect response.
    3. If the user has provided any data, then you have to consider and reference them before coming up with one single perfect response.
    """
    prompt = prompt_injection(
        data.persona,
        main_instructions,
        data.userName,
        data.instructions,
        data.task,
        data.external_data,
        data.conversation,
        data.query,
        data.memory_use,
        data.latest_data,
    )
    max_tokens = calculate_response_token(4000, prompt)
    response_text = davinciCompletion(
        prompt,
        temperature=0.5,
        max_tokens=int(max_tokens),
        top_p=0.5,
        n=1,
        frequency_penalty=0.5,
        presence_penalty=1.0,
        logprobs=10,
        stream=False,
        model="text-davinci-003",
    )

    qnaData = {
        "user_phone_number_Value": data.user_phone_number_Value,
        "user_nickname_Value": data.user_nickname_Value.lower(),
        "user_middle_name_Value": data.user_middle_name_Value.lower(),
        "userAddressValue": data.userAddressValue.lower(),
        "userBirthdateValue": data.userBirthdateValue.lower(),
        "user_family_name_Value": data.user_family_name_Value.lower(),
        "user_email_verified_Value": data.user_email_verified_Value,
        "usergenderValue": data.usergenderValue.lower(),
        "user_given_name_value": data.user_given_name_value.lower(),
        "user_locale_Value": data.user_locale_Value,
        "userEmail": data.userEmail.lower(),
        "userName": data.userName.lower(),
        "persona": data.persona,
        "task": data.task,
        "external_data": data.external_data,
        "instructions": data.instructions,
        "conversation": data.conversation,
        "query": data.query,
        "response": response_text,
    }

    insert_doc(qnaBackupCollection, qnaData)
    insert_doc(qnaCollection, qnaData)

    response = JSONResponse(
        content={"prompt": prompt, "message": response_text, "response_token": max_tokens}
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.post("/davinci")
@limiter.limit("20/minute")
async def davinci(data: DavinciData, request: Request, response: Response):
    response_text = davinciCompletion(
        data.prompt,
        temperature=0.0,
        max_tokens=700,
        top_p=1.0,
        n=1,
        frequency_penalty=1.5,
        presence_penalty=2.0,
        logprobs=10,
        model="text-davinci-003",
    )
    return response_text
