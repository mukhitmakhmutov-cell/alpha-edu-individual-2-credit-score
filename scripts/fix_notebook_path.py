import json

with open('notebooks/notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = cell['source']
        if isinstance(source, list):
            new_source = []
            for line in source:
                if 'data_path' in line and 'application_train' in line:
                    line = 'data_path = "data/application_train.csv"\n'
                new_source.append(line)
            cell['source'] = new_source
        elif isinstance(source, str):
            if 'data_path' in source and 'application_train' in source:
                source = source.replace(
                    'data_path = "application_train.csv"',
                    'data_path = "data/application_train.csv"'
                )
                cell['source'] = source

with open('notebooks/notebook.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Fixed data_path in notebook")

with open('notebooks/notebook.ipynb', 'r', encoding='utf-8') as f:
    nb2 = json.load(f)
print("Notebook OK, cells:", len(nb2['cells']))
