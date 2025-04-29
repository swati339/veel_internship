import logging
from veel_internship.models.ollama_model import OllamaModel

logger = logging.getLogger(__name__)

def stream_generator(ollama_model: OllamaModel, food_name: dict):
    try:
        streaming_response = ollama_model.streaming(food_name)
        for chunk in streaming_response:
            yield chunk
    except Exception as e:
        logger.error(f"Error while streaming recipe: {e}")
        yield "Error occurred during streaming."
