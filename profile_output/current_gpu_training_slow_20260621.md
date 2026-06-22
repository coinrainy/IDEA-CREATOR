# Current GPU Training Slowdown Diagnosis

Date: 2026-06-21 23:25 Asia/Shanghai.

## Running Job

- Parent runner: `reproduce_srlp.py`
- Active child process: `F:\Anaconda\python.exe train_srlp_transductive.py`
- Active task: `actor/full_latent_iso`, `split_id=3`, `epochs=1000`, `eval_epochs=100`
- Output root: `baselines/BGRL/runs/srlp_aux_10split_target_family_20260621_221832`

## Measurements

| Signal | Observed value |
| --- | --- |
| GPU | NVIDIA GeForce RTX 4060 Laptop GPU |
| GPU memory | about 3.0 GB / 8.0 GB |
| GPU utilization sample | 2-14% |
| GPU power sample | about 18-31 W |
| Python process CPU | about 93-102% of one logical CPU |
| Python working set | about 1.48 GB |
| Python process disk I/O | 0 B/s during sample |
| System disk time | about 1-3% |
| Available RAM | about 16 GB |

## Diagnosis

The current run is not slow because the GPU is overloaded. It is slow because
the workload is too small and too serial to keep the GPU busy. The runner
executes datasets, variants, and splits sequentially. The active training
process is mostly single-core CPU bound, while the RTX 4060 only receives many
small graph kernels and short evaluation bursts.

Code-level contributors found in the current harness:

- `reproduce_srlp.py` forces `OMP_NUM_THREADS`, `MKL_NUM_THREADS`,
  `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, and `TORCH_NUM_THREADS` to
  `1` for reproducible sequential runs.
- `reproduce_srlp.py` uses `subprocess.run(stdout=PIPE)`, so the child process
  output is buffered until the child finishes. This makes `split_3.log` look
  stalled during an active run.
- `train_srlp_transductive.py` writes TensorBoard scalars every epoch and runs a
  linear evaluation every 100 epochs.
- SRLP hard isolation rebuilds/filters online graph tensors every epoch.
- Diagnostic values such as effective rank and linear evaluation move tensors
  back to CPU for NumPy/scikit-learn work.

## Recommendation

For the current 10-split target-family ablation, the conservative choice is to
let it finish because the low GPU utilization is expected for small transductive
graph experiments and the run is still making progress. For faster future runs,
consider adding a less conservative runner mode that streams logs, relaxes CPU
thread caps for evaluation, reduces per-epoch TensorBoard writes, and optionally
runs independent small-graph jobs in parallel when GPU memory allows.
