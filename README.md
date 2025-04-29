# Recipe Generator using Ollama and FastAPI

This project provides a FastAPI-based API to generate recipes using the Ollama language model.

## Features

- Generate structured or streamed recipe outputs from food name and ingredients.
- Uses local Ollama models ('qwen').
- Pydantic schema validation.
- Logging for debugging and tracking API calls.

## Requirements

- Python 3.11
- [Ollama](https://ollama.com) installed and running
- Required Python packages ( ` FastAPI, uvicorn, ollama, pydantic,starlette.`)


## API Endpoints

### `POST /generate-recipe`

Generate a recipe (structured output).

**Request Body**
```json
{
  "Food_Name": "Tomato Pasta",
  "Ingredients": ["Tomato", "Pasta", "Garlic", "Salt"]
}


uvicorn main:app --reload

