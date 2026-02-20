# mcp-reporter

An MCP server that sends HTML email reports via Gmail SMTP.

## Tools

| Tool | Parameters | Description |
|---|---|---|
| `send_report` | `subject`, `body`, `to_email?` | Send an HTML email. `to_email` defaults to `EMAIL_RECEIVER` in `.env` |

## Setup

```bash
uv sync
cp .env.example .env
# fill in .env
```

## Environment Variables

```env
EMAIL_SENDER=your_gmail@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
EMAIL_RECEIVER=receiver@gmail.com
```

> `EMAIL_PASSWORD` must be a **Gmail App Password**, not your regular password.
> Generate one at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) (requires 2FA enabled).

## Run

```bash
uv run main.py
```
