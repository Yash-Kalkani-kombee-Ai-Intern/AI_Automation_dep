"""Save a gallery of model predictions for unseen handwritten digits."""

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch

from utils import device_for_training, get_loader, load_model, seed_everything


def visualize(checkpoint: str, data_dir: str, output_dir: str, n: int, seed: int):
    if not 1 <= n <= 25:
        raise ValueError("--n must be between 1 and 25")
    seed_everything(seed)
    device = device_for_training()
    model = load_model(checkpoint, device)
    dataset = get_loader(train=False, batch_size=128, data_dir=data_dir).dataset
    indices = torch.randperm(len(dataset))[:n].tolist()
    images = torch.stack([dataset[index][0] for index in indices])
    actual = [dataset[index][1] for index in indices]
    with torch.inference_mode():
        predictions = model(images.to(device)).argmax(dim=1).cpu().tolist()

    columns = 5
    rows = (n + columns - 1) // columns
    fig, axes = plt.subplots(rows, columns, figsize=(columns * 2.1, rows * 2.5), squeeze=False)
    for ax in axes.flat:
        ax.axis("off")
    for index, ax in enumerate(axes.flat[:n]):
        ax.imshow(images[index][0].numpy(), cmap="gray")
        ax.set_title(f"True: {actual[index]} | Pred: {predictions[index]}", color="green" if actual[index] == predictions[index] else "red", fontsize=9)
    fig.suptitle("CNN predictions on MNIST test images")
    fig.tight_layout()
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    fig.savefig(output / "predictions.png", dpi=140)
    plt.close(fig)
    print(f"Saved prediction gallery to {(output / 'predictions.png').resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", default="outputs/cnn_mnist.pth")
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--n", type=int, default=15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    visualize(args.checkpoint, args.data_dir, args.output_dir, args.n, args.seed)
