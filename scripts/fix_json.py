import json

with open('notebooks/notebook.ipynb', 'rb') as f:
    data = f.read()

# Current broken line (hex)
old_line = bytes.fromhex('2020202022646174615f70617468203d205c5c22646174612f6170706c69636174696f6e5f747261696e2e6373765c225c6e222c0d0a')
# Correct line (hex) - removed extra 5c before first 22
new_line = bytes.fromhex('2020202022646174615f70617468203d205c22646174612f6170706c69636174696f6e5f747261696e2e6373765c225c6e222c0d0a')

data = data.replace(old_line, new_line)

with open('notebooks/notebook.ipynb', 'wb') as f:
    f.write(data)

with open('notebooks/notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print('Fixed! Cells:', len(nb['cells']))
