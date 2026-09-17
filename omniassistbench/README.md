# OmniAssistBench sample viewer

A static viewer for a 17-case sample of **OmniAssistBench** (arXiv 2608.21360, "OmniAssistBench: Assistant-style Interaction Benchmark for Omni-LLMs", NJU / Nankai / Waterloo).

- Dataset: https://huggingface.co/datasets/JontiSun/OmniAssistBench (public, not gated)
- Code: https://github.com/XianyunSun/OmniAssistBench
- Project page: https://xianyunsun.github.io/OmniAssistBench/

To view it, run `python3 -m http.server` in this directory and open `http://localhost:8000/`. You can open a case directly with `?case=<id>`, for example `?case=navigation`.

## What the benchmark is

The HF release has 4 parquet shards (67.9 GB). Each shard has one row group per row.

- There are 687 rows but only 685 unique `video_name` values. `VSYjs5RnlRo-q1` and `gB0XyrWGFC4-q1` each appear twice.
- Each row is one QA turn. It holds the evaluation clip as embedded mp4 bytes, plus these text fields: `video_name`, `class`, `source`, `turns`, `question`, `gt_answer`, `key_points`, `example_video` (+ embedded bytes) and `example_text`.
- Multi-turn cases are chains of clips named `<id>-seg1..N`. A model sees them one chat turn at a time and replies after each clip, either with an answer or with `[KEEP QUIET]`.
- User prompts are embedded in the video, as speech, a picture-in-picture gesture, or on-screen text. The `question` field is only a human-readable copy.
- Grouping rows into cases gives 300 cases: 102 multi-turn and 198 single-turn. This matches the paper's "300 videos".

## How the subset was chosen

The sample has one case for each of the 16 sub-tasks and one real-world case, 17 cases in total:

| Tier | Sub-task | Case |
|---|---|---|
| Basic | II identity identification | fZl_LVU7a18-q1 |
| Basic | AI addressee identification | c6148208-q1 |
| Basic | CE complex emotion | 1_10495-q1 |
| Basic | ER event retrieval | HdnJE5S3oNI-q2 |
| Basic | AO appearance order | shorts-z1pFq-wYGpM-q1 |
| Basic | DC dynamic counting | Pao-hT2WNhA-q1 |
| Basic | AR action reference | bTmwvIL5eTs-q1 |
| Basic | LR linguistic reference | a1ba567f-q1 |
| Basic | GPF gesture prompt | Yt5xifeyx7I (3 turns) |
| Basic | OPF OCR prompt | yuh_fo6OKfQ-q1 |
| Advanced | CR context-aware | VID20251021095424 |
| Advanced | SER single-event proactive | A3WbCRfad-w-2 (4 turns, 3 KEEP QUIET) |
| Advanced | MER multi-event proactive | QiabTfzORmE (3 turns, 1 KEEP QUIET) |
| Advanced | ST step tracking | Mmq_fASrTB4 (6 turns, plan given as text) |
| Advanced | CT checklist tracking | bhoMvPJKc24, **excerpt** seg1–2 of 4 |
| Advanced | MT multitask tracking | acYN7Mkwhh0, **excerpt** seg1–2 of 4 |
| Real-world | RC blind-user navigation | navigation, **excerpt** seg14–20 of 20 (clip offset 457.0 s) |

Short cases were preferred because of the 55 MB size budget. Longer chains were cut to their first turns.

## Data files

- `data/cases.json` holds one object per case.
  - `records` contains the **verbatim HF rows** for the segments shown. The embedded `*.bytes` video columns are dropped; the `path` is kept.
  - Keys starting with `_viewer_` were added for this viewer:
    - Segment start and end in clip time, and the start time in the original chain.
    - Expected silence (`yes` / `no` / `either`). `KEEP QUIET`, `KEEP_QUIET` and `KEEP QUIET.` all count as silence.
    - Prompt modality, inferred from the sub-task.
    - An approximate span for the spoken question. This comes from Whisper-small ASR plus fuzzy text matching, so it is approximate and missing where matching failed.
    - The parquet row location and the clip offset.
- `full_dataset_stats.json` covers **all 687 rows**. The text columns were read directly. Each mp4 duration was read from its `mvhd` header with HTTP range requests.
  - The benchmark has 10.71 h / 59.4 GB of evaluation clips.
  - Mean case duration is 128.5 s (median 73.8 s). The paper reports a mean of 182 s; the unit it measures is unclear.
  - 80 turns expect `KEEP QUIET`, and 2 more accept either answer.
  - The stats also include the README leaderboard.
- `file_durations.json` holds the durations of the re-encoded clips.

## Re-encoding

- Segments are concatenated in order with ffmpeg / libx264, `-preset slow -crf 27 -maxrate 650k -bufsize 1300k`. `QiabTfzORmE` used crf 30 to stay under 8 MB.
- Frames are 24 fps, 640x360 (portrait chains 360x640). Mixed-orientation chains are letterboxed.
- **Audio is kept** as AAC 64 kbps at 44.1 kHz, because the prompts are spoken.
- Output uses `+faststart`.
- The average bitrate (~0.3–0.6 Mbps) is below the 500–700 kbps target in places. That is the cost of fitting 17 cases (1,038 s) into the 55 MB budget.
- The whole directory is about 47 MB, and each video is 8 MB or less.

## License / redistribution

- **Annotations:** the HF dataset card declares **Apache-2.0**. The GitHub README badge says MIT; the repo LICENSE file is the code license.
- **Videos:** most clips (571 of 687 rows) are **cut from YouTube videos** that belong to their creators. Others come from existing datasets, each under its own license: Mustard++, Ego4D, VIRAT, Assembly101, BASKET, MELD, COIN and CASTLE.
  - The 62 "filmed" rows (the real-world cases and several OCR/CR clips) were recorded by the authors.
  - The Apache-2.0 tag on the HF card cannot relicense third-party YouTube or Ego4D footage. Ego4D, for example, requires its own license agreement.
- **Redistribution:** the annotations may be redistributed under Apache-2.0. Redistributing the video excerpts is **not clearly permitted**. They are included here only as low-resolution research previews. Two of the sample clips (c6148208-q1 and a1ba567f-q1) come from Ego4D and one (1_10495-q1) from Mustard++. Do not publish this viewer publicly without checking the source licenses. For the Ego4D-, MELD- and Mustard-derived clips, link to the HF dataset instead.
