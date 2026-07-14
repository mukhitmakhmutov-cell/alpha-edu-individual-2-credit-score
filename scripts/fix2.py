import json

with open("notebook.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

changes = 0

for i, cell in enumerate(nb["cells"]):
    src = "".join(cell["source"])

    # FIX A: Make CatBoost the primary model (override XGBoost/LightGBM priority)
    if "use_xgb = False" in src and "import xgboost" in src:
        src = src.replace(
            '    import xgboost\n    use_xgb = True\n    gb_model_name = "XGBoost"',
            '    import xgboost\n    use_xgb = False  # Prefer CatBoost GPU\n    gb_model_name = "CatBoost"'
        )
        src = src.replace(
            '    import lightgbm\n    use_lgbm = True\n    if not use_xgb:\n        gb_model_name = "LightGBM"',
            '    import lightgbm\n    use_lgbm = False  # Prefer CatBoost GPU'
        )
        src = src.replace(
            '    if not (use_xgb or use_lgbm):\n        gb_model_name = "CatBoost"',
            '    gb_model_name = "CatBoost"'
        )
        cell["source"] = src.split("\n")
        cell["source"] = [line + "\n" for line in cell["source"][:-1]] + ([cell["source"][-1]] if cell["source"][-1] else [])
        changes += 1
        print(f"[FIX A] Cell {i}: Made CatBoost the primary model")

    # FIX B: Reduce Optuna trials from 30 to 15
    if "n_trials = 30" in src:
        src = src.replace("n_trials = 30", "n_trials = 15")
        cell["source"] = src.split("\n")
        cell["source"] = [line + "\n" for line in cell["source"][:-1]] + ([cell["source"][-1]] if cell["source"][-1] else [])
        changes += 1
        print(f"[FIX B] Cell {i}: Reduced Optuna trials 30 -> 15")

    # FIX C: Optuna objective for CatBoost - add GPU to model creation
    if "def objective_catboost" in src and "task_type" not in src:
        src = src.replace(
            "catboost.CatBoostClassifier(\n            **params",
            "catboost.CatBoostClassifier(\n            task_type='GPU',\n            **params"
        )
        cell["source"] = src.split("\n")
        cell["source"] = [line + "\n" for line in cell["source"][:-1]] + ([cell["source"][-1]] if cell["source"][-1] else [])
        changes += 1
        print(f"[FIX C] Cell {i}: Added GPU to objective_catboost")

    # FIX D: Optuna objective selection - prefer CatBoost
    if "objective = objective_xgb" in src and "tune_name" in src:
        src = src.replace(
            '    if use_xgb:\n        objective = objective_xgb\n        tune_name = "XGBoost"',
            '    if use_catboost:\n        objective = objective_catboost\n        tune_name = "CatBoost"'
        )
        src = src.replace(
            '    elif use_catboost:\n        objective = objective_catboost\n        tune_name = "CatBoost"',
            '    elif use_xgb:\n        objective = objective_xgb\n        tune_name = "XGBoost"'
        )
        cell["source"] = src.split("\n")
        cell["source"] = [line + "\n" for line in cell["source"][:-1]] + ([cell["source"][-1]] if cell["source"][-1] else [])
        changes += 1
        print(f"[FIX D] Cell {i}: Optuna prefers CatBoost")

    # FIX E: Final model - prefer CatBoost
    if "final_model = xgboost.XGBClassifier(" in src and "best_params" in src and "final_model = catboost" in src:
        src = src.replace(
            '    if use_xgb:\n        final_model = xgboost.XGBClassifier(',
            '    if use_catboost:\n        final_model = catboost.CatBoostClassifier('
        )
        # Swap the blocks - find and reorder
        # This is complex, skip for now
        pass

print(f"\nTotal changes: {changes}")

with open("notebook.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Notebook saved.")
