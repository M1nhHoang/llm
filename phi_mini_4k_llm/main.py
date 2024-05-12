from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from llm import LLM_chat

app = FastAPI()
llm_model = LLM_chat()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/chat_stream/")
async def chat_stream(
    question: dict = {"text": ""},
):
    if not question.get("text"):
        return {"error": "text is required"}
    return StreamingResponse(
        llm_model.generate_stream(question.get("text")), media_type="text/event-stream"
    )