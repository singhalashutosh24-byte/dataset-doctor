import os 
import pandas as pd 
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Dataset Doctor")



@mcp.tool()
def say_hello(name: str) -> str:
    """Greets a person by name."""
    return f"Hello {name}, Dataset Doctor is alive!"



@mcp.tool()
def get_shape(file_path: str) -> str:
    """Returns the number of rows and columns in a CSV file."""
    df = pd.read_csv(file_path)
    rows, cols = df.shape
    return f"The dataset has {rows} rows and {cols} columns."
@mcp.tool()
def check_missing(file_path: str) -> str:
    """Counts the empty (missing) cells in each column of a CSV file."""
    df = pd.read_csv(file_path)
    missing = df.isna().sum()
    return f"Missing values per column:\n{missing.to_string()}"
@mcp.tool()
def check_hidden_zeros(file_path: str) -> str:
    """Counts zeros in every number column. A zero may be real (like 0 pregnancies) or a hidden missing value (like 0 insulin), so judge by what each column means."""
    df = pd.read_csv(file_path)
    numeric = df.select_dtypes(include="number")
    lines = []
    for col in numeric.columns:
        if numeric[col].nunique() <= 2:
            continue
        count = (numeric[col] == 0).sum()
        if count > 0:
            lines.append(f"{col}: {count} zeros")
    return "\n".join(lines) if lines else "No suspicious zeros found."

@mcp.tool()
def mark_hidden_zeros(file_path: str, columns: str) -> str:
    """Replaces zeros with empty values in the given columns (comma-separated names) and saves the result as data_marked.csv. Only use it on columns where zero is impossible."""
    df = pd.read_csv(file_path)
    names = [c.strip() for c in columns.split(",")]
    unknown = [c for c in names if c not in df.columns]
    if unknown:
        return f"These columns were not found: {unknown}"
    df[names] = df[names].replace(0, float("nan"))
    out_path = os.path.join(os.path.dirname(file_path), "data_marked.csv")
    df.to_csv(out_path, index=False)
    return f"Saved {out_path}. Zeros turned into empty values in: {', '.join(names)}."
    
@mcp.tool()
def fill_missing(file_path: str) -> str:
    """Fills empty cells in each column with that column's median and saves the result as data_clean.csv."""
    df = pd.read_csv(file_path)
    df = df.fillna(df.median(numeric_only=True))
    out_path = os.path.join(os.path.dirname(file_path), "data_clean.csv")
    df.to_csv(out_path, index=False)
    return f"Saved {out_path} with empty values filled using each column's median."
@mcp.tool()
def check_duplicates(file_path: str) -> str:
    """Counts rows that are exact copies of an earlier row in a CSV file."""
    df = pd.read_csv(file_path)
    count = df.duplicated().sum()
    return f"The dataset has {count} duplicate rows."
@mcp.tool()
def diagnose_dataset(file_path: str) -> str:
    """Runs all Dataset Doctor checks on a CSV file and returns one combined report with a verdict."""
    df = pd.read_csv(file_path)
    problems = []
    missing_total = int(df.isna().sum().sum())
    if missing_total > 0:
        problems.append(f"{missing_total} missing cells")
    dup_total = int(df.duplicated().sum())
    if dup_total > 0:
        problems.append(f"{dup_total} duplicate rows")
    if problems:
        verdict = "VERDICT: NOT READY. " + ", ".join(problems) + "."
    else:
        verdict = "VERDICT: No missing cells or duplicates. Check the zero report above for hidden problems."
    report = [
        get_shape(file_path),
        check_missing(file_path),
        check_hidden_zeros(file_path),
        check_duplicates(file_path),
        verdict,
    ]
    return "\n\n".join(report)
if __name__ == "__main__":
    mcp.run()