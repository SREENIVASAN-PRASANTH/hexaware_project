import joblib
from fastapi import FastAPI
from pydantic import BaseModel

model = joblib.load("D:/python projects/hexaware project/sentiment_analysis_model/sentiment_model.pkl")

app = FastAPI()

class TextRequest(BaseModel):
    text: str
    
@app.post("/predict_feedback")
def predict_sentiment(request : TextRequest):
    text = request.text
    prediction = model.predict([text])
    
    return {"sentiment" : prediction[0]}




