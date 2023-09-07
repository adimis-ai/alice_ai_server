import openai
import os

# Load your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the categories and topics for the content
categories = [
    "content that inspires you",
    "content that entertains you",
    "content that educates you",
    "content that shares your views",
    "content that makes you think",
]
topics = ["Technology", "Fullstack Development", "Artificial Intelligence"]

def generate_linkedin_post(category, topic):
    prompt = (
        f"Write a short, precise, and psychologically persuasive LinkedIn post "
        f"for a software development agency, about {category} related to {topic}"
    )

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text

    return response

# Generate text for each category and topic
for category in categories:
    for topic in topics:
        generated_text = generate_linkedin_post(category, topic)
        print("Generated LinkedIn Post:")
        print(generated_text)
        print("\n")
