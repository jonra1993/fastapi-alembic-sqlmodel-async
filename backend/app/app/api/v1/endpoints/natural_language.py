from datetime import datetime, timedelta
from app.api.celery_task import predict_transformers_pipeline
from fastapi import APIRouter, HTTPException
from app.utils.fastapi_globals import g
from app.schemas.response_schema import IPostResponseBase, create_response
from app.core.celery import celery

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
    Sync text generation using a NLP model from transformers libray (Not reommended for long time inferences)
    """
    text_generator_model = g.text_generator_model
    prediction = text_generator_model(prompt)
    return create_response(message="Prediction got succesfully", data=prediction)


@router.post("/text_generation_prediction_batch_task")
async def text_generation_prediction_batch_task(
    prompt: str = "Batman is awesome because",
) -> IPostResponseBase:
    """
    Async batch task for text generation using a NLP model from transformers libray
    """
    prection_task = predict_transformers_pipeline.delay(prompt)
    return create_response(
        message="Prediction got succesfully", data={"task_id": prection_task.task_id}
    )


@router.post("/text_generation_prediction_batch_task_after_some_seconds")
async def text_generation_prediction_batch_task_after_some_seconds(
    prompt: str = "Batman is awesome because", seconds: float = 5
) -> IPostResponseBase:
    """
    Async batch task for text generation using a NLP model from transformers libray

    It is executed after x number of seconds
    """
    delay_elapsed = datetime.utcnow() + timedelta(seconds=seconds)
    prection_task = predict_transformers_pipeline.apply_async(
        args=[prompt], eta=delay_elapsed
    )
    return create_response(
        message="Prediction got succesfully", data={"task_id": prection_task.task_id}
    )


@router.get("/get_result_from_batch_task")
async def get_result_from_batch_task(task_id: str) -> IPostResponseBase:
    """
    Get result from batch task using task_id
    """
    async_result = celery.AsyncResult(task_id)

    if async_result.ready():
        if not async_result.successful():
            raise HTTPException(
                status_code=404,
                detail=f"Task {task_id} with state {async_result.state}.",
            )

        result = async_result.get(timeout=1.0)
        return create_response(
            message="Prediction got succesfully",
            data={"task_id": task_id, "result": result},
        )
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} does not exist or is still running.",
        )
