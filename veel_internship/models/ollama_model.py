import logging
from typing import List

import ollama
from veel_internship.prompts.prompt_templates import SystemPrompts
from veel_internship.prompts.user_message import UserPrompt
from utils.check_ollama_model import model_exist
from veel_internship.configs.logging_config import setup_logging


setup_logging()
logger = logging.getLogger(__name__)


class OllamaModel:
    def __init__(self, model_name: str = "qwen", temperature: float = 0.5):
        self.model_name = model_name
        self.temperature = temperature

        if not model_exist(self.model_name):
            logger.info(f"Model '{model_name}' not found locally. Attempting to pull.")
            try:
                ollama.pull(model_name)
                logger.info(f"Model '{model_name}' pulled successfully.")
            except Exception as e:
                logger.error(f"Error pulling model '{model_name}': {e}")
                raise

    def _build_messages(self, food_name: dict) -> List[dict]:
        return [
            {
                "role": "system",
                "content": SystemPrompts.structured_output_prompt.strip(),
            },
            {
                "role": "user",
                "content": (
                    f"Generate the recipe:\n"
                    f"Food Name: {food_name['Food_Name']}\n"
                    f"Ingredients: {', '.join(food_name['Ingredients'])}"
                ),
            },
        ]

    def streaming(self, food_name: dict):
        try:
            logger.info("Starting streaming response from LLM.")
            response = ollama.chat(
                model=self.model_name,
                messages=self._build_messages(food_name),
                stream=True,
            )
            for chunk in response:
                part = chunk.get("message", {}).get("content", "")
                if part:
                    yield part
        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            yield "Error during streaming."

    def structured_output(self, food_name: dict) -> str:
        try:
            logger.info("Calling LLM model for structured output.")
            response = ollama.chat(
                model=self.model_name,
                messages=self._build_messages(food_name),
                stream=False,
            )
            content = response.get("message", {}).get("content", "").strip()
            logger.info("Structured response received successfully.")
            return content
        except Exception as e:
            logger.error(f"Error generating response from Ollama: {e}")
            return "Error generating response from Ollama."

    def generate_recipe(self, food_name: dict, stream: bool = False):
        logger.info(f"Generating recipe (stream={stream})")
        if stream:
            return self.streaming(food_name)
        else:
            return self.structured_output(food_name)
