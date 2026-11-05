# VideoMemBench sample viewer

A small, browsable sample of **VideoMemBench** ("How Well Do MLLMs Remember in Video Conversations?", arXiv 2610.40131).

- Dataset: https://huggingface.co/datasets/VideoMemBench/data
- Paper: https://arxiv.org/abs/2610.40131
- Code: https://github.com/Oliiveralien/VideoMemBench
- Project page: https://videomembench.github.io/

Serve the directory over HTTP (`python3 -m http.server`) and open `index.html`. The page uses `fetch()`, so `file://` will not work.

## What the benchmark tests

Each video has one ordered multi-turn dialogue. Later turns depend on earlier ones through typed links:

- **Episodic**: the question revisits a scene or entity set up earlier.
- **Answer**: the question builds on an earlier answer.

The model sees 128 uniform timestamped frames plus its own earlier answers (self-rollout). It is not a streaming benchmark, and turns have no timestamps.

## Sample

- 14 dialogues, grouped by video length: 5 under 2 min, 4 from 2 to 10 min, 3 long, and 2 that show release issues.
- 13 show the whole release video re-encoded to 360p H.264. `videomembench-36` shows the dialogue alone.
- `data/samples.json` holds the verbatim `annotations.jsonl` rows plus `_viewer_` keys: probed duration, resolution, file size, and release row index.

## What the viewer shows

- **Dependency graph**: episodic links above the turns, answer links below.
- **Turn table**: options with the key highlighted, links, and the answer chain that AnsDepAcc requires to be correct.
- **Timeline**: where the 128 protocol frames fall, and any times written in the questions. Those times are clickable.
- **Stats**: computed over all 326 dialogues, plus the 25-model leaderboard from the GitHub README.

## Full-release numbers (computed here, 2026-11-05)

| | |
|---|---|
| Videos / dialogues | 326 |
| Turns | 2,476 (1,709 open, 603 multiple choice, 164 true/false) |
| Dependency links | 1,200 episodic, 594 answer |
| Video size | 146.5 GB |
| Hours | 130.6, leaving out one outlier |
| Median video | 17 min |

## Release issues found

- **22 videos are 2-second stubs** under 0.3 MB, but their dialogues have 4–7 turns about a longer video. One is `videomembench-58`, included here.
- **`videomembench-36`** is 4.9 GB, and ffprobe reports 84,485 s (23.5 h). That is almost certainly a broken container duration. It is left out of the hours total.

## License

The HF card puts the annotations under CC BY-NC-SA 4.0, for evaluation only and not for training. The GitHub README says redistribution needs prior written permission. Source videos remain with their owners.
