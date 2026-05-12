from argparse import ArgumentParser
from pathlib import Path
import json
import sys

from PIL import Image
import torch
import torchvision.transforms.functional as tf
from tqdm import tqdm

sys.path.append(str(Path(__file__).resolve().parents[2]))

from lpipsPyTorch.modules.lpips import LPIPS
from utils.image_utils import psnr
from utils.loss_utils import ssim


def load_rgb(path, size=None):
    image = Image.open(path).convert("RGB")
    if size is not None and image.size != size:
        image = image.resize(size, Image.BICUBIC)
    return tf.to_tensor(image).unsqueeze(0).cuda()


def evaluate_scene(scene_dir, data_root, split="train", lpips_model=None):
    scene_dir = Path(scene_dir)
    scan_name = scene_dir.name if scene_dir.name.startswith("dtu_scan") else scene_dir.parent.name
    scan_id = scan_name.replace("dtu_scan", "")
    render_dir = scene_dir / split / "ours_30000" / "renders"
    if split == "test":
        gt_dir = scene_dir / split / "ours_30000" / "gt"
    else:
        gt_dir = Path(data_root) / f"scan{scan_id}" / "images"

    render_paths = sorted(list(render_dir.glob("*.jpg")) + list(render_dir.glob("*.png")))
    if not render_paths:
        raise FileNotFoundError(f"No render images found in {render_dir}")

    ssims = {}
    psnrs = {}
    lpipss = {}
    for render_path in tqdm(render_paths, desc=f"scan{scan_id} render metrics"):
        gt_path = gt_dir / f"{render_path.stem}.png"
        if not gt_path.exists():
            raise FileNotFoundError(f"Missing GT image for {render_path.name}: {gt_path}")

        render_image = Image.open(render_path).convert("RGB")
        render = tf.to_tensor(render_image).unsqueeze(0).cuda()
        gt = load_rgb(gt_path, render_image.size)
        if render.shape != gt.shape:
            raise ValueError(f"Shape mismatch for {render_path.name}: {render.shape} vs {gt.shape}")

        ssims[render_path.name] = ssim(render, gt).item()
        psnrs[render_path.name] = psnr(render, gt).item()
        if lpips_model is not None:
            lpipss[render_path.name] = lpips_model(render, gt).item()

    summary = {
        "SSIM": float(torch.tensor(list(ssims.values())).mean().item()),
        "PSNR": float(torch.tensor(list(psnrs.values())).mean().item()),
        "num_images": len(render_paths),
        "split": split,
        "iteration": 30000,
    }
    if lpipss:
        summary["LPIPS"] = float(torch.tensor(list(lpipss.values())).mean().item())
    per_view = {
        "SSIM": ssims,
        "PSNR": psnrs,
    }
    if lpipss:
        per_view["LPIPS"] = lpipss

    with (scene_dir / f"render_metrics_{split}.json").open("w") as fp:
        json.dump(summary, fp, indent=2)
    with (scene_dir / f"render_metrics_{split}_per_view.json").open("w") as fp:
        json.dump(per_view, fp, indent=2)

    return scan_id, summary


def main():
    parser = ArgumentParser()
    parser.add_argument("--scene_dirs", nargs="+", required=True)
    parser.add_argument("--data_root", default="data/dtu_dataset/dtu")
    parser.add_argument("--split", default="train", choices=["train", "test"])
    parser.add_argument("--skip_lpips", action="store_true")
    args = parser.parse_args()

    torch.cuda.set_device(torch.device("cuda:0"))
    lpips_model = None if args.skip_lpips else LPIPS(net_type="vgg").cuda()
    results = {}
    for scene_dir in args.scene_dirs:
        scan_id, summary = evaluate_scene(scene_dir, args.data_root, args.split, lpips_model)
        results[f"scan{scan_id}"] = summary
        print(f"scan{scan_id}: {summary}")

    if len(results) > 1:
        metric_keys = ("SSIM", "PSNR") if args.skip_lpips else ("SSIM", "PSNR", "LPIPS")
        means = {
            key: float(torch.tensor([scene[key] for scene in results.values()]).mean().item())
            for key in metric_keys
        }
        means["num_scenes"] = len(results)
        print(f"mean: {means}")


if __name__ == "__main__":
    main()
