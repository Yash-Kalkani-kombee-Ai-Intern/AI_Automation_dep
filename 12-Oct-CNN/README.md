# CNN Image Classification with PyTorch (MNIST)

Beginner-friendly image classification with a CNN built **from scratch in PyTorch** (not a pretrained model).

## Objectives
- Explain convolution filters, ReLU, max pooling, flattening, and fully connected layers.
- Train a CNN on 60,000 MNIST grayscale handwritten-digit images.
- Evaluate on the **10,000-image held-out test set**, including precision/recall, confusion matrix, and sample predictions.
- Target **over 95% test accuracy** (commonly achievable after a few epochs, but actual results depend on training and environment).

## Architecture

```text
Input                   (N, 1, 28, 28)
Conv2d(1, 16, 3, p=1)   (N, 16, 28, 28)
ReLU + MaxPool2d(2)     (N, 16, 14, 14)
Conv2d(16, 32, 3, p=1)  (N, 32, 14, 14)
ReLU + MaxPool2d(2)     (N, 32, 7, 7)
Flatten                 (N, 1568)
Linear(1568, 128) + ReLU (N, 128)
Linear(128, 10)         (N, 10) raw scores (logits)
```

**Convolution:** a small learnable kernel slides across an image to detect patterns, such as strokes and curves.  
**Pooling:** max pooling summarizes each local 2 × 2 patch into its largest activation, reducing height/width by half.  
**Fully connected:** combines detected patterns and produces 10 class scores (digits 0–9).

## Files

```text
12-Oct-CNN/
├── model.py              # nn.Module CNN architecture
├── utils.py              # MNIST DataLoader and reusable helpers
├── train.py              # Training loop and loss curve
├── evaluate.py           # Held-out test accuracy and confusion matrix
├── predict.py            # Prediction image gallery
├── tests/test_model.py   # Basic shape and backprop checks
├── requirements.txt
├── .gitignore
└── README.md
```

## Run (Windows PowerShell)

From the `12-Oct-CNN` folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
python train.py --epochs 5
python evaluate.py
python predict.py --n 15
```

PyTorch installation may require a platform-specific command; see https://pytorch.org/get-started/locally/ if the default install is unsuitable. The MNIST download runs automatically on first use, requiring internet access.

To train longer if needed:

```powershell
python train.py --epochs 8
python evaluate.py
```

For CPU-only machines, training can be slower; there is no GPU requirement.

## Output files (created locally)

```text
outputs/
├── cnn_mnist.pth            # Trained model weights
├── training_metrics.json   # Epoch loss and train accuracy
├── loss_curve.png          # Loss graph
├── evaluation_metrics.json # Actual held-out test accuracy and per-class metrics
├── confusion_matrix.png    # Actual vs predicted digit counts
└── predictions.png         # True/predicted labels for sample images
```

`outputs/` and `data/` are ignored in Git by default to avoid uploading datasets and model artifacts. If your deliverable needs metrics in GitHub, copy the small `evaluation_metrics.json` into a separately tracked `results/` folder after evaluating; do not invent example scores.

## How training works
1. DataLoader supplies batches of images and correct digit labels.
2. `model(images)` produces 10 raw scores for each image.
3. `CrossEntropyLoss` compares those scores to the correct labels.
4. `loss.backward()` computes gradients via backpropagation.
5. `optimizer.step()` adjusts convolution and linear-layer weights.
6. Repeat over batches and epochs, then evaluate separately on unseen test data.

No softmax is applied in the model because `CrossEntropyLoss` handles logits directly. For predictions, `argmax(dim=1)` chooses the highest-scoring digit.

## GitHub commands
From the root of the existing `AI_Automation_dep` repository:

```powershell
git add 12-Oct-CNN
git commit -m "Add PyTorch CNN MNIST image classification project"
git push origin main
```

## Acceptance checklist
- [x] CNN layers, filters and pooling documented
- [x] Full PyTorch CNN training implementation
- [x] Hold-out test evaluation and visualizations implemented
- [ ] Run full MNIST training and **verify** actual test accuracy exceeds 95%
- [ ] Commit/push folder to GitHub
