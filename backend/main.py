from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llm_client import review_code_with_llm

app = FastAPI()


class ReviewRequest(BaseModel):
    code: str
    language: str = "python"


class ReviewResponse(BaseModel):
    logic: str
    bugs: str
    optimizations: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/review", response_model=ReviewResponse)
async def review_code(payload: ReviewRequest):
    try:
        result = await review_code_with_llm(
            code=payload.code,
            language=payload.language,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ReviewResponse(**result)