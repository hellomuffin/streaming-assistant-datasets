# GuideMe sample viewer (12 of the 50 released preview videos)

GuideMe ("Multi-Domain Task Guidance and Intervention in Streaming Video", arXiv 2607.02991, ECCV 2026; City University of Hong Kong, Huawei Research, USTC, CUHK) tests whether a video LLM can coach a user through a task as the video streams. At each queried time the model either answers `Silent` or speaks one of four outputs: a next-step instruction, completion feedback, error detection or corrective guidance.

- Paper: https://arxiv.org/abs/2607.02991 (CC BY 4.0)
- Code: https://github.com/fawnliu/GuideMe (no LICENSE file)
- Data: https://huggingface.co/datasets/alisn/GuideMe_Test_Subset50 (the only public data)
- Project: https://fawnliu.github.io/project/guideme/

Open the viewer with `python3 -m http.server` in this directory. It loads its data with `fetch()`, so it will not work from `file://`.

## What was released

The full benchmark has 2,458 videos, 223.7 h and 47,775 samples. It is **not released**. The authors published only a 50-video **test preview**:

- `annotation_test_subset50.json` is a JSON list of 50 records with `video_id`, `videos` and `conversations[]`. Each conversation turn has `from` (user|assistant), `value` and `timestamp` (integer seconds). There are 50 user queries and 1,095 assistant turns.
- `videos_2fps/*.mp4` holds all 50 source videos, already reduced to 2 fps (H.265).
  - CaptainCook4D files are 640x360 with audio.
  - EgoPER files are 1280x720 and mostly have no audio.
  - QEVD files are 640x360 with no audio. Their frames are sideways and carry no rotation flag.

The preview has 20 CaptainCook4D, 17 EgoPER, 13 QEVD-Fit-Coach and **0 HoloAssist** videos, even though HoloAssist is 68% of the full benchmark. The records have **no output-type label** and no source/domain field. For this viewer:

- The source dataset was derived from the file-name pattern.
- The four output types were assigned by hand for the 12 shown cases (`_viewer_output_types`).
- A keyword heuristic labelled all 50 videos for the stats (`_viewer_output_types_heuristic`). It matches the hand labels exactly on 223 of 252 turns (88%). It was tuned on those same turns, so its accuracy on the other 38 videos is probably lower.

## Files

- `index.html` is the self-contained viewer.
- `data/guideme_subset.json` holds the 12 original records, copied verbatim. Only `_viewer_*` keys were added:
  - `_viewer_source`, `_viewer_task`
  - `_viewer_video`, `_viewer_clip_offset_s`, `_viewer_clip_duration_s`, `_viewer_source_duration_s`
  - `_viewer_output_types` (hand labels), `_viewer_output_types_heuristic`, `_viewer_note`
- `videos/<file>.mp4` has one video per case.
- `file_durations.json` gives the clip durations.
- `full_dataset_stats.json` has two parts:
  - Stats over **all 50 preview records**: sources, durations, turn gaps, utterance lengths, heuristic type counts, estimated anchor and dense query counts, and per-video rows.
  - A separate `paper_full_benchmark` block with the paper's own numbers for the unreleased full benchmark.

## Case selection (12)

The selection covers the three sources in the preview and all four output types. Most cases were chosen because their dialogue contains error detection and correction.

| Source | Case | Why |
|---|---|---|
| QEVD-Fit-Coach | 0012, 0033, 0056 | These have the most wrong-limb, not-exercising and form-error detections. The coach lines appear to be the original QEVD live-coach feedback. |
| CaptainCook4D | 8_45 (spiced hot chocolate) | Nearly every step is followed by an error: spill, wrong ingredient, wrong quantity or wrong power. |
| CaptainCook4D | 27_49 (pimiento cheese) | Spills, hands used instead of a utensil, a skipped step and a wrong ingredient. The clip is an excerpt, 150–510 s. |
| CaptainCook4D | 29_37 (caprese bruschetta) | Order errors, each followed by guidance back to the task graph. The clip is an excerpt, 325–685 s. |
| CaptainCook4D | 1_143 (egg sandwich) | The densest error sequence in the preview. The clip is an excerpt, 40–400 s. |
| EgoPER | oatmeal/pinwheels/quesadilla/tea `_error_` recordings | Covers all four EgoPER error tasks: wrong bowl, fold instead of roll, dropped tortilla, wrong mug. |
| EgoPER | coffee_u1_a7_normal_016 | A normal recording with no errors, included for contrast. The clip is an excerpt, 0–360 s. |

The viewer does not show a HoloAssist case because the preview contains no HoloAssist record.

## Video processing

The inputs are the preview's own 2 fps files. The HF release already provides these videos, so nothing was fetched from the source datasets. They were re-encoded with:

`ffmpeg [-ss off -t 360] -vf scale=-2:360 -c:v libx264 -preset slow -crf 32 -g 20 -r 2 -pix_fmt yuv420p -c:a aac -b:a 32k -ac 1 -movflags +faststart`

- Frame rate stays at 2 fps. That is what the benchmark models see, and higher rates cannot be recovered.
- Where a source has audio it was kept, but as 32 kbps mono rather than 64 kbps. Most of these videos are long, and this was needed to stay under the 55 MB directory budget.
- Sources longer than 8 min were cut to a 360 s excerpt that contains the error-dense part. Annotation times stay in source seconds; clip time = `timestamp - _viewer_clip_offset_s`.
- The QEVD videos were left sideways, as shipped.

## Licenses and redistribution

- **Annotations:** the HF dataset card and the GitHub repo state **no license**. The paper (arXiv) is CC BY 4.0, but that license covers the paper, not the data. The dialogue text was generated by an LLM from the source datasets' annotations. The QEVD lines appear to be the original coach feedback.
- **Videos:** the files are frames from the source datasets, re-hosted by the GuideMe authors:
  - CaptainCook4D: Apache-2.0 per its GitHub repo.
  - EgoPER: research use, distributed by its authors.
  - QEVD-Fit-Coach (Qualcomm): distributed under Qualcomm's research license, which requires accepting terms.

  The GuideMe authors re-host all 50 without stating terms.
- **Redistribution:** it is **not clearly permitted**. No license grants it for the GuideMe annotations, and EgoPER and QEVD normally require their own agreements. This viewer is intended for internal, non-public preview only. Before any public hosting, confirm with the GuideMe authors, or replace the EgoPER and QEVD clips with "video not included" placeholders; the page already falls back to one when a file is missing.
