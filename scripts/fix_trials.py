import json

with open('notebooks/notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        if isinstance(cell['source'], list):
            for j, line in enumerate(cell['source']):
                if 'n_trials = 15' in line:
                    cell['source'][j] = line.replace('n_trials = 15', 'n_trials = 30')
                    print(f'Fixed: {cell["source"][j].strip()}')

with open('notebooks/notebook.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Done')
