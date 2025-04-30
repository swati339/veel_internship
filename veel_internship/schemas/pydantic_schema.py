from typing import List, Literal

from pydantic import BaseModel, Field


class RequestRecipe(BaseModel):
    Food_Type: Literal["Veg", "Non_Veg"] = Field(..., description="Type of food")
    Food_Name: str = Field(..., description="Name of the food")
    Ingredients: List[str] = Field(..., description="List of foods")


class ResponseRecipe(BaseModel):
    title: str = Field(..., description="Title of the recipe")
    ingredients: List[str] = Field(..., description="List of ingredients")
    steps: List[str] = Field(..., description="List of steps to make the recipe")
