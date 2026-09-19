"""Translate unique Devanagari words -> single English word glosses via z-ai CLI.
Output: data/gloss_map.json  {word: english_or_empty}
Function words get "" (never displayed on screen).
"""
import json
import os
import re
import subprocess
import sys
import time

BASE = "/home/z/my-project"
BATCH = 130

CONTEXT = (
    "Context: Hindi voiceover of an explainer video titled 'What architecture could AI need "
    "for AGI'. The video uses a metaphor of a surgeon (सर्जन) operating a robotic surgical "
    "system, and covers: memory (मेमरी), attention (अटेंशन), world model, planning (योजना), "
    "reasoning, tools, agents, training, neural networks, and a student learning from a teacher."
)

SYSTEM = (
    "You are a translation engine for on-screen keyword display. " + CONTEXT +
    " For each Devanagari word: give the SINGLE best English word (lowercase, letters only, "
    "no phrases, no punctuation). For function words (postpositions के को का की में से पर बाद, "
    "auxiliaries है हैं था थी हो सकता सकती गया गयी कर लिया, pronouns ये वो यह वह इस उस कुछ, "
    "conjunctions और या लेकिन तो अगर कि, particles भी ही नहीं ना ही, discourse words तो अच्छा "
    "मतलब बस तो) output empty string \"\". Keep technical loanwords accurate "
    "(मेमरी=memory, अटेंशन=attention, ट्रांसफॉर्मर=transformer, एजेंट=agent, टूल=tool). "
    "Output STRICT JSON object only, no markdown fences, mapping each input word to its result."
)


def strip_punct(w):
    return re.sub(r"[।.,!?;:\"'\-–—\(\)\[\]{}]+", "", w).strip()


def parse_json_loose(text):
    t = text.strip()
    t = re.sub(r"^```(?:json)?\s*", "", t)
    t = re.sub(r"\s*```$", "", t)
    m = re.search(r"\{.*\}", t, re.S)
    if m:
        t = m.group(0)
    return json.loads(t)


def main():
    with open(f"{BASE}/data/words.json", encoding="utf-8") as f:
        data = json.load(f)
    uniq = sorted(set(strip_punct(w["w"]) for w in data["words"]))
    uniq = [w for w in uniq if w]
    print(f"[gloss] unique clean words: {len(uniq)}")

    out_path = f"{BASE}/data/gloss_map.json"
    gloss = {}
    if os.path.exists(out_path):
        gloss = json.load(open(out_path, encoding="utf-8"))
        print(f"[gloss] resuming: {len(gloss)} already done")

    todo = [w for w in uniq if w not in gloss]
    batches = [todo[i:i + BATCH] for i in range(0, len(todo), BATCH)]
    print(f"[gloss] batches: {len(batches)}")

    for bi, batch in enumerate(batches):
        ok = False
        for attempt in range(3):
            payload = json.dumps(batch, ensure_ascii=False)
            r = subprocess.run(
                ["z-ai", "chat", "-p", "Input: " + payload, "-s", SYSTEM,
                 "-o", "/tmp/gloss_out.json"],
                capture_output=True, text=True, timeout=180)
            if r.returncode == 0 and os.path.exists("/tmp/gloss_out.json"):
                try:
                    resp = json.load(open("/tmp/gloss_out.json"))
                    content = resp["choices"][0]["message"]["content"]
                    got = parse_json_loose(content)
                    # validate
                    good = {w: str(got.get(w, "")).strip().lower()
                            for w in batch if w in got}
                    if len(good) >= len(batch) * 0.8:
                        gloss.update(good)
                        ok = True
                        break
                    print(f"[gloss] batch {bi}: only {len(good)}/{len(batch)} keys, retry")
                except Exception as e:
                    print(f"[gloss] batch {bi} parse fail: {e}")
            time.sleep(2)
        if not ok:
            print(f"[gloss] batch {bi} FAILED after retries — filling with ''")
            for w in batch:
                gloss.setdefault(w, "")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(gloss, f, ensure_ascii=False, indent=0)
        print(f"[gloss] batch {bi+1}/{len(batches)} done, total={len(gloss)}")

    n_disp = sum(1 for v in gloss.values() if v)
    print(f"[gloss] DONE: {len(gloss)} words, {n_disp} displayable, saved {out_path}")


if __name__ == "__main__":
    main()
