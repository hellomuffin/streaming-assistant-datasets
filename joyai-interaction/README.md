# JoyAI-VL-Interaction training-data viewer

JoyAI-VL-Interaction is JD's streaming-interaction model (arXiv 2606.14777).
- Dataset: HF `jdopensource/JoyAI-VL-Interaction`, Apache-2.0, annotations only.
- Size: 9 JSON files, **3,018,207 records**.
- Record schema: `{video_name, task_type, source, question[{content,time}], response[{content,time}] | response[[...],...]}`.
  - Times are integer seconds stored as strings.
  - An alert `time` can be a comma list of every positive second.
  - Silence is implicit: every second without a listed turn.

This directory is a **27-case sample** of that training data (this is not a benchmark). Open it through `python3 -m http.server`.

## Layout
- `index.html`: the viewer.
- `data/f1_alerting.json` … `data/f6_delegation.json`: the sample records.
  - Records are **verbatim**, with added `_viewer_*` keys: family, subtype, timing class, release file and index, language, classification evidence, evidence second, clip offset, video provenance.
  - Chinese records also carry `_viewer_gloss_en`, an English translation written by the viewer author. It is not part of the dataset.
- `videos/*.mp4`: 21 clips.
- `file_durations.json`
- `full_dataset_stats.json`: statistics computed over all 3,018,207 records.

## Six families: how records were classified
The release's `task_type` values (chat / event_grounding / narration / background) do not map 1:1 onto the paper's six families. Rules are applied in order and the first match wins. They are heuristics written from the paper §3.2 definitions and from the record evidence.

1. **Delegation (6)**: any response contains `</delegation>`. The subtype comes from the holding reply before the token:
   - "合适的工具 / appropriate tool" → tool/API call
   - "图像编辑/生成工具" → image tool
   - "我帮你查一下" in chat → search look-up
   - Molmo2 source with a holding reply that does not mention a background model → video-grounded knowledge
   - code words → code generation
   - writing words → writing/expert text
   - otherwise → STEM/text problem
2. Empty record → unclassified.
3. **Alerting (1)**: `event_grounding`, or source `ucfcrime`.
4. **Commentary (4)**: `narration`.
5. **Counting & time (3)**: either of:
   - TransRAC source or "Nth repetition" replies
   - in the chat pipeline, timing instructions: count every n s, Q&A timer window, wait/hold N s, or VideoGPT-plus "how long did it last"
6. **Commentary / guidance (4)**: assembly101 / holoassist / epickitchens / ego4d, or egoexolearn with a goal statement. This is a judgment call, because the paper has no guidance family.
7. Unclassified: bare arithmetic questions.
8. **Casual chat (5)**: a chat record with ≥2 non-template questions.
   - EgoIT with ≥50% exclamatory/warm replies → companionship.
   - Other EgoIT or ego sources → everyday egocentric conversation.
   - YouTube/Bilibili URL → long-video dialogue.
9. **Time-aligned QA (2)**: the rest.
   - Forward: the first answer comes after the question.
   - Backward: answered at once, with "just now / 刚才 / 回想…" wording.
   - Present: answered at once, with "now / 现在 / 正在" wording.
   - Otherwise: at-question (undetermined).

Counts over the full release:

| family | records |
|---|---|
| 1 alerting | 247,390 |
| 2 time-aligned QA | 1,750,643 |
| 3 counting & time perception | 141,319 |
| 4 commentary & narration (incl. 41,634 guidance) | 308,920 |
| 5 casual chat | 129,249 |
| 6 delegation | 400,244 |
| unclassified: arithmetic 40,116 + empty 326 | 40,442 |

Subtype counts are in `full_dataset_stats.json`.

## Sample selection
- Every family has 4–6 cases, covering every subtype except family 4 "LLM-styled commentary" (Molmo2, YouTube-only) and family 6 "code generation".
- Family 2 includes one case of each timing class.
- Family 5 includes each chat style.
- Family 6 shows the delegation token and hidden query exactly as stored.
- Cases whose video could be fetched were preferred.

## Videos: provenance and licenses
- Sources:
  - **HF-hosted:** GUI-World, OmniStar-RNG, EgoLife, RepCountA lance (TransRAC), and TimeLens-100K (DiDeMo shard, first 900 MB streamed).
  - **HF zip members read by HTTP range:** Vript, UCF-Crime mirror `jinmang2/ucf_crime`, CCTV-Fights mirror `34data/video-fights`.
  - **Bilibili:** sections downloaded with yt-dlp.
- Unavailable (placeholders):
  - YouTube is blocked by a bot check from this cluster (Live-WhisperX, Molmo2).
  - WebVid (VideoGPT-plus) was withdrawn.
  - Assembly101 and HoloAssist-derived EgoIT clips are license-gated and were deliberately not fetched.
  - The Charades-Ego-derived EgoIT interval clip is not published.
- Re-encoding:
  - H.264, short side 360, source audio kept as AAC 64 kbps, `+faststart`.
  - Video bitrate: 420 kbps for clips ≤60 s, 300 kbps for ≤120 s, 230 kbps above that.
  - Two excerpts: `F3-timedwindow-bili` has offset 4 s and `F5-longvideo-bili-zh` has offset 51 s. Every annotation tick falls inside its clip.
- **Redistribution:** the Apache-2.0 license covers JD's annotation text only. Each clip keeps its source's terms:
  - Bilibili: uploader copyright.
  - UCF-Crime and CCTV-Fights: research use.
  - Vript: academic use.
  - EgoLife and GUI-World: dataset cards.
  - DiDeMo: Flickr CC.
  
  The clips are **not** cleared for public redistribution. Keep this viewer private.

## Findings worth knowing
- Delegation:
  - 445,628 responses (4.3% of all) carry `</delegation>`.
  - 99.9% are emitted in the same second as the question.
  - 91% of hidden queries copy the question verbatim.
  - 9.4% of questions explicitly ask for the background model (writing/code >90%).
  - The release stores **no returned result or final answer** turns.
- No distinct "video reasoning problem" delegation group was found.
- The evidence second for backward and present QA is not stored.
- The `ThePolyMath/UCF-Crime-Dataset` mirror is truncated: Abuse023 is 17 s there versus 33 s in the original, so the original was used instead.
