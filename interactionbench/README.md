# InteractionBench sample viewer

A small, browsable sample of **InteractionBench** ("A Real-Time Interaction Benchmark for Streaming Video Systems").

- Dataset: https://huggingface.co/datasets/InteractionBench/InteractionBench
- Code: https://github.com/Espere-1119-Song/InteractionBench
- Blog: https://www.enxinsong.com/blog/interactionbench/
- Paper: not yet on arXiv (as of 2026-11-05)

Serve the directory over HTTP (`python3 -m http.server`) and open `index.html`. The page uses `fetch()`, so `file://` will not work.

## Sample

- 28 items on 27 videos, 4–6 per task (Look, Recall, Time, Alert, Track, Commentate).
- It includes 2 silent items, 3 near-miss suite items, MCQ and free-form items, and the rare `CIR` and `BRC` labels.
- Each video is the whole release file, re-encoded to 360p H.264 with AAC audio. Timestamps match the annotations 1:1.
- `data/samples.json` holds the verbatim `items.jsonl` rows. Keys starting with `_viewer_` were added here: the MCQ options shown to the system, the near-miss suite, the other items on the same video, and the source resolution.

## What the viewer shows

- **Timeline**: the question or standing request, each ground-truth response at its earliest warranted time, the 5-second Timing Accuracy window after it, `evidence_time_s`, and near-miss moments.
- **Table**: the same events in time order, with the near-miss "why it is not the event" text.
- **Scoring panel**: Accuracy, Timing Accuracy, Silence Compliance and Total, as defined in the repository README.
- **Stats**: computed over all 1,060 items (`full_dataset_stats.json`).

## Full-release numbers (computed here, 2026-11-05)

| | |
|---|---|
| Items | 1,060 |
| Videos | 812 (35.88 h, median 143.5 s, longest 940.6 s) |
| Timed ground-truth responses | 3,780 |
| Silent items | 69 |
| Items with an MCQ form | 688 |
| Near-miss suites | 53 (106 moments) |
| Items with `evidence_time_s` | 156 |

## Notes

- The capability codes (`IVQA`, `LVM`, `CIR`, `TOA`, `PTR`, `CST`, `BRC`, `LCG`) are not expanded anywhere in the release or the repository, so the viewer shows them as they are.
- No license is stated for the annotations. The videos come from public platforms and remain with their owners.
