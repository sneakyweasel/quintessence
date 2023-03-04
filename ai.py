''' GPT-3 and DALL-E integration. '''
import openai
import requests

VERBOSE = False
OPENAI_API_KEY = "123456"


def retrieve_gpt3_response(prompt):
    ''' GPT-3 prompt and evaluation method.'''
    openai.api_key = OPENAI_API_KEY

    # Send the prompt to GPT-3
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=400
    )
    return response.choices[0].text


def convert_storyline_to_image_prompts(storyline):
    ''' Method to split the GPT-3 response into a list of steps.'''
    # prompt_intro = "Digital art in the style of retrowave."
    prompt_intro = ""
    steps = storyline.split('\n')
    image_prompts = []
    for step in steps:
        if len(step) > 20:
            image_prompts.append(prompt_intro + step)
    return image_prompts


def retrieve_image_from_dalle(image_prompt):
    ''' Method to create images from the GPT-3 response.'''

    # Retrieve DALLE image
    response = openai.Image.create(
        prompt=image_prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response["data"][0]["url"]
    return image_url


def save_image(img_url, index):
    '''Save image to local file.'''
    img_data = requests.get(img_url, timeout=10).content
    with open(f'./haze-frontend/public/pic{str(index)}.png', 'wb') as handler:
        handler.write(img_data)
