import json
import ollama
from typing import List
from veel_internship.schemas.pydantic_schema import Responserecipe


class OllamaModel:
    def __init__(self, model_name: str = "qwen"):
        self.model_name = model_name

    def structured_output(self, food_name: str, stream: bool = False):
        """
        Generates a structured recipe for the given food name using Ollama.

        Args:
            food_name (str): The name of the food to generate a recipe for.

        Returns:
            Responserecipe: A structured response containing title, ingredients, etc.
        """
        # try:
        #     response = ollama.chat(
        #         model=self.model_name,
        #         messages=[
        #             {
        #                 "role": "system",
        #                 "content": "You are a helpful assistant that returns recipes in structured JSON format.",
        #             },
        #             {
        #                 "role": "user",
        #                 "content": f"Generate a recipe for {food_name} and return it in JSON format:.",
        #             }
        #         ],
        #         stream=True,
        #         format = Responserecipe.model_json_schema(),



        #     )

        #     # content = response['message']['content'].strip()
        #     return response['message']['content'].strip()

        #     # # Ensure it's JSON
        #     # parsed = json.loads(content)
        #     # recipe = Responserecipe(**parsed)  # Validate with Pydantic
        #     # return recipe

        # except json.JSONDecodeError:
        #     print("The model did not return valid JSON.")
        # except Exception as e:
        #     print(f" Error while calling Ollama: {e}")
        
        # return None

        try:
            if stream == True:
                full_response = ""
                for chunk in ollama.chat(
                    model=self.model_name,
                    messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that returns recipes in structured JSON format.",
                    },
                    {
                        "role": "user",
                        "content": f"Generate a recipe for {food_name} and return it in JSON format:.",
                    }
                    ]
                 
                ):
                    part = chunk.get("message", {}).get("content", "")
                    full_response += part
                    print(part, end="", flush=True)  
                return full_response.strip()
            else:
                response = ollama.chat(
                    model=self.model_name,
                     messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that returns recipes in structured JSON format.",
                    },
                    {
                        "role": "user",
                        "content": f"Generate a recipe for {food_name} and return it in JSON format:.",
                    }
                ]
                )
                return response["message"]["content"].strip()

        except Exception as e:
            print(f"Error while calling Ollama: {e}")
            return "Error generating response from Ollama."