"""Train a CNN on MNIST and save its weights and learning curves."""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
from torch import nn

from model import DigitCNN
from utils import device_for_training, get_loader, save_json, seed_everything


def train(epochs: int, batch_size: int, lr: float, seed: int, data_dir: str, output_dir: str):
    seed_everything(seed)
    device = device_for_training()
    print(f"Training on: {device}")
    loader = get_loader(train=True, batch_size=batch_size, data_dir=data_dir)
    model = DigitCNN().to(device)
    criterion = nn.CrossEntropyLoss()  # Expects raw scores, not softmax probabilities
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    history = {"epoch": [], "train_loss": [], "train_accuracy": []}

    for epoch in range(1, epochs + 1):
        model.train()
        loss_sum, correct, seen = 0.0, 0, 0
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            logits = model(images)
            loss = criterion(logits, labels)
            loss.backward()  # Backpropagation
            optimizer.step()  # Update weights
            loss_sum += loss.item() * images.size(0)
            correct += (logits.argmax(dim=1) == labels).sum().item()
            seen += labels.size(0)

        avg_loss = loss_sum / seen
        accuracy = 100.0 * correct / seen
        history["epoch"].append(epoch)
        history["train_loss"].append(round(avg_loss, 5))
        history["train_accuracy"].append(round(accuracy, 2))
        print(f"Epoch {epoch}/{epochs} | loss={avg_loss:.4f} | train_accuracy={accuracy:.2f}%")

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), output / "cnn_mnist.pth")
    save_json({"settings": {"epochs": epochs, "batch_size": batch_size, "learning_rate": lr, "seed": seed}, "history": history}, str(output / "training_metrics.json"))
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(history["epoch"], history["train_loss"], marker="o")
    ax.set(xlabel="Epoch", ylabel="Training loss", title="CNN training loss")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(output / "loss_curve.png", dpi=140)
    plt.close(fig)
    print(f"Saved model and plots to: {output.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()
    train(args.epochs, args.batch_size, args.lr, args.seed, args.data_dir, args.output_dir)
