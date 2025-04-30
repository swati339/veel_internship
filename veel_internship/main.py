

import json
import logging

import gradio as gr
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse

from utils.streamming import stream_generator
from veel_internship.configs.logging_config import setup_logging
from veel_internship.models.ollama_model import OllamaModel
from veel_internship.schemas.pydantic_schema import RequestRecipe

# Set up FastAPI app
app = FastAPI()

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize the model
ollamamodel = OllamaModel(model_name="qwen")


# FastAPI endpoint for recipe generation
@app.post("/generate-recipe")
async def generate_recipe(req: RequestRecipe):
    input_json = req.dict()
    stream = True  # Set to True to enable streaming response

    if stream:
        logger.info("Streaming mode enabled for recipe generation.")
        generator = stream_generator(ollamamodel, input_json)
        return StreamingResponse(generator, media_type="text/plain")
    else:
        logger.info("Structured output mode enabled for recipe generation.")
        response_text = ollamamodel.generate_recipe(input_json)
        logger.info(f"Response Text: {response_text}")
        
        
        try:
            parsed = json.loads(response_text)
            return JSONResponse(content=parsed)
        except json.JSONDecodeError:
            return {"response": response_text}


# Gradio
def gradio_generate_recipe(food_name: str, ingredients: str) -> str:
    input_json = {
        "food_name": food_name.strip(),
        "ingredients": ingredients.strip()
    }
    logger.info(f"Gradio input received: {input_json}")
    response = ollamamodel.generate_recipe(input_json)
    # return response
    for chunk in response:
        yield chunk


# Launch Gradio interface (for demo purposes)
def launch_gradio():
    demo = gr.Interface(
        fn=gradio_generate_recipe,
        inputs=[
            gr.Textbox(label="Food Name"),
            gr.Textbox(label="Ingredients (comma-separated)")
        ],
        outputs=gr.Textbox(label="Generated Recipe"),
        title="Recipe Generator with Ollama",
        description="Enter a food name and ingredients to get a recipe generated using Ollama."
    )
    demo.queue().launch()


if __name__ == "__main__":
    launch_gradio()
