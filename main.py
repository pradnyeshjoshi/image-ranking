#!/usr/local/bin/python3
import os
import torch
import torch.utils.data
import torchvision.transforms as transforms
import torch.optim as optim
import torch.nn as nn
from utils import Data
import numpy as np

from models.resnet import resnet101, resnet18, ResNet, BasicBlock, resnet34, resnet50


transform_test = [transforms.ToTensor()]

transform_train = [
    transforms.RandomCrop(64, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor()]


# model = ResNet(BasicBlock, [3,4,23,3], num_classes=1000)
# model._name = "ResNet"#resnet18(pretrained=True)
# model.fc = nn.Linear(model.fc.in_features, 200)
# model = resnet18(pretrained=False)
# model.fc = nn.Linear(2048, 1024) #2048

model = resnet50(pretrained=True)
model.fc = nn.Linear(2048,2048)
# Hyperparamters
batch_size = 10
no_epoch = 10
LR = 0.0001
optimizer = optim.SGD(model.parameters(), lr=LR, momentum=0.9, weight_decay=1e-5)
criterion = nn.TripletMarginLoss(
    margin=1.0
)  # Only change the params, do not change the criterion.

scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.5)
upsample = nn.Upsample(scale_factor=3.5, mode='bilinear')

data = Data(
    batch_size,
    criterion,
    "../data/tiny-imagenet-200/",
    upsample=upsample,
    scheduler=scheduler,
    transform_train=transform_train,
    transform_test=transform_test,
)


start_epoch = 0 # Change me!


if os.path.exists(
    "models/trained_models/temp_{}_{}.pth".format(model.name, start_epoch)
):
    print("found model", model.name)
    model.load_state_dict(
        torch.load(
            "models/trained_models/temp_{}_{}.pth".format(model.name, start_epoch)
        )
        # data.test(model)
    )
    # data.test(model)
    data.train(no_epoch, model, optimizer, start_epoch=start_epoch + 1)
else:
    print("No model found for ", model.name)
    data.train(no_epoch, model, optimizer)
