# SPOT-Bench sample viewer

A small, browsable sample of **SPOT-Bench**, from "Don't Pause! Every prediction matters in a streaming video" (NeurIPS 2026 E&D Track, arXiv 2604.24317, NUS and Google).

- Dataset: https://huggingface.co/datasets/cvml-nus/spot-bench. It is gated with automatic approval and asks you to request Ego4D and Ego-Exo4D access first.
- Paper: https://arxiv.org/abs/2604.24317
- Code: https://github.com/dibschat/SPOT-Bench
- Project page: https://dibschat.github.io/SPOT-Bench/

Serve the directory over HTTP (`python3 -m http.server`) and open `index.html`. The page uses `fetch()`, so `file://` will not work.

## What the benchmark tests

The model watches the whole video as a stream and decides at every step whether to respond. Every response is scored, not only the ones at question times.

| Family | Task | Respond when | Release |
|---|---|---|---|
| Detection | ABD | the queried action starts or ends ("start" / "end") | full: 322 videos, 2,340 slots |
| Detection | PNR | the queried action takes effect ("now") | full: 286 videos, 1,234 slots |
| Interaction | SQA | enough evidence for the answer is visible | val: 15 videos, 101 slots |
| Interaction | SPG | the current step nears completion; give the next step | val: 13 videos, 95 slots |
| Intervention | SI | the user hesitates or errs in a known task | val: 13 videos, 40 slots |
| Intervention | UI | an imminent risk appears; nobody asks | val: 13 videos, 35 slots |

## Sample

- 30 cases, 4–6 per task.
- 25 show their whole release video, re-encoded to 360p H.264. The release has no audio.
- 5 cases show annotations only, because their video is from Ego4D, Ego-Exo4D or MovieNet. Ego4D and Ego-Exo4D require a signed license to redistribute. MovieNet clips are feature films.
- The 25 videos come from HT-Step (YouTube), Perception Test, THUMOS14, HoloAssist and EgoBlind.
- `data/samples.json` holds the verbatim annotation entries plus `_viewer_` keys: video id, task, source, zip path, size, duration and resolution.

## What the viewer shows

- **Timeline**: one lane per turn, with the question time and every ground-truth slot. Each slot is drawn as its actual Timeliness curve, using the per-task window and the early and late Gaussian widths from `evals/config.py`.
- **Hover readout**: the score a prediction at that moment would get, or that it would be a false positive.
- **"any" strip**: the moments where some slot is within reach. The rest of the stream is dead time.
- **Table**: questions, model context and gold responses in time order, with each slot's full-credit and matchable windows.
- **Stats**: computed over all six annotation files, plus the results tables from the GitHub README and the project page.

Released files and videos were read on 2026-11-11. The video subset was pulled from `videos.zip` with HTTP range requests, without downloading the 43 GB archive.
