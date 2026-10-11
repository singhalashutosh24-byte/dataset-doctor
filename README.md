# Dataset Doctor

An MCP server that checks whether a CSV file is ready for machine learning.
Connect it to Claude Desktop and ask in plain English: "Is my dataset ready for ML?"

## What makes it different

A normal missing-value check says the Pima Indians Diabetes dataset has **0 missing values**.
But it has hundreds of hidden ones: zeros in columns like Insulin (374 of 768 rows)
where a zero is impossible. Dataset Doctor finds these, lets Claude judge which zeros
are fake (0 pregnancies is real, 0 insulin is not), and fixes only those columns.

## Tools

| Tool | What it does |
|---|---|
| `diagnose_dataset` | Full check-up with a final verdict |
| `get_shape` | Number of rows and columns |
| `check_missing` | Empty cells per column |
| `check_hidden_zeros` | Zeros in every number column, for Claude to judge |
| `check_duplicates` | Rows that are exact copies |
| `mark_hidden_zeros` | Turns chosen fake zeros into real empty cells |
| `fill_missing` | Fills empty cells with each column's median |

Cleaned files are saved next to the original. The original is never changed.

## Setup

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Test it in the MCP Inspector (needs Node.js):

```
npx @modelcontextprotocol/inspector python server.py
```

## Use it with Claude Desktop

Add this to `claude_desktop_config.json`, using your own paths:

```json
"mcpServers": {
  "dataset-doctor": {
    "command": "C:\\path\\to\\dataset-doctor\\venv\\Scripts\\python.exe",
    "args": ["C:\\path\\to\\dataset-doctor\\server.py"]
  }
}
```

Restart Claude Desktop, then try:

> Use dataset-doctor's diagnose_dataset on C:\path\to\dataset-doctor\data.csv

## Data

`data.csv` is the Pima Indians Diabetes dataset (768 patients, 9 columns).