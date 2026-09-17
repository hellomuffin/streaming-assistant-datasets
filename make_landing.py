import os, html
R = os.path.dirname(os.path.abspath(__file__))
ENTRIES = [
 ("training-data", "Proactive-assistant training data", "Findings on newer benchmarks, leading models and how their training data was annotated, plus a timeline viewer of real training records: EgoProactive, Ambient synthetic labels, ProAssist, JoyAI-VL-Interaction, MMDuet2, LiveCC, ROMA, Gander."),
 ("joyai-interaction", "JoyAI-VL-Interaction training data", "27 real training records from the 3.02M-record release, sorted into its six families: proactive alerting, time-aligned QA, counting over time, commentary, casual chat, and delegation to a background model (arXiv 2606.14777)."),
 ("streamarena", "StreamArena", "Hour-long YouTube streams with human-written real-time, retrospective, tool-use and proactive questions (arXiv 2608.05703)."),
 ("viabench", "VIABench", "Egocentric video from blind users: proactive reminders with alert windows, online VQA and guided interaction (arXiv 2607.14660)."),
 ("guideme", "GuideMe", "Streaming task guidance: instruction, completion feedback, error detection and correction on HoloAssist, CaptainCook4D, EgoPER, QEVD (arXiv 2607.02991)."),
 ("omniassistbench", "OmniAssistBench", "Assistant-style omni interaction with spoken, gestured and handwritten questions, proactive responses and process tracking (arXiv 2608.21360)."),
]
rows = []
for slug, name, desc in ENTRIES:
    if not os.path.exists(os.path.join(R, slug, "index.html")): continue
    rows.append(f'<a class="card" href="{slug}/"><h2>{html.escape(name)}</h2><p>{html.escape(desc)}</p><span>Open viewer &rarr;</span></a>')
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Streaming Assistant Dataset Samples</title>
<style>
:root{{--bg:#0f1419;--panel:#1a2129;--border:#2d3640;--text:#e6e9ed;--muted:#8a949e;--accent:#4dabf7}}
body{{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:14px;line-height:1.5}}
header{{padding:20px;border-bottom:1px solid var(--border);background:var(--panel)}}
h1{{margin:0;font-size:20px;color:var(--accent)}} header p{{margin:6px 0 0;color:var(--muted);max-width:80ch}}
main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;padding:20px}}
.card{{display:flex;flex-direction:column;gap:6px;background:var(--panel);border:1px solid var(--border);border-radius:6px;padding:16px;color:var(--text);text-decoration:none}}
.card:hover{{border-color:var(--accent)}} .card h2{{margin:0;font-size:16px}} .card p{{margin:0;color:var(--muted)}} .card span{{color:var(--accent);font-size:12px;margin-top:auto}}
</style></head><body>
<header><h1>Streaming / proactive assistant datasets — sample viewers</h1>
<p>Small representative samples of benchmarks and training sets for real-time proactive video assistants, re-encoded to 360p, with every annotation shown on a clickable timeline. Each viewer links to the original dataset, paper and license.</p></header>
<main>{"".join(rows)}</main></body></html>'''
open(os.path.join(R, "index.html"), "w").write(page)
print(len(rows), "entries")
