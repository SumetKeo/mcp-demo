import asyncio
import os
from contextlib import AsyncExitStack

from anthropic import Anthropic
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SERVERS = {
    "mcp-postgres": os.path.join(BASE_DIR, "servers", "mcp-postgres"),
    "mcp-reporter": os.path.join(BASE_DIR, "servers", "mcp-reporter"),
}


async def main():
    client = Anthropic()
    tool_sessions: dict[str, ClientSession] = {}
    all_tools: list[dict] = []

    async with AsyncExitStack() as stack:
        # Connect to each MCP server
        for name, directory in SERVERS.items():
            params = StdioServerParameters(
                command="uv",
                args=["--directory", directory, "run", "main.py"]
            )
            transport = await stack.enter_async_context(stdio_client(params))
            session = await stack.enter_async_context(ClientSession(*transport))
            await session.initialize()

            tools = (await session.list_tools()).tools
            for tool in tools:
                tool_sessions[tool.name] = session
                all_tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema,
                })
            print(f"[{name}] connected — {len(tools)} tools")

        print(f"\nReady with {len(all_tools)} tools total. Type 'quit' to exit.\n")

        messages: list[dict] = []

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ("quit", "exit", "q"):
                break
            if not user_input:
                continue

            messages.append({"role": "user", "content": user_input})

            # Agentic loop
            while True:
                response = client.messages.create(
                    model="claude-opus-4-6",
                    max_tokens=4096,
                    tools=all_tools,
                    messages=messages,
                )
                messages.append({"role": "assistant", "content": response.content})

                if response.stop_reason == "end_turn":
                    for block in response.content:
                        if hasattr(block, "text"):
                            print(f"\nAssistant: {block.text}\n")
                    break

                # Handle tool calls
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        print(f"  → calling {block.name}...")
                        session = tool_sessions[block.name]
                        result = await session.call_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(result.content),
                        })

                messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    asyncio.run(main())
