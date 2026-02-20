# mcp-postgres

An MCP server that exposes PostgreSQL query tools for products and orders to any MCP client (Claude Desktop, mcp-client, etc.).

## Tools

### Products
| Tool | Description |
|---|---|
| `get_all_products` | Get all products |
| `search_products(keyword)` | Search by name or category |
| `get_products_by_category(category)` | Filter by category |
| `get_low_stock_products(threshold)` | Products below stock threshold (default: 50) |

### Orders
| Tool | Description |
|---|---|
| `get_all_orders` | Get all orders with product details |
| `get_orders_by_status(status)` | Filter by status: pending / shipped / delivered / cancelled |
| `get_orders_summary` | Revenue and count grouped by status |
| `get_most_expensive_order` | Single highest-value order |
| `get_orders_by_customer(customer_name)` | All orders for a customer |

## Setup

```bash
uv sync
cp .env.example .env
# fill in .env
```

## Database Setup

Initialize the database schema and mock data:

```bash
bash scripts/setup.sh
```

This will:
1. Create the `mcp-demo` database if it doesn't exist
2. Create `products` and `orders` tables
3. Insert 15 products and 20 mock orders

Or run the SQL manually:
```bash
psql -U postgres -d mcp-demo -f scripts/init.sql
```

## Scripts

| File | Description |
|---|---|
| `scripts/init.sql` | Schema + mock data (products & orders) |
| `scripts/setup.sh` | Auto-creates DB and runs `init.sql` |

## Environment Variables

```env
DB_HOST=localhost
DB_NAME=your_database_name
DB_USER=your_db_username
DB_PASSWORD=your_db_password
DB_PORT=5432
```

## Run

```bash
uv run main.py
```
