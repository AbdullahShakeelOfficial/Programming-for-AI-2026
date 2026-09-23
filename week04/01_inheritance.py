class AIModel:
    """Base class for general AI models."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.is_trained = False

    def train(self) -> None:
        """Simulates model training."""
        self.is_trained = True

    def describe(self) -> str:
        """Returns base model description."""
        return f"Model: {self.model_name}"


class ClassificationModel(AIModel):
    """Subclass representing classification models."""

    def __init__(self, model_name: str, classes: list[str]):
        super().__init__(model_name)
        self.classes = classes

    def describe(self) -> str:
        return f"{super().describe()} | Classes: {self.classes}"


class RegressionModel(AIModel):
    """Subclass representing regression models."""

    def __init__(self, model_name: str, target_name: str):
        super().__init__(model_name)
        self.target_name = target_name

    def describe(self) -> str:
        # Relationship Note:
        # ClassificationModel and RegressionModel have an 'is-a' relationship with AIModel
        # because both specialized model classes inherit core attributes and training behaviors
        # while adding specific attributes for their domain task.
        return f"{super().describe()} | Target: {self.target_name}"


def main():
    clf = ClassificationModel("RandomForest", ["Cat", "Dog"])
    reg = RegressionModel("LinearRegressor", "HousePrice")

    clf.train()
    reg.train()

    print(f"{clf.describe()} | Trained: {clf.is_trained}")
    print(f"{reg.describe()} | Trained: {reg.is_trained}")


if __name__ == "__main__":
    main()