from __future__ import print_function
from __future__ import division
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import argparse
from glob import glob
from pathlib import Path
from shutil import copy


parser = argparse.ArgumentParser(description='Compute mean and std for fMoW')
parser.add_argument('--data_dir', type=Path, default='../../data/fMoW/msrgb',
                        help='path to fmow dataset')


def main():
    args = parser.parse_args()
    data_transforms = transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.ToTensor(),
        ])
    dataset = datasets.ImageFolder(str(args.data_dir / "train"), data_transforms)
    loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=10,
        num_workers=1,
        shuffle=False
    )

    mean = 0.
    std = 0.
    nb_samples = 0.
    for data, labels in loader:
        batch_samples = data.size(0)
        data = data.view(batch_samples, data.size(1), -1)
        mean += data.mean(2).sum(0)
        std += data.std(2).sum(0)
        nb_samples += batch_samples

    mean /= nb_samples
    std /= nb_samples

    print("mean: ", mean)
    print("std: ", std)


if __name__ == '__main__':
    main()