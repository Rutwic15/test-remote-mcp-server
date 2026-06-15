# FastMCP Remote Server

A small Python project demonstrating how to build Model Context Protocol (MCP)
servers with [FastMCP](https://gofastmcp.com/).

The repository contains:

- An HTTP calculator server in `main.py`
- A SQLite-backed expense tracker example in `test.py`

## Requirements

- Python 3.14 or later
- [`uv`](https://docs.astral.sh/uv/) (recommended) or `pip`

## Calculator Server

Start the HTTP MCP server:

```bash
uv run main.py
```

The server listens on:

```text
http://localhost:8000/mcp
```

### Tools

| Tool | Description | Parameters |
| --- | --- | --- |
| `add_numbers` | Adds two integers | `a`, `b` |
| `generate_random` | Generates a random integer in a range | `min_val=1`, `max_val=100` |

### Resources

| URI | Description |
| --- | --- |
| `info://server` | Returns server metadata and the available tool names |

The server binds to `0.0.0.0`, so it can accept connections from other
machines when the host firewall and network configuration allow it.

## Expense Tracker Example

The expense tracker stores data in the local `expenses.db` SQLite database.
The database table is created automatically when the server starts.

Run it with:

```bash
uv run test.py
```

This example uses FastMCP's default transport.

### Tools

| Tool | Description |
| --- | --- |
| `add_expense` | Adds an expense with a date, amount, category, optional subcategory, and note |
| `list_expenses` | Lists every stored expense |

### Resources

| URI | Description |
| --- | --- |
| `expense://summary` | Returns total spending and a category breakdown |
| `expense://categories` | Lists categories and their totals |
| `expense://category/{category}` | Returns expenses for one category |

### Prompts

| Prompt | Description |
| --- | --- |
| `spending_review_prompt` | Reviews overall spending and suggests practical reductions |
| `category_review_prompt` | Analyzes spending within a selected category |

## Project Structure

```text
.
├── main.py          # HTTP calculator MCP server
├── test.py          # SQLite expense tracker MCP server
├── expenses.db      # Local expense data
├── pyproject.toml   # Project metadata and dependencies
├── uv.lock          # Locked dependency versions
└── README.md
```

## Notes

- Dates in the expense tracker are stored as text, so use a consistent format
  such as `YYYY-MM-DD`.
- `expenses.db` contains local application data. Avoid committing private
  financial information to a public repository.
- Stop a running server with `Ctrl+C`.
