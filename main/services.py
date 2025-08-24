GEMINI_API_KEY = 'AIzaSyBaSqdeZra6vX5zqrsbm37iFnarrUMwbFU'

def gemini_api(data):
    from google import genai
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""You are a meal generator. Always respond ONLY in valid JSON format without explanations, text, or markdown.
                    The client will provide the following input:
                    {{
                        "dietary": "{data['dietary']}",
                        "cuisine": "{data['cuisine']}",
                        "meal_type": "{data['meal_type']}",
                        "calories": "{data['calories']}",
                        "restriction": "{data['restriction']}",
                        "protein_source": "{data['protein_source']}",
                        "cooking_time": "{data['cooking_time']}",
                        "budget": "{data['budget']}"
                    }}

                    Based on the input, generate exactly one meal suggestion with the following fields in the JSON response:

                    {{
                    "title": "string (name of the meal)",
                    "calories": "integer (approximate calorie count)",
                    "description": "string (short description of the meal)",
                    "ingredients": ["list of strings (ingredients with amounts)"],
                    "process": ["list of strings (step-by-step instructions to cook)"],
                    "duration": "string (total cooking time in minutes)",
                    "budget": "string (approximate cost range in user's currency)"
                    }}

                    Rules:
                    - Do not include explanations, comments, or any text outside the JSON.
                    - Always return valid JSON only.
                    - Ensure values are relevant to the provided input.
                """

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )
    print(response.text)

# context = {
#     "dietary": "vegan",
#     "cuisine": "filipino",
#     "meal_type": "breakfast",
#     "calories": "1000",
#     "restriction": "halal",
#     "protein_source": "lamb",
#     "cooking_time": "20 minutes",
#     "budget": "200pesos"
# }

# gemini_api(context)