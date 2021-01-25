from __future__ import print_function
from __future__ import division
import argparse
from glob import glob
from pathlib import Path
from shutil import copy


parser = argparse.ArgumentParser(description='Creates a PyTorch ImageFolder-compatible dataset for fMoW')
parser.add_argument('--data_dir', type=Path, default='../../data/fMoW',
                        help='path to fmow dataset')
parser.add_argument('--dst_dir', type=Path, default='../../data/fMoW/msrgb',
                        help='path to new dataset destination')
parser.add_argument('--test_run', action='store_true',
                        help='runs in test mode (nothing is actually copied)')


def main():
    args = parser.parse_args()

    # get all immediate subfolders in train/val, assert they match
    class_paths, classes = {}, {}
    class_paths["train"] = [Path(p) for p in glob(str(args.data_dir / "train/*/"))]
    class_paths["val"] = [Path(p) for p in glob(str(args.data_dir / "val/*/"))]
    classes["train"] = [p.name for p in class_paths["train"]]
    classes["val"] = [p.name for p in class_paths["val"]]
    assert(set(classes["train"]) == set(classes["val"]))

    if args.test_run:
        print(classes["train"])

    for set_type in ["train", "val"]:
        # get dst paths
        destinations = [args.dst_dir / set_type / p.name for p in class_paths[set_type]]

        # make destination directories
        for d in destinations:
            d.mkdir(parents=True, exist_ok=True)

        # do the copying
        for cls in classes[set_type]:
            if args.test_run:
                msrgb_images = [Path(p) for p in glob(str(args.data_dir / f"{set_type}/{cls}/*/*msrgb.jpg"))][:10]
            else:
                msrgb_images = [Path(p) for p in glob(str(args.data_dir / f"{set_type}/{cls}/*/*msrgb.jpg"))]

            for img in msrgb_images:
                dst = args.dst_dir / set_type / cls
                if args.test_run:
                    print("About to copy..")
                    print(img)
                    print("to..")
                    print(dst)
                    print('')
                else:
                    copy(img, dst)


if __name__ == '__main__':
    main()
