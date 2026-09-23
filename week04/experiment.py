class Experiment:
    """Reusable Experiment entity class for experiment tracker."""

    def __init__(
        self,
        experiment_id: str,
        model_name: str,
        dataset_name: str,
        accuracy: float,
    ):
        if not (0.0 <= accuracy <= 1.0):
            raise ValueError("Accuracy must be between 0 and 1.")
        self.experiment_id = str(experiment_id)
        self.model_name = str(model_name)
        self.dataset_name = str(dataset_name)
        self.accuracy = float(accuracy)

    def to_dictionary(self) -> dict:
        """Returns JSON-compatible dictionary."""
        return {
            "experiment_id": self.experiment_id,
            "model_name": self.model_name,
            "dataset_name": self.dataset_name,
            "accuracy": self.accuracy,
        }