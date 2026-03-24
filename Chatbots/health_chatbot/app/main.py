from fastapi import FastAPI
from app.api.routes import router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "UHC Chatbot API is running"}

# Import router ONLY
app.include_router(router)
