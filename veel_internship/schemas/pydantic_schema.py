import logging
from configs.logging_config import setup_logging
from typing import List
from pydantic import BaseModel, Field
from typing import Literal

class RequestRecipe(BaseModel):
    Food_Type: Literal["Veg", "Non_Veg"] = Field(..., description="Type of food")
    Food_Name: str = Field(..., description="Name of the food")
    Ingredients: List[str] = Field(..., description ="List of foods")

class Responserecipe(BaseModel):
    title: str = Field(..., description="Title of the recipe")
    ingredients: List[str] = Field(..., description="List of ingredients")
    steps: List[str] = Field(..., description="List of steps to make the recipe")


