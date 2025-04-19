from typing import List
from pydantic import BaseModel, Field
from typing import Literal

class RequestRecipe(BaseModel):
    Food_Type: Literal["Veg", "Non_Veg"] = Field(..., description="Type of food")
    Food_Name: str = Field(..., description="Name of the food")
    Ingredients: List[str] = Field(..., description ="List of foods")

    # model: str = Field(default = "qwen")
    # system_prompt: str = Field(default = "You are a helpful assistant that generates food recipes.")
    # temperature: float = Field(default = 0.5)
    # top_p: float = Field(default = 0.9)

class Responserecipe(BaseModel):
    title: str = Field(..., description="Title of the recipe")
    ingredients: List[str] = Field(..., description="List of ingredients")
    steps: List[str] = Field(..., description="List of steps to make the recipe")

    # temperature: float = Field(default = 0.5)
    # top_p: float = Field(default = 0.9)


