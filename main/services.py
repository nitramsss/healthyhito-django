import os
from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def gemini_api(data):
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = prompt = f""" You are a meal generator. Respond ONLY with a valid Python dictionary. 
                            Do not include explanations, comments, markdown, or any text outside the dictionary. 

                            Input:
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

                            Output (one meal suggestion only) must be in this exact format:
                            {{
                                "title": "string",
                                "calories": integer,
                                "description": "string",
                                "ingredients": ["string", "string", ...],
                                "process": ["string", "string", ...],
                                "duration": "string",
                                "budget": "string"
                            }}
                        """


    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )

    return  response.text