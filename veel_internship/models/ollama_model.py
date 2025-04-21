import logging
from configs.logging_config import setup_logging

import ollama
from typing import List
from schemas.pydantic_schema import Responserecipe
from prompts.prompt_templates import SystemPrompts

class OllamaModel:
    def __init__(self, model_name: str = "qwen", temperature: float = 0.5):
        self.model_name = model_name
        self.temperature = temperature  # fixed attribute name

    def _build_messages(self, food_name: str) -> List[dict]:
        return [
            {
                "role": "system",
                "content": SystemPrompts.OLLAMA_PROMPT.strip(),
            },
            {
               "role": "user",
            "content": f"Please generate a recipe for the following:\n"
                       f"Food Name: {food_name['Food_Name']}\n"
                       
                       f"Ingredients: {', '.join(food_name['Ingredients'])}",

            }
        ]

    def streaming(self, food_name: str) -> str:
        response = ollama.chat
        full_response = ""  # Initialize the variable before using it

        try:
            for chunk in response(
                model=self.model_name,
                messages=self._build_messages(food_name),
                stream=True
            ):
                part = chunk.get("message", {}).get("content", "")
                full_response += part
                print(part, end="", flush=True)
        except Exception as e:
            print(f"Streaming failed: {e}")
            return "Error during streaming."

        return full_response.strip()

    def structured_output(self, food_name: str) -> str:
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=self._build_messages(food_name),
                temperature=self.temperature,
                stream=False,
            )
            return response["message"]["content"].strip()
        except Exception as e:
            print(f"Error while calling Ollama: {e}")
            return "Error generating response from Ollama."
