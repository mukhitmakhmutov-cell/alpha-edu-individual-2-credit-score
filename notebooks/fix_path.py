import json

with open('notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        if isinstance(cell['source'], list):
            for j, line in enumerate(cell['source']):
                if 'data_path' in line and 'application_train' in line:
                    cell['source'][j] = 'data_path = "../data/application_train.csv"\n'
                    print(f'Fixed cell {nb["cells"].index(cell)}: {cell["source"][j].strip()}')

with open('notebook.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Done')
