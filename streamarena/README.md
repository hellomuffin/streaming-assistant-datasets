# StreamArena sample viewer

StreamArena (arXiv 2608.05703; HKUST, Xiaohongshu, HKU, CUHK) tests streaming video assistants on hour-long YouTube videos. It has 243 videos (52 to 134 min, about 360 h) and 3,646 open-ended questions. Each video's questions are asked at different times and form one multi-turn thread. There are four question families:

| qtype | Family | # | What the model must do |
|---|---|---:|---|
| RTP | Real-time perception | 263 | Answer from the current frame or the last few seconds of audio |
| HR | Historical retrospection | 877 | Answer from earlier content, marked by `evidence_ts_sec`. Layers by gap: L1 ≤5 min, L2 5–15, L3 15–30, L4 >30 min |
| Tool | Tool use | 1,732 | Start from what is seen or heard, then use web or image search |
| Pro | Proactive interaction | 774 | Register a "tell me when…" request at `ask_sec`, then alert at `ref_sec` (t_gt). A case counts only if the first alert lands in [t_gt − 0.5 s, t_gt + 2 s] and the content is judged correct. Layers by wait: L1 ≤30 s, L2 30 s–4 min, L3 >4 min |

Open `index.html` over http (`python3 -m http.server`). The page has a family selector (RTP / HR / Tool / Pro), a case selector, Prev/Next buttons and the ←/→ keys (these move across families). You can deep-link a case with `#fam=HR&i=0`.

## Subset: 12 cases, 3 per family, from 5 videos

| case | video (domain, language) | qid | why |
|---|---|---|---|
| rtp_peppa_q1 | jvEuEu65YE8 (Film & TV / Anime, zh) | 1 | Visual RTP. The window also holds the next thread turn, Tool q2 |
| rtp_dongyuhui_q1 | wrHVgPEdN5g (E-commerce Live, zh) | 1 | RTP answerable from Mandarin speech only |
| rtp_guoyu_q15 | Prb_YPSdzH4 (Conference & Interview, zh) | 15 | RTP that needs both speech and the on-screen slide |
| tool_gwanghwamun_q4 | T3BaW1jD4dc (First-Person POV, zh) | 4 | Egocentric walk. Identify the film on a billboard, then search |
| tool_qianwen_q4 | ajP9V6AbEAM (Launch Event, zh+en) | 4 | Tool plus memory: "PPT" at 1:12, "Office" at 5:16. Two excerpts |
| tool_guoyu_q5 | Prb_YPSdzH4 | 5 | Tool plus memory of speech (5:49 → 7:46). Two excerpts |
| hr_dongyuhui_q14 | wrHVgPEdN5g | 14 | Multi-evidence HR (3 moments). Three evidence excerpts plus the ask |
| hr_peppa_q8 | jvEuEu65YE8 | 8 | Visual HR, L2 (302 s gap). Two excerpts |
| hr_guoyu_q13 | Prb_YPSdzH4 | 13 | Spoken-evidence HR, L2 (339 s gap). Two excerpts |
| pro_peppa_q3 | jvEuEu65YE8 | 3 | Pro L1, 11 s wait, visual event |
| pro_gwanghwamun_q11 | T3BaW1jD4dc | 11 | Pro L1, 16 s wait, egocentric action (starts crossing) |
| pro_qianwen_q9 | ajP9V6AbEAM | 9 | Pro L2, 33 s wait, speaker change |

How the cases were chosen. The goals were: every family appears 3 times; 5 of the 8 L1 domains are covered; evidence comes from vision, from speech, or from both; HR includes a multi-evidence item; Pro covers L1 and L2. Among videos that satisfy this, the ones with the smallest tars were used (5 tars, about 1.8 GB downloaded). Pro L3 (wait longer than 4 min) and HR L3/L4 are not included, because a faithful excerpt would exceed the size budget. The whole thread for each video is still listed in the page and stored in the JSON.

**Excerpts and the time mapping.** The source videos are 63–91 min long, so each case uses one or more excerpts. HR and memory-dependent Tool cases use separate short excerpts around each evidence moment and around the ask moment, joined in one mp4. Dashed lines on the timeline mark the cuts. `_viewer_clip_segments` lists `{src_start, src_end, clip_start, clip_end}`. Within a segment, clip time = t − src_start + clip_start. For the first segment this is `t − _viewer_clip_offset_s`. All annotation times stay in original seconds, and the page shows the original and clip times side by side. Every annotated moment of each selected question (ask, ref and all evidence) falls inside its clip; this was checked by script. Other thread questions whose moments happen to fall inside a clip are also shown, faded.

## Files
- `data/streamarena.json` — the 12 records. Each is the verbatim record from `question.en.jsonl` (the 14 original fields) plus these keys: `_viewer_case_id`, `_viewer_video`, `_viewer_clip_offset_s`, `_viewer_clip_segments`, `_viewer_note`, `_viewer_record_zh` (the verbatim record from `question.jsonl`), `_viewer_video_meta_en` / `_zh` (verbatim `video_meta` rows), and `_viewer_thread_en` / `_zh` (every question of that video, verbatim).
- `videos/<case>.mp4`, `file_durations.json`, `full_dataset_stats.json` (computed from all 3,646 questions and 243 video rows).

## Re-encode settings
The encoder was ffmpeg with libx264 (preset slow, High profile). Video: short side 360 px, 25 fps, 520 kbps target (700 kbps max), GOP 50. Audio: AAC 64 kbps stereo; the original audio is kept because most speech is Mandarin. Other settings: `-movflags +faststart`; chapters and metadata stripped. The 12 clips run 32–84 s and are 2.4–6.1 MB each; the whole directory is about 43 MB.

The sources are the HF tar members `videos/<id>.tar → <id>/<id>.mp4`. Two sources are portrait, not ≥1080p as the paper states: T3BaW1jD4dc is 360×640 and wrHVgPEdN5g is 720×1036.

## Findings in the full annotation files
- **HR `horizon_sec` does not always follow the dataset card.** For all 250 HR items with more than one evidence moment, `horizon_sec` = ask_sec − **max**(evidence), not ask − min. As a result, hr_dongyuhui_q14 is labelled L1 (37 s) although its first evidence is 20 min before the ask.
- 23 HR items have evidence after `ask_sec`, which makes the horizon negative. 2 Pro items have `ref_sec` ≤ `ask_sec`.
- 24 cumulative-count HR items use evidence `[0, ask_sec]`.
- The dataset card lists 8 L1 domains, including Security & Surveillance (1 video). The paper counts 7 domains.

## License and redistribution
- **Annotations** (`*.jsonl`): the HF dataset card says CC-BY-NC-4.0. The paper text says CC BY 4.0 and the GitHub README says Apache-2.0 (code). The strictest reading is CC-BY-NC-4.0: non-commercial use, with attribution to Zhang et al. 2026, arXiv 2608.05703.
- **Videos**: these are YouTube uploads whose copyright stays with the original uploaders (the channels are listed in `video_meta`). The authors host them on HF "under fair-use for research reproducibility (non-commercial)", with a takedown route; the paper itself says raw videos are not redistributed. **No license grants redistribution of the video content.** The clips here are short excerpts re-encoded for internal research viewing. Treat them as not cleared for public redistribution. Before hosting publicly, replace them with YouTube links or embeds at the original timestamps (`video_meta.url` plus `ask_sec`), or get permission.
