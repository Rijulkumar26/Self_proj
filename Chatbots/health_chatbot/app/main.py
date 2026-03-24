from fastapi import FastAPI
import threading

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API running"}


def preload():
    from app.services.retriever import load_resources
    print(" Preloading...")
    load_resources()
    print(" Done")


# NON-BLOCKING
threading.Thread(target=preload).start()


from app.api.routes import router
app.include_router(router)
