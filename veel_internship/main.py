# import logging
# from veel_internship.configs.logging_config import setup_logging


# setup_logging()
# logger = logging.getLogger(__name__)

# # Example usage of logging
# logger.info("This is an info message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")


	

from veel_internship.models.ollama_model import OllamaModel
from veel_internship.schemas.pydantic_schema import RequestRecipe  # importing from file from the root directory
from veel_internship.prompts.prompt_templates import SystemPrompts
import json

if __name__ == "__main__":
    new_model = OllamaModel(model_name="qwen")  # model name

    schema = RequestRecipe.model_json_schema()

    # Pretty print the JSON schema
    print(json.dumps(schema, indent=2))

    input_json = {
        "Food_Type": "Non_Veg",
        "Food_Name": "Egg Fried Rice",
        "Ingredients": ["rice", "egg", "peas", "carrot", "soy sauce"]
    }

    stream = True  # Toggle streaming

    print("Generating Recipe")
    
    # Use streaming if set to True, else structured_output
    if stream:
        recipe = new_model.streaming(input_json["Food_Name"])
    else:
        recipe = new_model.structured_output(input_json["Food_Name"])
    
    # print("\nFinal Recipe Output:")
    # print(recipe)

   