import json
with open("output_notebook.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)
for i, cell in enumerate(nb["cells"]):
    status = cell.get("metadata", {}).get("papermill", {}).get("status", "not-run")
    exc = cell.get("metadata", {}).get("papermill", {}).get("exception", False)
    if status != "completed" or exc:
        print(f"Cell {i}: status={status}, exception={exc}")
total = len(nb["cells"])
print(f"Total cells: {total}")
last_ok = -1
for i, cell in enumerate(nb["cells"]):
    status = cell.get("metadata", {}).get("papermill", {}).get("status", "not-run")
    if status == "completed":
        last_ok = i
print(f"Last completed cell: {last_ok}")
