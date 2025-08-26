GEMINI_API_KEY = 'AIzaSyBaSqdeZra6vX5zqrsbm37iFnarrUMwbFU'

def gemini_api(data):
    from google import genai

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
    # import json
    # meal = json.loads(response.text)

    # print(meal["ingredients"])
    # print(meal["ingredients"][0])


    return  response.text

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