from openai import OpenAI
import requests
import json


from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MCP_URL = "http://localhost:8000/api/mcp/"


class AIAgent:
    @staticmethod
    def execute_prompt(prompt: str, token: str):
        # 1. Fetch tools
        response = requests.post(
            MCP_URL,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list"
            }
        )

        tools_schema = response.json()

        # DEBUG: Print this to your terminal to see the ACTUAL error
        print(f"DEBUG MCP Response: {tools_schema}")

        # Check if "result" exists before accessing it
        if "result" not in tools_schema:
            return {
                "error": "MCP Server did not return results",
                "details": tools_schema  # This will likely show 'detail': 'Authentication credentials...'
            }

        tools = tools_schema["result"].get("tools", [])

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You control desktop automation tools."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            tools=tools
        )

        tool_calls = completion.choices[0].message.tool_calls

        results = []

        for call in tool_calls:

            result = requests.post(
                MCP_URL,
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": call.function.name,
                        "arguments": json.loads(call.function.arguments)
                    }
                }
            ).json()

            results.append(result)

        # services.py
        response = requests.post(
            MCP_URL,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list"
            }
        )

        if response.status_code != 200:
            return {"error": f"MCP Server returned {response.status_code}", "details": response.text}

        tools_schema = response.json()
