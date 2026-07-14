import json

with open('notebooks/notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Add %matplotlib inline to the imports cell
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
        if 'import pandas as pd' in src and 'matplotlib' not in src:
            if isinstance(cell['source'], list):
                cell['source'].insert(0, '%matplotlib inline\n')
                for j, line in enumerate(cell['source']):
                    if 'import pandas as pd' in line:
                        cell['source'].insert(j, 'import matplotlib.pyplot as plt\n')
                        cell['source'].insert(j+1, 'import seaborn as sns\n')
                        break
            break

with open('notebooks/notebook.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print('Added %matplotlib inline')
