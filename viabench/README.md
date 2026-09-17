# VIABench sample viewer

This directory holds a small, browsable sample of **VIABench** ("A Comprehensive Video Benchmark Collected from Blind Individuals for Visual Impairment Assistance", arXiv 2607.14660, Nanjing University MCG and Shanghai AI Laboratory).

- Dataset: https://huggingface.co/datasets/MCG-NJU/VIABench
- Paper: https://arxiv.org/abs/2607.14660
- Code: https://github.com/MCG-NJU/VIABench. It holds only the prompts and the judge prompt. No project page was found.

To open it, serve the directory over HTTP (`python3 -m http.server`) and load `index.html`. The page uses `fetch()`, so opening it from `file://` will not work.

## What the benchmark tests

VIABench has three annotation modes. The viewer has a **Mode** selector for switching between them.

| Mode | File | One record | Fields |
|---|---|---|---|
| Proactive Reminder (PR) | `annotations/proactive_reminder.json` | One video. Its `annotations[]` list holds the alert windows. | `video_uid`, `caption`; each annotation has `qid`, `start_time`, `end_time`, `task` (subtask), `description` (reference reminder) |
| VQA | `annotations/visual_question_answering.json` | One video. Its `annotations[]` list holds the questions. | `video_uid`, `caption`; each annotation has `qid`, `start_time`, `end_time`, `task` (Simulated Query / Blind Person Query), `question`, `answer` |
| Vision-Guided Interaction (VGI) | `annotations/vision_guided_interaction.json` | One episode key (`4_convert_files/NNN`), mapped to a list of guidance turns | `start_time`, `end_time`, `task` (Camera Manipulation / Target Manipulation / Movement Guidance / Completion), `description`, `target` (the user's goal), `video` |

- **PR:** a ground-truth window `[start_time, end_time]` is the period in which an unprompted alert counts as correct.
- **VQA:** a question is asked at `start_time`, and the model may use only the video before that moment.
- **VGI:** step-by-step guidance toward the `target` goal.

## Full-dataset numbers (public release, computed here)

All numbers below are in `full_dataset_stats.json`. They come from the three annotation files plus an `ffprobe` of all 600 released mp4 files, read over HTTP.

| | Released on HF (2026-09-16) | Paper |
|---|---|---|
| Videos | **600** (69.25 GB) | 761 |
| Hours | **45.42** | 46.9 |
| Annotations | **14,158** | 14,526 |
| PR | 13,152 windows on 530 videos | — |
| VQA | 340 questions on 165 videos. All 165 are also PR videos. | — |
| VGI | 666 turns in 70 episodes | 231 purpose-filmed videos |
| PR subtask labels | 22 real labels + 2 stray query labels | 21 |

- **VGI videos:** only 70 of the paper's 231 purpose-filmed videos are in the public release.
- **PR subtask labels:** the released file has 22 real labels. "Stairs Up/Down" and "Staircase Up/Down" look like one subtask split in two, and merging them gives the paper's 21. Two annotations labelled "Simulated Query" / "Blind Person Query" sit in the PR file by mistake.
- **PR window length:** median 1.77 s, mean 6.33 s.
- **PR data issues:**
  - 42 windows end before they start.
  - 10 windows have zero length.
  - 10 windows end after the video ends.
- **VQA data issues:**
  - 18 questions have a zero-length span.
  - 1 question has `end_time < start_time`.
  - 10 reference answers say "unable to determine".
- **Videos by source:**

  | Source | Videos | Hours |
  |---|---|---|
  | Douyin | 234 | 12.41 |
  | YouTube | 151 | 23.15 |
  | Bilibili | 91 | 8.04 |
  | YouTube Shorts | 54 | 0.46 |
  | Purpose-filmed VGI | 70 | 1.36 |

- **Source video length:** median 2:54, maximum 32:39.

## The 12 cases and how they were chosen

There are 4 cases per mode. All times are in the ORIGINAL video's seconds. For a clip, clip time = original time − `_viewer_clip_offset_s`.

| Mode | Case | Source | Shown clip | Why |
|---|---|---|---|---|
| PR | 4_bilibili_c/0645 | Bilibili | full 58 s | Traffic lights, crosswalk, camera obstruction, sidewalk. 13 windows, 7 subtasks. |
| PR | 5_douyin_1_c/0747 | Douyin | 71–146 s of 217 s | Escalator, box elevator, staircase, road branch, direction guidance. 39 windows. |
| PR | 5_douyin_1_c/0733 | Douyin | 35–110 s of 169 s | Intersection, crossing to the other side, road surface, stairs |
| PR | 5_douyin_1_c/0827 | Douyin | 60–135 s of 175 s | Direction deviation, slope, road surface, active avoidance. 35 windows. |
| VQA | 4_bilibili_c/0524 | Bilibili | 60–135 s of 279 s | 9 real questions from the blind creator (Blind Person Query); 6 fall in the clip |
| VQA | 5_douyin_1_c/0739 | Douyin | 0–60 s of 105 s | Both query types; includes a zero-length question and an "unable to determine" answer |
| VQA | 6_youtube_c/5gtUXtawqHk | YouTube | 0–50 s of 411 s | Both query types, from a long YouTube video |
| VQA | 7_youtube_shorts_c/GkQ_kATde6o | YouTube Shorts | full 31 s | 3 simulated queries |
| VGI | 4_convert_files/043 | purpose-filmed | full 79 s | All 4 turn types, including Movement Guidance; 12 turns |
| VGI | 4_convert_files/075 | purpose-filmed | full 77 s | 4 Movement Guidance turns (only 9 exist in the whole release) |
| VGI | 4_convert_files/084 | purpose-filmed | full 75 s | 16 turns, mostly Target Manipulation |
| VGI | 4_convert_files/071 | purpose-filmed | 0–70 s of 81 s | 17 turns with 2 Completion turns. Overlapping windows. |

- **PR:** these 4 videos were picked greedily from videos ≤ 5 min so that their full records together cover all 22 PR subtask labels. Excerpt windows were then chosen to maximise the number of distinct subtasks inside a 75 s clip. The shown clips contain 20 of the 22 labels. Exit/Entry Recognition and Sign Recognition appear only in table rows marked "outside excerpt".
- **VQA:** both query types, all four platforms, and several questions per video.
- **VGI:** all four turn types, varied goals, and the rare Movement Guidance turns.

Every record's table lists all of its annotations. Rows outside the clip are dimmed.

## Files

- `index.html`: self-contained viewer with no external libraries.
- `data/proactive_reminder.json`, `data/visual_question_answering.json`, `data/vision_guided_interaction.json`: the selected records.
  - PR/VQA records are copied **verbatim**, with the original dict key added as `_viewer_key`.
  - A VGI record is the verbatim list of turns, stored under `_viewer_records`.
  - All other added keys start with `_viewer_`:
    - `_viewer_video`, `_viewer_clip_offset_s`, `_viewer_clip_end_s`
    - `_viewer_source_file`, `_viewer_source_duration_s`, `_viewer_source_bytes`, `_viewer_source_resolution`
    - `_viewer_source_platform`
    - `_viewer_source_url`, for YouTube only. It is built from `caption`, which holds the YouTube id.
    - `_viewer_other_mode_annotations`, `_viewer_note`
- `videos/<mode>_<source>.mp4`: 12 clips.
- `file_durations.json`, `full_dataset_stats.json`.

## Re-encode settings

- H.264 (libx264, `-preset slow`), with the short side scaled to 360 px and the aspect ratio kept (portrait sources come out 360×640).
- Video: `-b:v 460k -maxrate 650k -bufsize 1300k`, 30 fps, yuv420p.
- Audio: **AAC 64 kbps stereo, kept.** The creators' own speech carries the Blind Person Queries.
- `-movflags +faststart`.
- Excerpts were cut with `-ss <offset> -t <length>`.
- Result: 50–79 s clips at about 500–540 kbps total, 1.9–5.1 MB each, **about 50 MB for the whole directory**.
- Every clip passed `ffprobe` and a test decode. Every annotation shown on the timeline falls inside its clip; one PR window in 0733 is marked "partly outside".

## License and redistribution: read this

- **Annotations:** the HF dataset card carries the tag `license: mit`. There is no LICENSE file and no license text beyond that tag. The GitHub repo has no license either (the GitHub API returns `license: null`). The arXiv paper itself is CC BY 4.0, which covers the paper text, not the data.
- **Video provenance:**
  - 530 of the 600 released videos (`videos/reminder_vqa/...`) are **web-sourced**. Blind or visually impaired creators recorded or shared them on **Douyin, Bilibili and YouTube / YouTube Shorts**, and the authors found them "through keyword search and manual screening".
  - The provenance fields preserved in each record are the folder name (the platform), `video_uid`, and `caption`. `caption` is the creator's original post title with a date for Douyin/Bilibili, or the YouTube video id for YouTube. For YouTube cases the viewer derives `https://www.youtube.com/watch?v=<caption>`. The VQA case `6_youtube_c/5gtUXtawqHk` has `video_uid` `6_youtube_c/1127`, so the id lives only in `caption` and the file name.
  - The 70 VGI videos (`videos/interaction/...`) were purpose-filmed by the authors' trained annotators.
- **Redistribution status: UNCLEAR, and likely not covered by the MIT tag.**
  - The web-sourced footage belongs to the original creators. It shows real people, often in public places with bystanders visible, and has platform watermarks.
  - Neither the paper nor the dataset card documents creator consent, platform terms or a redistribution license. The paper says only that clips were chosen to "meet quality and ethical standards".
  - The MIT tag is the dataset authors' declaration and cannot grant rights they do not hold.
  - Until the authors clarify, treat the clips in `videos/` (especially the 8 PR/VQA clips) as **for internal research inspection only, not for public redistribution**.
  - The purpose-filmed VGI clips are lower-risk, but no separate license is stated for them either.
