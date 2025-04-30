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
    stream = True

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


# Gradio ChatInterface message handler
def chat_interface_fn(message, history):
    food_name = "Chat Request"  
    ingredients = message

    input_json = {
        "food_name": food_name.strip(),
        "ingredients": ingredients.strip()
    }

    logger.info(f"Gradio Chat input received: {input_json}")
    response = ollamamodel.generate_recipe(input_json, stream=True)

    accumulated = ""
    for chunk in response:
        accumulated += chunk
        yield accumulated


# Launch ChatInterface
def launch_gradio():
    chat = gr.ChatInterface(
        fn=chat_interface_fn,
        chatbot=gr.Chatbot(),
        textbox=gr.Textbox(placeholder="Enter ingredients to generate a recipe..."),
        title="Recipe Chat with Ollama",
        description="Chat-style recipe generator. Enter ingredients and get a live-generated recipe.",
        examples=[
            "tomato, onion, garlic",
            "chicken, soy sauce, ginger",
            "paneer, capsicum, turmeric"
        ]
    )
    chat.queue().launch()


if __name__ == "__main__":
    launch_gradio()
