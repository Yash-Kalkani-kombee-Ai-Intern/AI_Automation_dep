import torch
from torch import nn

from model import DigitCNN


def test_forward_shape():
    model = DigitCNN()
    result = model(torch.randn(4, 1, 28, 28))
    assert result.shape == (4, 10)


def test_one_training_step_updates_parameters():
    model = DigitCNN()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    images = torch.randn(4, 1, 28, 28)
    labels = torch.tensor([0, 1, 2, 3])
    before = model.classifier[-1].weight.detach().clone()
    loss = nn.CrossEntropyLoss()(model(images), labels)
    loss.backward()
    optimizer.step()
    assert not torch.equal(before, model.classifier[-1].weight.detach())
