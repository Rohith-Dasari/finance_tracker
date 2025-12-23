import asyncio
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.session import ClientSession


async def main():
    server_params = StdioServerParameters(
        command="python", args=[r"server\mcp_server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "add_to_watchlist",
                arguments={"username": "rohith", "stock_name": "NVIDIA"},
            )
            print("Tool Response:", result.content)


if __name__ == "__main__":
    asyncio.run(main())
