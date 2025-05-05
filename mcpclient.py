import asyncio
import os
from agents import Agent, Runner
from agents.mcp import MCPServer, MCPServerSse
from agents.model_settings import ModelSettings
from dotenv import load_dotenv

#load .env
load_dotenv()

# run fastmcp run mcp-server-openai.py:mcp --transport sse
#before running this, run the mcp-server-openai.py file

async def main():
    server = MCPServerSse(
        name="SQLite Database Manager",
        params={
            "url": "http://localhost:8000/sse",
        },
    )
    await server.connect()  # Initialize the server connection
    
    agent = Agent(
        name="Database Assistant",
        instructions="""You are a database management assistant. Use the available tools to help with database operations.
        You can:
        1. List all tables in the database
        2. Describe the structure of any table
        3. Run SQL queries to get or modify data
        Always provide clear explanations of the results.""",
        mcp_servers=[server],
        model_settings=ModelSettings(tool_choice="required"),
    )

    history = []
    while True:

        message = input("Enter your message: ")
        if message.lower() == "exit":
            await server.cleanup()
            break

        history.append({"role": "user", "content": message})
        result = await Runner.run(starting_agent=agent, input=history)
        print(result.final_output)
        history.append({"role": "assistant", "content": result.final_output})

    
    await server.cleanup()  # Clean up the server connection

if __name__ == "__main__":
    asyncio.run(main())
 