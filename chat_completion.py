import os
from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("KEY"),
    base_url=os.getenv("BASE_URL"),
)

completion = client.chat.completions.create(
    model="grok-3",
    messages=[
        {"role": "system", "content": "Extract the event information, carefully analyze the text and extract the event data into JSON format."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on friday"},
    ],
)

response =completion.choices[0].message.content
print(response)
