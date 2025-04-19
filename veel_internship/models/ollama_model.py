import logging
# import coloredlogs
def setup_logging(level='INFO'):
    """Set up basic colored logging."""
    logger = logging.getLogger()
    # coloredlogs.install(level=level, logger=logger, fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s')

import ollama
from typing import List
from veel_internship.schemas.pydantic_schema import Responserecipe

class OllamaModel:
    def __init__(self, model_name: str = "qwen"):
        self.model_name = model_name

    def _build_messages(self, food_name: str) -> List[dict]:
        return [
            {
                "role": "system",
                "content": "You are a helpful assistant that returns recipes in structured JSON format. ",
            },
            {
                "role": "user",
                "content": f"Generate a recipe for {food_name} and return it in JSON format only. No extra text or emojis.",
            }
        ]

    def streaming(self, food_name: str) -> str:
        full_response = ""
        try:
            for chunk in ollama.chat( #for response= ollama.chat, for chunk in resposne
                
                model=self.model_name,
                messages=self._build_messages(food_name),
                stream=True
            ):
                part = chunk.get("message", {}).get("content", "")
                full_response += part
                print(part, end="", flush=True)  # Optional: live print while streaming
        except Exception as e:
            print(f"Streaming failed: {e}")
        return full_response.strip()

    def structured_output(self, food_name: str, stream: bool = False) -> str:
        try:
            if stream:
                return self.streaming(food_name)
            else:
                response = ollama.chat(
                    model=self.model_name,
                    messages=self._build_messages(food_name),
                    stream=False
                )
                return response["message"]["content"].strip()
        except Exception as e:
            print(f"Error while calling Ollama: {e}")
            return "Error generating response from Ollama."
