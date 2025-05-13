import os

from openai import OpenAI

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You're deepseek, the friendly and helpful whale of the deep blue ocean"},
        {"role": "user", "content": "Write me a limrick about the deep blue ocean"},
    ],
    stream = False
)

print(response.choices[0].message.content)
