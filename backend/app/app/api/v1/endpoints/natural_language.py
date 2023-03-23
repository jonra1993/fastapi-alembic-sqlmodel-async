from fastapi import APIRouter
from app.utils.fastapi_globals import g
from app.schemas.response_schema import IPostResponseBase, create_response

router = APIRouter()


@router.post("/sentiment_analysis")
async def sentiment_analysis_prediction(
    prompt: str = "Fastapi is awesome",
) -> IPostResponseBase:
    """
    Gets a sentimental analysis predition using a NLP model from transformers libray
    """
    sentiment_model = g.sentiment_model
    prediction = sentiment_model(prompt)
    return create_response(message="Prediction got succesfully", data=prediction)


@router.post("/text_generation")
async def text_generation_prediction(
    prompt: str = "Superman is awesome because",
) -> IPostResponseBase:
    """
    Text generation using a NLP model from transformers libray
    """
    text_generator_model = g.text_generator_model
    prediction = text_generator_model(prompt)
    return create_response(message="Prediction got succesfully", data=prediction)
