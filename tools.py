import os
import json
# import requests
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Literal

class TemperatureRequest(BaseModel):
    location: str = Field(description="The City and state, e,g, San Francisco, CA")
    unit: Literal["celsius", "fahrenheit"] = Field("fahrenheit", description="Temperature unit")

class CeilingRequest(BaseModel):
    location: str = Field(description="The city and state, e.g. San Francisco, CA")

def get_current_temperature(**kwargs):
    request = TemperatureRequest(**kwargs)
    temperature: int
    if request.unit.lower() == "fahrenheit":
        temperature = 59
    elif request.unit.lower() == "celsius":
        temperature = 15
    else:
        raise ValueError("unit must be one of fahrenheit or celsius")
    return {
        "location": request.location,
        "temperature": temperature,
        "unit": request.unit.lower()
    }

def get_current_ceiling(**kwargs):
    request = CeilingRequest(**kwargs)
    return {
        "location": request.location,
        "ceiling": 1500,
        "ceiling_type": "broken",
        "unit": "ft"
    }

get_current_temperature_schema = TemperatureRequest.model_json_schema()
get_current_ceiling_schema = CeilingRequest.model_json_schema()

tools_definition = [
    {
        "type": "function",
        "function": {
            "name": "get_current_temperature",
            "description": "Get the current temperature in a given location",
            "parameters": get_current_temperature_schema
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_ceiling",
            "description": "Get the current cloud ceiling in a given location",
            "parameters": get_current_ceiling_schema
        },
    },
]

tools_map = {
    "get_current_temperature": get_current_temperature,
    "get_current_ceiling": get_current_ceiling,
}

messages = [{"role": "user", "content" : "What's the temperature like in San Francisco"}]

client = OpenAI(
    api_key=os.getenv("KEY"),
    base_url=os.getenv("BASE_URL"),
)



response = client.chat.completions.create(
    model="grok-3-latest",
    messages=messages,
    tools=tools_definition,
    tool_choice="auto"

)

print(response.choices[0].message.content)

# Append assistant message including tool calls to messages
messages.append(response.choices[0].message)

# Check if there is any tool calls in response body
# You can also wrap this in a function to make the code cleaner

if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:

        # Get the tool function name and arguments Grok wants to call
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        # Call one of the tool function defined earlier with arguments
        result = tools_map[function_name](**function_args)

        # Append the result from tool function call to the chat message history,
        # with "role": "tool"
        messages.append(
            {
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id  # tool_call.id supplied in Grok's response
            }
        )
