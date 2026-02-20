# mcp-client

An interactive terminal client that connects to MCP servers and uses **Claude** (`claude-opus-4-6`) to orchestrate tool calls via natural language.

## How It Works

1. Connects to `mcp-postgres` and `mcp-reporter` servers on startup
2. Discovers all available tools from both servers
3. Passes tools to Claude with each message
4. Claude decides which tools to call and in what order
5. Results are fed back to Claude to form a final response

## Setup

```bash
uv sync
cp .env.example .env
# fill in ANTHROPIC_API_KEY
```

## Environment Variables

```env
ANTHROPIC_API_KEY=sk-ant-your_api_key_here
```

Get your API key at [console.anthropic.com](https://console.anthropic.com).

## Run

```bash
uv run main.py
```

## Example Prompts

```
You: Show all pending orders
You: Which products are low on stock?
You: Get the orders summary and send it as an email report
You: Search for electronics products
You: Who placed the most expensive order?
```

## Available Tools

Automatically discovered from connected servers at startup:

- **mcp-postgres** — `get_all_products`, `search_products`, `get_products_by_category`, `get_low_stock_products`, `get_all_orders`, `get_orders_by_status`, `get_orders_summary`, `get_most_expensive_order`, `get_orders_by_customer`
- **mcp-reporter** — `send_report`
