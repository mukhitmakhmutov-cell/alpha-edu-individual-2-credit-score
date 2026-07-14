import json

with open("notebook.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

changes = 0

for i, cell in enumerate(nb["cells"]):
    src = "".join(cell["source"])

    # FIX 1: Drop constant columns
    if "SK_ID_CURR" in src and "drop_cols" in src and "high_missing" in src:
        new_src = """if df is not None:
    # Drop technical identifiers
    drop_cols = ["SK_ID_CURR"]

    # Drop columns with very high missing percentage (>70%)
    high_missing = df.columns[df.isna().mean() > 0.70].tolist()
    drop_cols.extend(high_missing)

    # Drop constant / near-constant numeric columns (std < 1e-6)
    num_df = df.select_dtypes(include=["number"])
    constant_cols = num_df.columns[num_df.std() < 1e-6].tolist()
    drop_cols.extend(constant_cols)

    drop_cols = list(set(drop_cols))  # remove duplicates

    print(f"Удаляем {len(drop_cols)} столбцов:")
    print(drop_cols)
    print()

    df.drop(columns=drop_cols, inplace=True)
    print(f"Осталось столбцов: {df.shape[1]}")
"""
        lines = new_src.split("\n")
        cell["source"] = [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
        changes += 1
        print(f"[FIX 1] Cell {i}: Added constant column drop")

    # FIX 2: Enable CatBoost GPU
    if "catboost.CatBoostClassifier(" in src and "task_type" not in src:
        src = src.replace(
            "catboost.CatBoostClassifier(\n            iterations=",
            "catboost.CatBoostClassifier(\n            task_type='GPU',\n            iterations="
        )
        src = src.replace(
            'catboost.CatBoostClassifier(\n            **params, random_state=42, verbose=0, auto_class_weights="Balanced"',
            "catboost.CatBoostClassifier(\n            task_type='GPU',\n            **params, random_state=42, verbose=0, auto_class_weights=\"Balanced\""
        )
        lines = src.split("\n")
        cell["source"] = [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
        changes += 1
        print(f"[FIX 2] Cell {i}: Enabled CatBoost GPU")

    # FIX 3: Remove deprecated use_label_encoder
    if "use_label_encoder" in src:
        src = src.replace(", use_label_encoder=False", "")
        src = src.replace("use_label_encoder=False, ", "")
        lines = src.split("\n")
        cell["source"] = [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
        changes += 1
        print(f"[FIX 3] Cell {i}: Removed deprecated use_label_encoder")

print(f"\nTotal changes: {changes}")

with open("notebook.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Notebook saved.")
