import json
import logging

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from utils.streamming import stream_generator
from veel_internship.configs.logging_config import setup_logging
from veel_internship.models.ollama_model import OllamaModel
from veel_internship.schemas.pydantic_schema import RequestRecipe

app = FastAPI()

setup_logging()
logger = logging.getLogger(__name__)

ollamamodel = OllamaModel(model_name="qwen")


@app.post("/generate-recipe")
async def generate_recipe(req: RequestRecipe):
    input_json = req.dict()
    stream = False  # Set to True if you want to enable streaming

    if stream:
        logger.info("Streaming mode enabled for recipe generation.")
        generator = stream_generator(ollamamodel, input_json)
        return StreamingResponse(generator, media_type="text/plain")
    else:
        logger.info("Structured output mode enabled for recipe generation.")
        response_text = ollamamodel.structured_output(input_json)
        logger.info(f"Response Text: {response_text}")
        
        try:
            # Try to dump as JSON if it's a valid dict-string
            parsed = json.loads(response_text)
            logger.info(f"Pretty JSON:\n{json.dumps(parsed, indent=2)}")
        except Exception:
            logger.debug("Response is not JSON serializable for pretty-printing.")

        return response_text
