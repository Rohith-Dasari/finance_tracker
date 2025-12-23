from fastmcp import Client
from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL
from datetime import date


async def run_chat(prompt: str, username: str):

    gemini = genai.Client(api_key=GEMINI_API_KEY)
    time_now = f"Today’s date is {date.today().isoformat()}. All relative date expressions must be resolved using this date."

    history = [
        genai.types.Content(
            role="user",
            parts=[
                genai.types.Part(
                    text=(
                        "You are a financial assistant. The current username is "
                        f"{username}. Always use this username when calling tools. "
                        "Summarize tool outputs into one short plain sentence. "
                        "Do not return markdown or bold markers. "
                        "Describe price as up/down with percent and mention volume only if notable. "
                        f"{prompt}" + time_now
                    )
                )
            ],
        )
    ]

    async with Client("server/mcp_server.py") as mcp_client:
        while True:
            response = await gemini.aio.models.generate_content(
                model=GEMINI_MODEL,
                contents=history,
                config=genai.types.GenerateContentConfig(
                    tools=[mcp_client.session],
                ),
            )

            content = response.candidates[0].content
            history.append(content)

            if response.text:
                return response.text

            tool_calls = getattr(content, "parts", [])
            if not tool_calls:
                return "No response from tools."

            for part in tool_calls:
                if not hasattr(part, "function_call"):
                    continue
                fc = part.function_call
                args = dict(fc.args) if hasattr(fc, "args") else {}
                tool_result = await mcp_client.session.call_tool(fc.name, args)
                history.append(
                    genai.types.Content(
                        role="tool",
                        parts=[
                            genai.types.Part(
                                function_response=genai.types.FunctionResponse(
                                    name=fc.name,
                                    response=tool_result,
                                )
                            )
                        ],
                    )
                )
