import os
import sqlite3
from fastmcp import FastMCP

DB_URL = os.path.join(os.path.dirname(__file__), "expenses.db")

mcp = FastMCP("Expense tracker")


def init_db():
    with sqlite3.connect(DB_URL) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT DEFAULT '',
            note TEXT DEFAULT ''
            )"""
        )

init_db()


def fetch_all_expenses():
    with sqlite3.connect(DB_URL) as c:
        curr = c.execute(
            "SELECT id, date, amount, category, subcategory, note FROM expenses ORDER BY id ASC"
        )
        cols = [d[0] for d in curr.description]
        return [dict(zip(cols, r)) for r in curr.fetchall()]


def fetch_expenses_by_category(category: str):
    with sqlite3.connect(DB_URL) as c:
        curr = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE lower(category) = lower(?)
            ORDER BY date ASC, id ASC
            """,
            (category,),
        )
        cols = [d[0] for d in curr.description]
        return [dict(zip(cols, r)) for r in curr.fetchall()]


def build_summary():
    with sqlite3.connect(DB_URL) as c:
        total_row = c.execute(
            "SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM expenses"
        ).fetchone()
        category_rows = c.execute(
            """
            SELECT category, COUNT(*), COALESCE(SUM(amount), 0)
            FROM expenses
            GROUP BY category
            ORDER BY SUM(amount) DESC, category ASC
            """
        ).fetchall()

    return {
        "expense_count": total_row[0],
        "total_amount": total_row[1],
        "categories": [
            {"category": row[0], "count": row[1], "total_amount": row[2]}
            for row in category_rows
        ],
    }


@mcp.tool()
def add_expense(date, amount, category, subcategory = "", note=""):
    with sqlite3.connect(DB_URL) as c:
        curr = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?, ?, ?, ?, ?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": curr.lastrowid}


@mcp.tool()
def list_expenses():
    return fetch_all_expenses()


@mcp.resource("expense://summary")
def expense_summary():
    """High-level totals and category breakdown for the database."""
    return build_summary()


@mcp.resource("expense://categories")
def expense_categories():
    """List the categories currently present in the expense database."""
    summary = build_summary()
    return {
        "categories": [item["category"] for item in summary["categories"]],
        "details": summary["categories"],
    }


@mcp.resource("expense://category/{category}")
def expenses_for_category(category: str):
    """Return all expenses for a single category."""
    return {
        "category": category,
        "expenses": fetch_expenses_by_category(category),
    }


@mcp.prompt()
def spending_review_prompt():
    """Prompt for a general expense review using the available resources."""
    return """
Review my expense tracker data.

Use the `expense://summary` resource for totals and category breakdown.
Use the `expense://categories` resource if you need the available categories.
Then explain the biggest spending buckets, note any unusual patterns, and suggest 3 practical ways to reduce spending.
""".strip()


@mcp.prompt()
def category_review_prompt(category: str):
    """Prompt for analyzing one expense category in detail."""
    return f"""
Analyze my `{category}` spending in the expense tracker.

Use the `expense://category/{category}` resource to inspect the entries.
Summarize what the money is being spent on, call out any repeated patterns, and suggest a budget rule for this category.
""".strip()

if __name__ == "__main__":
    mcp.run()
