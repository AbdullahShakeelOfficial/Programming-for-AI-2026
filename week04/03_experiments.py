import json
from pathlib import Path


class Experiment:
    """Stores AI experiment results with validated accuracy."""

    def __init__(
        self,
        experiment_id: str,
        model_name: str,
        dataset_name: str,
        accuracy: float,
    ):
        if not (0.0 <= accuracy <= 1.0):
            raise ValueError("Accuracy must be between 0 and 1.")
        self.experiment_id = experiment_id
        self.model_name = model_name
        self.dataset_name = dataset_name
        self.accuracy = accuracy

    def to_dictionary(self) -> dict:
        """Serializes instance fields into a JSON-compatible dictionary."""
        return {
            "experiment_id": self.experiment_id,
            "model_name": self.model_name,
            "dataset_name": self.dataset_name,
            "accuracy": self.accuracy,
        }


def main():
    lab_folder = Path(__file__).resolve().parent
    json_path = lab_folder / "data" / "experiments.json"

    exps = [
        Experiment("EXP-001", "Logistic Regression", "MNIST", 0.84),
        Experiment("EXP-002", "Decision Tree", "CIFAR-10", 0.88),
        Experiment("EXP-003", "KNN", "Iris", 0.91),
    ]

    # Convert custom objects to dictionary records before JSON dump
    dict_records = [exp.to_dictionary() for exp in exps]
    json_path.parent.mkdir(parents=True, exist_ok=True)

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(dict_records, file, indent=4)

    # Read back JSON and print top model
    try:
        with json_path.open("r", encoding="utf-8") as file:
            loaded_data = json.load(file)

        best_exp = max(loaded_data, key=lambda x: x["accuracy"])
        print("Best Experiment Loaded from JSON:")
        print(json.dumps(best_exp, indent=4))
    except FileNotFoundError:
        print(f"Error: missing file at '{json_path}'.")
    except json.JSONDecodeError:
        print("Error: JSON structure is invalid.")


if __name__ == "__main__":
    main()