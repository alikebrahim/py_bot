import os
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List

class CalendarEvent(BaseModel):
    name: str = Field(description="Name of the event")
    date: str = Field(description="Date of the event")
    participants: List[str] = Field(description="List of participants")

client = OpenAI(
    api_key=os.getenv("KEY"),
    base_url=os.getenv("BASE_URL"),
)

completion = client.beta.chat.completions.parse(
    model="grok-3",
    messages=[
        {"role": "system", "content": "Extract the event information, carefully analyze the text and extract the event data into JSON format."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on friday"},
    ],
    response_format=  CalendarEvent,
)

response =completion.choices[0].message.parsed
print(response)
