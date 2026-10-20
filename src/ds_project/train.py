"""Train a baseline model and save it to ``models/``."""

import argparse

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline

from ds_project.config import MODELS_DIR, RANDOM_STATE
from ds_project.data import load_example_dataset, split
from ds_project.features import build_preprocessor


def build_model() -> Pipeline:
    return Pipeline(
        [
            ("preprocess", build_preprocessor()),
            ("model", RandomForestClassifier(random_state=RANDOM_STATE)),
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(MODELS_DIR / "model.joblib"))
    args = parser.parse_args()

    X_train, X_test, y_train, y_test = split(load_example_dataset())
    model = build_model().fit(X_train, y_train)
    print(classification_report(y_test, model.predict(X_test)))

    joblib.dump(model, args.output)
    print(f"Saved model to {args.output}")


if __name__ == "__main__":
    main()
