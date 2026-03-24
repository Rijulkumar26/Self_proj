from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}

# Import AFTER app is created
try:
    from app.api.routes import router
    app.include_router(router)
except Exception as e:
    print("ERROR DURING STARTUP:", e)
