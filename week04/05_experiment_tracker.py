import json
from pathlib import Path
from experiment import Experiment

# G2. Setup root-safe path definitions
lab_folder = Path(__file__).resolve().parent
json_path = lab_folder / "data" / "experiments.json"
report_path = lab_folder / "reports" / "experiment_summary.txt"


# G3. Add an experiment
def add_experiment(
    experiments: list[Experiment],
    experiment_id: str,
    model_name: str,
    dataset_name: str,
    accuracy: float | str,
) -> Experiment:
    try:
        acc_float = float(accuracy)
    except (ValueError, TypeError):
        raise ValueError(f"Accuracy '{accuracy}' must be numeric.")

    exp = Experiment(experiment_id, model_name, dataset_name, acc_float)
    experiments.append(exp)
    return exp


# G4. Display all experiments
def display_experiments(experiments: list[Experiment]) -> None:
    if not experiments:
        print("No experiments are available.")
        return
    for exp in experiments:
        print(
            f"{exp.experiment_id} | {exp.model_name} | "
            f"{exp.dataset_name} | Accuracy: {exp.accuracy:.2f}"
        )


# G5. Search by experiment ID
def search_experiment(
    experiments: list[Experiment], experiment_id: str
) -> Experiment | None:
    for exp in experiments:
        if exp.experiment_id == experiment_id:
            return exp
    return None


# G6. Compare experiments
def find_best_experiment(experiments: list[Experiment]) -> Experiment | None:
    if not experiments:
        return None
    return max(experiments, key=lambda exp: exp.accuracy)


# G7. Save experiments to JSON
def save_experiments(
    experiments: list[Experiment], file_path: Path | str
) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    records = [exp.to_dictionary() for exp in experiments] # list comprehension to convert each Experiment to a dictionary
    with path.open("w", encoding="utf-8") as file:
        json.dump(records, file, indent=4)


# G8. Load experiments from JSON
def load_experiments(file_path: Path | str) -> list[Experiment]:
    path = Path(file_path)
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            records = json.load(file)
            return [
                Experiment(
                    rec["experiment_id"],
                    rec["model_name"],
                    rec["dataset_name"],
                    rec["accuracy"],
                )
                for rec in records
            ]
    except json.JSONDecodeError:
        print("Error: JSON data is invalid.")
        return []


# G9. Write the summary report
def write_summary(experiments: list[Experiment], file_path: Path | str) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = ["=== Experiment Summary Report ===", ""]
    for exp in experiments:
        lines.append(
            f"ID: {exp.experiment_id} | Model: {exp.model_name} | Accuracy: {exp.accuracy:.2f}"
        )

    best = find_best_experiment(experiments)
    lines.append("")
    if best:
        lines.append(
            f"Best Experiment: {best.experiment_id} ({best.model_name}) with Accuracy {best.accuracy:.2f}"
        )
    else:
        lines.append("Best Experiment: None")

    with path.open("w", encoding="utf-8") as file:
        file.write("\n".join(lines))


# G10. Add assertions
def run_assertions() -> None:
    exps = []

    # 1. Conversion of accuracy string to float
    e1 = add_experiment(exps, "EXP-100", "CNN", "MNIST", "0.85")
    assert isinstance(e1.accuracy, float) and e1.accuracy == 0.85

    # 2. Conversion of Experiment object to dictionary
    d = e1.to_dictionary()
    assert d == {
        "experiment_id": "EXP-100",
        "model_name": "CNN",
        "dataset_name": "MNIST",
        "accuracy": 0.85,
    }

    # 3. Successful search for existing ID
    assert search_experiment(exps, "EXP-100") == e1

    # 4. Search for unknown ID returning None
    assert search_experiment(exps, "EXP-999") is None

    # 5. Selection of experiment with greatest accuracy
    e2 = add_experiment(exps, "EXP-101", "ResNet", "MNIST", 0.95)
    assert find_best_experiment(exps) == e2

    # Verify accuracy out of 0-1 range raises ValueError
    try:
        Experiment("EXP-ERR", "Test", "Data", 1.5)
        assert False, "Failed to raise ValueError for out-of-bounds accuracy!"
    except ValueError:
        pass

    print("All assertions passed successfully.")


# G11. Complete main()
def main():
    run_assertions()

    loaded = load_experiments(json_path)
    print(f"\nLoaded {len(loaded)} experiment records at startup.")

    # Add demonstration records if empty
    if not loaded:
        print("Data store empty. Adding default records...")
        add_experiment(
            loaded, "EXP-001", "Logistic Regression", "Student Performance", 0.84
        )
        add_experiment(
            loaded, "EXP-002", "Decision Tree", "Student Performance", 0.88
        )
        add_experiment(loaded, "EXP-003", "KNN", "Student Performance", 0.91)

    print("\n--- Current Experiments ---")
    display_experiments(loaded)

    print("\n--- Search EXP-002 ---")
    found = search_experiment(loaded, "EXP-002")
    if found is not None:
        print(found.to_dictionary())
    else:
        print("Experiment was not found.")

    best = find_best_experiment(loaded)
    if best:
        print(f"\nBest Experiment: {best.experiment_id} | Accuracy: {best.accuracy:.2f}")

    save_experiments(loaded, json_path)
    write_summary(loaded, report_path)

    reloaded = load_experiments(json_path)
    print(f"\nReloaded {len(reloaded)} records from disk.")
    assert len(reloaded) == len(
        loaded
    ), "Reload count does not match saved count!"


if __name__ == "__main__":
    main()