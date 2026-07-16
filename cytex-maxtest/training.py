"""
ML lifecycle surface (ml_lifecycle_detector): training run, experiment tracking,
model artifacts. Static fixture — not meant to actually run.
"""
import mlflow
import wandb
import tensorflow as tf
import torch
import torch.nn as nn

wandb.init(project="cytex-maxtest", name="demo-run")
mlflow.set_experiment("cytex-maxtest")


def build_model():
    return tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(10, activation="softmax"),
    ])


def train():
    with mlflow.start_run():
        model = build_model()
        model.compile(optimizer="adam", loss="categorical_crossentropy")
        # training_run: the fit call + tracked params/metrics
        model.fit(x=[], y=[], epochs=5, batch_size=32)
        mlflow.log_param("epochs", 5)
        mlflow.log_metric("accuracy", 0.92)
        model.save("artifacts/model.h5")          # model artifact
        torch.save(nn.Linear(10, 2), "artifacts/model.pt")


if __name__ == "__main__":
    train()
