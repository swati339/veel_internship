import logging
import json

from configs.logging_config import setup_logging
from models.ollama_model import OllamaModel
from schemas.pydantic_schema import RequestRecipe
from prompts.prompt_templates import SystemPrompts

if __name__ == "__main__":
    setup_logging()
    new_model = OllamaModel(model_name="qwen")

    schema = RequestRecipe.model_json_schema()
    logging.info("Generating Recipe")

    # Print in JSON
    print(json.dumps(schema, indent=2))

    input_json = {
        "Food_Type": "Non_Veg",
        "Food_Name": "Egg Fried Rice",
        "Ingredients": ["rice", "egg", "peas", "carrot", "soy sauce"]
    }

    # Streaming defined by the method itself
    recipe = new_model.generate_recipe(input_json, stream=True)

    logging.info("Final recipe output:\n" + recipe)
