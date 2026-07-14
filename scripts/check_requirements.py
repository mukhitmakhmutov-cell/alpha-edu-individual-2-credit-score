import json

with open('notebooks/notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    src = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
    preview = src[:150].replace('\n', ' | ')
    print(f'Cell {i:2d} [{cell["cell_type"]:7s}]: {preview}')
