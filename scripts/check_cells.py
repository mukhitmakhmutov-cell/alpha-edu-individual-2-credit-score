import json

with open('notebooks/notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i in range(min(6, len(nb['cells']))):
    cell = nb['cells'][i]
    src = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
    print(f'=== Cell {i} ({cell["cell_type"]}) ===')
    print(src[:300])
    print()
