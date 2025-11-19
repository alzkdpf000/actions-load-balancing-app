# uvicorn main:app --reload
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

app = FastAPI()

origins = [
    "http://crew-stations.shop",
"http://localhost:10000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}




class FeelingCheckRequest(BaseModel):
    message: str


class FeelingCheckResponse(BaseModel):
    result: str




@app.post("/api/feel-check", response_model=FeelingCheckResponse)
async def check_spam(request: FeelingCheckRequest):
    if not request.message.strip():  # 공백만 있어도 빈 문자열로 처리
        raise HTTPException(status_code=422, detail="메시지를 입력해주세요.")
    print(request.message)
    model = joblib.load(f"feeling_model.pkl")
    prediction = model.predict([request.message])[0]
    print(prediction)
    return {"result": str(prediction)}











