from ds_project.data import load_example_dataset, split
from ds_project.train import build_model


def test_split_shapes():
    df = load_example_dataset()
    X_train, X_test, y_train, y_test = split(df, test_size=0.2)
    assert len(X_train) + len(X_test) == len(df)
    assert "target" not in X_train.columns
    assert len(y_train) == len(X_train)


def test_model_trains():
    X_train, X_test, y_train, y_test = split(load_example_dataset())
    model = build_model().fit(X_train, y_train)
    assert model.score(X_test, y_test) > 0.8
