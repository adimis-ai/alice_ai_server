import openai
import datetime
import os

# Load your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_time_of_execution():
    return datetime.datetime.now()

def count_words(text):
    return len(text.split())

def remove_first_words(text, max_words):
    words = text.split()
    if len(words) > max_words:
        new_text = " ".join(words[max_words:])
        return new_text
    return text

def davinci_completion(
    prompt,
    temperature=0.0,
    max_tokens=700,
    top_p=1.0,
    n=1,
    frequency_penalty=1.5,
    presence_penalty=2.0,
    logprobs=10,
    model="text-davinci-003",
):
    try:
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            n=n,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            logprobs=logprobs,
        )
        return response.choices[0].text
    except Exception as e:
        return str(e)

def calculate_response_token(max_token, text):
    words = text.split()
    max_response_token = (max_token - len(words)) / 1.33
    return max_response_token
