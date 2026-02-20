import os
import psycopg2
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("postgres-server")

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD", ""),
        port=int(os.getenv("DB_PORT", 5432))
    )


# ─────────────────────────────────────────
# PRODUCTS
# ─────────────────────────────────────────

@mcp.tool()
def get_all_products() -> list:
    """Get all products from the database."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, category, price, stock FROM products ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {"id": r[0], "name": r[1], "category": r[2], "price": float(r[3]), "stock": r[4]}
        for r in rows
    ]

@mcp.tool()
def search_products(keyword: str) -> list:
    """Search products by name or category."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, category, price, stock FROM products WHERE name ILIKE %s OR category ILIKE %s",
        (f"%{keyword}%", f"%{keyword}%")
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {"id": r[0], "name": r[1], "category": r[2], "price": float(r[3]), "stock": r[4]}
        for r in rows
    ]

@mcp.tool()
def get_products_by_category(category: str) -> list:
    """Get all products in a specific category."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, category, price, stock FROM products WHERE category ILIKE %s",
        (f"%{category}%",)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {"id": r[0], "name": r[1], "category": r[2], "price": float(r[3]), "stock": r[4]}
        for r in rows
    ]

@mcp.tool()
def get_low_stock_products(threshold: int = 50) -> list:
    """Get products with stock below the given threshold."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, category, price, stock FROM products WHERE stock < %s ORDER BY stock ASC",
        (threshold,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {"id": r[0], "name": r[1], "category": r[2], "price": float(r[3]), "stock": r[4]}
        for r in rows
    ]


# ─────────────────────────────────────────
# ORDERS
# ─────────────────────────────────────────

@mcp.tool()
def get_all_orders() -> list:
    """Get all orders with product details."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT o.id, o.customer_name, p.name AS product, p.category,
               o.quantity, o.total_price, o.status, o.ordered_at
        FROM orders o
        JOIN products p ON o.product_id = p.id
        ORDER BY o.ordered_at DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "order_id": r[0],
            "customer": r[1],
            "product": r[2],
            "category": r[3],
            "quantity": r[4],
            "total_price": float(r[5]),
            "status": r[6],
            "ordered_at": str(r[7])
        }
        for r in rows
    ]

@mcp.tool()
def get_orders_by_status(status: str) -> list:
    """Get orders filtered by status (pending, shipped, delivered, cancelled)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT o.id, o.customer_name, p.name AS product,
               o.quantity, o.total_price, o.status, o.ordered_at
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.status ILIKE %s
        ORDER BY o.ordered_at DESC
    """, (status,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "order_id": r[0],
            "customer": r[1],
            "product": r[2],
            "quantity": r[3],
            "total_price": float(r[4]),
            "status": r[5],
            "ordered_at": str(r[6])
        }
        for r in rows
    ]

@mcp.tool()
def get_orders_summary() -> dict:
    """Get a summary of orders grouped by status with total revenue."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT status, COUNT(*) AS total_orders, SUM(total_price) AS revenue
        FROM orders
        GROUP BY status
        ORDER BY status
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {
        "summary": [
            {"status": r[0], "total_orders": r[1], "revenue": float(r[2])}
            for r in rows
        ]
    }

@mcp.tool()
def get_most_expensive_order() -> dict:
    """Get the single most expensive order."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT o.id, o.customer_name, p.name AS product, p.category,
               o.quantity, o.total_price, o.status, o.ordered_at
        FROM orders o
        JOIN products p ON o.product_id = p.id
        ORDER BY o.total_price DESC
        LIMIT 1
    """)
    r = cur.fetchone()
    cur.close()
    conn.close()
    if not r:
        return {}
    return {
        "order_id": r[0],
        "customer": r[1],
        "product": r[2],
        "category": r[3],
        "quantity": r[4],
        "total_price": float(r[5]),
        "status": r[6],
        "ordered_at": str(r[7])
    }

@mcp.tool()
def get_orders_by_customer(customer_name: str) -> list:
    """Get all orders placed by a specific customer."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT o.id, o.customer_name, p.name AS product,
               o.quantity, o.total_price, o.status, o.ordered_at
        FROM orders o
        JOIN products p ON o.product_id = p.id
        WHERE o.customer_name ILIKE %s
        ORDER BY o.ordered_at DESC
    """, (f"%{customer_name}%",))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "order_id": r[0],
            "customer": r[1],
            "product": r[2],
            "quantity": r[3],
            "total_price": float(r[4]),
            "status": r[5],
            "ordered_at": str(r[6])
        }
        for r in rows
    ]


if __name__ == "__main__":
    mcp.run(transport='stdio')