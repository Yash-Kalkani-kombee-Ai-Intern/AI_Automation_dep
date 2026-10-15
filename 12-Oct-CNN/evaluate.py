"""Evaluate a trained CNN against unseen MNIST test images."""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, confusion_matrix

from utils import device_for_training, get_loader, load_model, save_json


def evaluate(checkpoint: str, batch_size: int, data_dir: str, output_dir: str):
    device = device_for_training()
    model = load_model(checkpoint, device)
    loader = get_loader(train=False, batch_size=batch_size, data_dir=data_dir)
    actual, predicted = [], []
    with torch.inference_mode():
        for images, labels in loader:
            logits = model(images.to(device))
            predicted.extend(logits.argmax(dim=1).cpu().tolist())
            actual.extend(labels.tolist())

    actual, predicted = np.array(actual), np.array(predicted)
    accuracy = 100 * (actual == predicted).mean()
    print(f"MNIST test accuracy: {accuracy:.2f}% ({(actual == predicted).sum()}/{len(actual)} correct)")
    print(classification_report(actual, predicted, digits=4, zero_division=0))
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    matrix = confusion_matrix(actual, predicted, labels=list(range(10)))
    fig, ax = plt.subplots(figsize=(8, 7))
    ConfusionMatrixDisplay(matrix, display_labels=list(range(10))).plot(ax=ax, cmap="Blues", values_format="d", colorbar=False)
    ax.set_title("MNIST test confusion matrix")
    fig.tight_layout()
    fig.savefig(output / "confusion_matrix.png", dpi=140)
    plt.close(fig)
    save_json({"test_accuracy_percent": round(float(accuracy), 4), "test_samples": len(actual), "correct_predictions": int((actual == predicted).sum()), "per_digit": classification_report(actual, predicted, output_dict=True, zero_division=0)}, str(output / "evaluation_metrics.json"))
    print(f"Saved evaluation results to {output.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", default="outputs/cnn_mnist.pth")
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()
    evaluate(args.checkpoint, args.batch_size, args.data_dir, args.output_dir)
