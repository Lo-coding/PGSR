# DTU Evaluation Results

The DTU run in `output_dtu` completed on the standard 15 scenes:
24, 37, 40, 55, 63, 65, 69, 83, 97, 105, 106, 110, 114, 118, and 122.
The numbers below are read from each scene's `test/mesh/results.json`.

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

