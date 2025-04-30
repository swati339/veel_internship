from veel_internship.schemas.pydantic_schema import RequestRecipe

recipe_obj = RequestRecipe(Food_Type="Veg", Food_Name="mushroom", Ingredients=["onion", "tomato"])


class UserPrompt:
    user_message = (
        f"I wan to make {recipe_obj.Food_Type} recipe"
        f"Generate a recipe for {recipe_obj.Food_Name} using {recipe_obj.Ingredients}. "
        f"Provide a title for the recipe and list of ingredients and steps to make the recipe. "
        f"Use the following format: "
        f"Title: <title>"
        f"Ingredients: <list of ingredients>"
        f"Steps: <list of steps>"
        f"Ensure that the response is in JSON format with keys 'title', 'ingredients', and 'steps'."
        f"Use double quotes for strings and ensure proper JSON formatting."
    )
