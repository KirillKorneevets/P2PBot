import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from src.route import api


app = FastAPI(title='P2PBot')

origins = ["http://localhost:8005"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api.router)



if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8005, log_level="info", reload=True)
