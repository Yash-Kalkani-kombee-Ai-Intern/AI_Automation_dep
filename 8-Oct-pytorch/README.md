# PyTorch Fundamentals — Practice Project

## Project Overview

This project is created to learn the basics of **PyTorch**, a Python framework used for Machine Learning and Deep Learning.

In this project, we learn how to create tensors, perform mathematical operations, calculate gradients, load data in batches, and train a simple Linear Regression model.

**Technologies Used:**
- Python
- PyTorch
- NumPy
- Matplotlib
- Jupyter Notebook

## 1. What is PyTorch?

PyTorch is a Python library used to build and train Machine Learning and Deep Learning models.

It helps us:
- Perform mathematical calculations using tensors.
- Automatically calculate gradients.
- Build neural networks.
- Train models by updating weights and biases.
- Use CPUs and supported GPUs for computation.

## 2. What is a Tensor?

A Tensor is a container used to store numerical data.

It is similar to a NumPy array, but PyTorch tensors also support automatic gradient calculation and GPU operations.

```python
import torch

x = torch.tensor([1.0, 2.0, 3.0])
y = torch.tensor([4.0, 5.0, 6.0])

print(x + y)
print(x * y)
```

**Important operations:**

| Syntax | Meaning |
|---|---|
| `torch.tensor()` | Create a tensor |
| `x + y` | Addition |
| `x * y` | Element-wise multiplication |
| `x.shape` | Check tensor shape |
| `x.reshape()` | Change tensor dimensions |
| `torch.matmul()` | Matrix multiplication |
| `torch.sum()` | Sum all elements |
| `torch.mean()` | Calculate average |

## 3. What is Autograd?

Autograd is PyTorch's automatic differentiation system.

It tracks mathematical operations and helps calculate gradients.

A gradient tells us how changing a value affects the output or loss.

```python
x = torch.tensor(3.0, requires_grad=True)

y = x ** 2

y.backward()

print(x.grad)
```

Output:

```text
tensor(6.)
```

The derivative of `x²` is `2x`. When `x = 3`, the gradient is `6`.

**Important syntax:**

| Syntax | Purpose |
|---|---|
| `requires_grad=True` | Enable gradient tracking |
| `.grad_fn` | Show the recorded operation |
| `.backward()` | Calculate gradients |
| `.grad` | Access gradients |
| `.zero_()` | Reset accumulated gradients |

## 4. What is Backpropagation?

Backpropagation is the process of calculating how each trainable parameter affects the loss by working backward through the computational graph.

In simple words:

1. The model makes a prediction.
2. We calculate the prediction error.
3. Backward calculates gradients.
4. The optimizer uses gradients to update weights.
5. The process repeats to improve predictions.

**Gradient meaning:**

- Negative gradient: Gradient descent increases the corresponding weight.
- Positive gradient: Gradient descent decreases the corresponding weight.
- Zero gradient: No update from that gradient.

The learning rate controls how large the update is.

## 5. Dataset and DataLoader

### Dataset

A Dataset stores training data and defines how to access each sample.

For example:

| Study Hours | Exam Marks |
|---|---|
| 1 | 10 |
| 2 | 20 |
| 3 | 30 |
| 4 | 40 |

A custom PyTorch Dataset commonly uses:

- `__init__()` — Initialize data.
- `__len__()` — Return the number of samples.
- `__getitem__()` — Return one sample.

### DataLoader

DataLoader retrieves samples from the Dataset and groups them into batches.

```python
loader = DataLoader(
    dataset,
    batch_size=2,
    shuffle=True
)
```

**Meaning:**

- `batch_size=2`: Process two records at a time.
- `shuffle=True`: Randomize sample order.
- `epoch`: One complete pass through the dataset.
- `batch`: A group of samples processed together.

Dataset provides samples, while DataLoader organizes how those samples are delivered during training.

## 6. Linear Regression Model

We built a Linear Regression model to predict student exam marks based on study hours.

Our training data:

| Hours | Marks |
|---|---|
| 1 | 10 |
| 2 | 20 |
| 3 | 30 |
| 4 | 40 |
| 5 | 50 |
| 6 | 60 |

**Formula:**

`Prediction = Weight × Input + Bias`

The model learns the weight and bias automatically.

For this example, the ideal values are:

- Weight = 10
- Bias = 0

So for 7 study hours, the expected prediction is 70 marks.

## 7. How the Training Loop Works

```python
for epoch in range(1000):

    for hours, marks in loader:

        # Forward: predict marks
        predictions = w * hours + b

        # Loss: calculate error
        loss = loss_fn(predictions, marks)

        # Reset old gradients
        optimizer.zero_grad()

        # Backward: calculate new gradients
        loss.backward()

        # Update weight and bias
        optimizer.step()
```

**Training steps explained:**

| Step | Meaning |
|---|---|
| Forward | Make a prediction |
| Loss | Calculate prediction error |
| Zero Grad | Clear old gradients |
| Backward | Calculate gradients |
| Optimizer | Update model weights |
| Epoch | Repeat training on the dataset |

The model repeats these steps until it learns a good relationship between inputs and outputs.

## 8. Loss Function and Optimizer

**MSELoss (Mean Squared Error)**

Measures the average squared difference between predicted and actual values.

```python
loss_fn = torch.nn.MSELoss()
```

A smaller loss means the predictions are closer to the correct answers.

**SGD (Stochastic Gradient Descent)**

Updates model parameters using gradients.

```python
optimizer = torch.optim.SGD(
    [w, b],
    lr=0.01
)
```

The learning rate (`lr`) controls the update size.

## 9. Training Results

The model was trained for 1,000 epochs using batches of two samples.


The training-loss graph showed a sharp decrease at the beginning, followed by loss remaining close to zero.

This indicates that the model learned the training relationship successfully.

The ideal learned parameters are:

- Weight close to 10
- Bias close to 0
- Prediction for 7 hours close to 70

These results demonstrate how gradient descent helps reduce training error.

## 10. How to Run the Project

**Step 1 — Install dependencies**

```bash
pip install torch numpy matplotlib jupyter
```

**Step 2 — Open the Jupyter Notebook**

Open the project folder in VS Code and select the Python environment where the dependencies are installed.

**Step 3 — Run the cells**

Execute the notebook cells in order.

**Step 4 — Check results**

Verify the tensor operations, gradients, DataLoader batches, training loss, learned weights, and final predictions.

## 11. Key Learnings

After completing this project, we understand:

- PyTorch tensors and mathematical operations.
- Tensor reshaping and indexing.
- Automatic differentiation using Autograd.
- Gradients and backward propagation.
- Custom Dataset and DataLoader.
- Batch processing and epochs.
- Linear Regression using PyTorch.
- Loss calculation and optimization.
- Visualizing training performance.

## Conclusion

This project demonstrates the foundational concepts of PyTorch through practical examples.

We learned how numerical data is stored in tensors, how gradients are calculated automatically, how data is processed in batches, and how a machine learning model improves through repeated training.

These concepts form the foundation for building more advanced neural networks and deep learning applications.