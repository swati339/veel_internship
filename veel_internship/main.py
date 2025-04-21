

import logging	
from configs.logging_config import setup_logging
from models.ollama_model import OllamaModel
from schemas.pydantic_schema import RequestRecipe  # importing from file from the root directory
from prompts.prompt_templates import SystemPrompts
import json

if __name__ == "__main__":
    new_model = OllamaModel(model_name="qwen")  # model name

    schema = RequestRecipe.model_json_schema()
    logging.info("Generating Recipe")

    # Pretty print the JSON schema
    print(json.dumps(schema, indent=2))

    input_json = {
        "Food_Type": "Non_Veg",
        "Food_Name": "Egg Fried Rice",
        "Ingredients": ["rice", "egg", "peas", "carrot", "soy sauce"]
    }

    stream = True  # Toggle streaming

    
if stream:
    recipe = new_model.streaming(input_json)
    
logging.info("Final recipe output:\n" + recipe)


   