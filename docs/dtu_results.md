# DTU Evaluation Results

The DTU run in `output_dtu` completed on the standard 15 scenes:
24, 37, 40, 55, 63, 65, 69, 83, 97, 105, 106, 110, 114, 118, and 122.
The geometry numbers below are read from each scene's `test/mesh/results.json`.

## Geometry Metrics

| Scan | Mean D2S | Mean S2D | Overall |
| ---: | ---: | ---: | ---: |
| 24 | 0.3240 | 0.3694 | 0.3467 |
| 37 | 0.5639 | 0.5285 | 0.5462 |
| 40 | 0.4021 | 0.3629 | 0.3825 |
| 55 | 0.2936 | 0.3858 | 0.3397 |
| 63 | 1.1467 | 0.4136 | 0.7801 |
| 65 | 0.5529 | 0.6128 | 0.5829 |
| 69 | 0.5062 | 0.4622 | 0.4842 |
| 83 | 0.7341 | 1.3828 | 1.0585 |
| 97 | 0.6656 | 0.6082 | 0.6369 |
| 105 | 0.4944 | 0.6781 | 0.5863 |
| 106 | 0.3751 | 0.5631 | 0.4691 |
| 110 | 0.5992 | 0.3782 | 0.4887 |
| 114 | 0.2797 | 0.3292 | 0.3045 |
| 118 | 0.3446 | 0.3973 | 0.3710 |
| 122 | 0.3174 | 0.3624 | 0.3399 |
| **Mean** | **0.5066** | **0.5223** | **0.5145** |

## Notes

- Best overall reconstruction: scan114 at 0.3045.
- Weakest overall reconstruction: scan83 at 1.0585, mostly due to the high S2D value.
- scan63 is the second largest outlier at 0.7801, driven by a high D2S value.
- The mean overall distance is higher than the README's reported PGSR Code_V1.0 mean of 0.47, but lower than the paper row mean of 0.53.

## Rendering Metrics

The original DTU run used `eval=False`, so the standard `metrics.py` test split had no images to evaluate. Rendering metrics were therefore computed on the existing train render outputs at iteration 30000, matching:

- rendered images: `output_dtu/dtu_scan*/test/train/ours_30000/renders/*.jpg`
- GT images: `data/dtu_dataset/dtu/scan*/images/*.png`

The GT images were resized to the render resolution because the run used `-r2`.

| Scan | Images | SSIM | PSNR |
| ---: | ---: | ---: | ---: |
| 24 | 49 | 0.9490 | 32.0608 |
| 37 | 49 | 0.9446 | 27.5843 |
| 40 | 49 | 0.9445 | 31.4730 |
| 55 | 49 | 0.9253 | 33.3487 |
| 63 | 49 | 0.9521 | 34.2074 |
| 65 | 49 | 0.9195 | 33.1672 |
| 69 | 49 | 0.9200 | 32.1264 |
| 83 | 64 | 0.9095 | 32.9266 |
| 97 | 64 | 0.9128 | 31.3316 |
| 105 | 64 | 0.9168 | 33.9859 |
| 106 | 64 | 0.9356 | 36.1473 |
| 110 | 64 | 0.9251 | 34.7478 |
| 114 | 64 | 0.9264 | 32.8084 |
| 118 | 64 | 0.9326 | 37.3437 |
| 122 | 64 | 0.9275 | 36.8250 |
| **Mean** | **56.5** | **0.9294** | **33.3389** |

LPIPS was not computed in this run because the WSL environment could not download the LPIPS `vgg.pth` weights from `raw.githubusercontent.com`. The helper script supports full SSIM/PSNR/LPIPS evaluation once the weight file is available; use `--skip_lpips` to reproduce the table above without LPIPS.

## Eval Split Rerun

Scenes 24, 37, and 40 were rerun with `--eval` and written to `output_dtu/dtu_scan*/eval`.
This creates a true held-out test split for novel-view rendering. The command used `-r2`, so both train and test rendering are at half resolution.

### Eval Geometry Metrics

| Scan | Mean D2S | Mean S2D | Overall |
| ---: | ---: | ---: | ---: |
| 24 | 0.3128 | 0.3775 | 0.3452 |
| 37 | 0.5792 | 0.5341 | 0.5566 |
| 40 | 0.4115 | 0.3555 | 0.3835 |
| **Mean** | **0.4345** | **0.4224** | **0.4284** |

### Novel-View Rendering Metrics

The metrics below use `eval/test/ours_30000/renders/*.png` and the corresponding `eval/test/ours_30000/gt/*.png`.

| Scan | Test Images | SSIM | PSNR |
| ---: | ---: | ---: | ---: |
| 24 | 7 | 0.9256 | 24.2548 |
| 37 | 7 | 0.9014 | 23.0943 |
| 40 | 7 | 0.9063 | 24.4782 |
| **Mean** | **7** | **0.9111** | **23.9424** |

These novel-view PSNR values are much lower than the train-view values, which is expected because the model did not train on these held-out camera views.
