#!/usr/bin/env python3
"""Benchmark the reference channel: collect raw data, then measure its format.

    python3 scripts/benchmark.py fetch   [@handle]   # catalogue + thumbnails + transcripts -> data/benchmark/raw/
    python3 scripts/benchmark.py analyze [@handle]   # raw -> data/benchmark/summary.json (committed)

Sources
  * YouTube Data API v3 (YT_API_KEY): channel, uploads, titles, descriptions, tags, stats, durations.
  * i.ytimg.com: thumbnails (maxresdefault, falls back to hqdefault).
  * Supadata transcript API (SUPADATA_API_KEY): existing captions only (mode=native, 1 credit each).
    YouTube blocks transcript requests from cloud IPs; Supadata works from here. Free plan = 100/month.

Raw data (their titles, scripts, thumbnails) stays in data/benchmark/raw/ and is NOT committed
(docs/originality.md). Only the measured numbers in summary.json are committed.
"""
import argparse
import json
import os
import re
import statistics as st
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(f"{BASE}/config/channel.json", encoding="utf-8"))
RAW = f"{BASE}/data/benchmark/raw"
YT = "https://www.googleapis.com/youtube/v3"
MX = ZoneInfo(CFG["timezone"])
WD = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]


# ------------------------------------------------------------------ helpers
def yt(endpoint, **params):
    key = os.environ.get("YT_API_KEY") or sys.exit("YT_API_KEY is not set")
    q = urllib.parse.urlencode({**params, "key": key})
    with urllib.request.urlopen(f"{YT}/{endpoint}?{q}", timeout=60) as r:
        return json.load(r)


def iso_seconds(d):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    dd, h, mi, s = (int(x or 0) for x in m.groups())
    return dd * 86400 + h * 3600 + mi * 60 + s


def supadata(video_id):
    key = os.environ.get("SUPADATA_API_KEY") or sys.exit("SUPADATA_API_KEY is not set")
    q = urllib.parse.urlencode({"url": f"https://www.youtube.com/watch?v={video_id}", "lang": CFG["language"],
                                "mode": "native", "text": "false", "chunkSize": 200})
    req = urllib.request.Request(f"https://api.supadata.ai/v1/transcript?{q}", headers={"x-api-key": key})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    if "jobId" in d:
        for _ in range(60):
            time.sleep(3)
            jr = urllib.request.Request(f"https://api.supadata.ai/v1/transcript/{d['jobId']}",
                                        headers={"x-api-key": key})
            with urllib.request.urlopen(jr, timeout=60) as r:
                d = json.load(r)
            if "content" in d:
                break
        else:
            raise TimeoutError("transcript job did not finish")
    return [{"start": c["offset"] / 1000, "dur": c["duration"] / 1000, "text": c["text"]} for c in d["content"]]


def save(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


# ------------------------------------------------------------------ fetch
def fetch(handle, top, newest):
    ch = yt("channels", part="snippet,statistics,contentDetails,brandingSettings", forHandle=handle.lstrip("@"))
    ch = ch["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, token = [], None
    while True:
        r = yt("playlistItems", part="contentDetails", playlistId=uploads, maxResults=50, **({"pageToken": token} if token else {}))
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        token = r.get("nextPageToken")
        if not token:
            break
    vids = []
    for i in range(0, len(ids), 50):
        r = yt("videos", part="snippet,statistics,contentDetails", id=",".join(ids[i:i + 50]))
        for v in r["items"]:
            sn, sta = v["snippet"], v.get("statistics", {})
            vids.append({"id": v["id"], "title": sn["title"], "published_at": sn["publishedAt"],
                         "description": sn.get("description", ""), "tags": sn.get("tags", []),
                         "duration_sec": iso_seconds(v["contentDetails"]["duration"]),
                         "views": int(sta.get("viewCount", 0)), "likes": int(sta.get("likeCount", 0)),
                         "comments": int(sta.get("commentCount", 0))})
    vids.sort(key=lambda v: v["published_at"], reverse=True)
    save(f"{RAW}/catalog.json", {"handle": handle, "channel_id": ch["id"], "title": ch["snippet"]["title"],
                                 "description": ch["snippet"].get("description", ""),
                                 "keywords": ch.get("brandingSettings", {}).get("channel", {}).get("keywords", ""),
                                 "subscribers": int(ch["statistics"].get("subscriberCount", 0)),
                                 "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                 "videos": vids})
    print(f"catalogue: {len(vids)} videos")

    os.makedirs(f"{RAW}/thumbs", exist_ok=True)
    for v in vids:
        path = f"{RAW}/thumbs/{v['id']}.jpg"
        if os.path.exists(path):
            continue
        for size in ("maxresdefault", "hqdefault"):
            try:
                urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{v['id']}/{size}.jpg", path)
                break
            except Exception:
                continue
    print(f"thumbnails: {len(os.listdir(f'{RAW}/thumbs'))}")

    pick = [v["id"] for v in sorted(vids, key=lambda v: -v["views"])[:top]] + [v["id"] for v in vids[:newest]]
    pick = list(dict.fromkeys(pick))
    os.makedirs(f"{RAW}/transcripts", exist_ok=True)
    new = 0
    for vid in pick:
        path = f"{RAW}/transcripts/{vid}.json"
        if os.path.exists(path):
            continue
        try:
            save(path, {"video_id": vid, "segments": supadata(vid)})
            new += 1
            print("transcript", vid)
        except Exception as e:
            print("transcript FAILED", vid, type(e).__name__, str(e)[:120])
        time.sleep(1.2)
    print(f"transcripts: {len(os.listdir(f'{RAW}/transcripts'))} ({new} new, {new} Supadata credits)")


# ------------------------------------------------------------------ analyze
CTA = re.compile(r"suscr[ií]b|campanita|activa(r)? las notificaciones|dale like|deja(r)? (tu|un) like|este canal es nuevo", re.I)
GREET = re.compile(r"\bhola\b|bienvenid|buenas noches", re.I)
BRIDGE = re.compile(r"(esta es la (historia|verdad)|este es el (misterio|caso))\b", re.I)
TURN = re.compile(r"lo que nadie sab|nadie lo sab|pero lo que lo cambia todo|lo que (lo )?cambia todo|pero,? ¿por qu[eé]|pero bajo|pero detr[aá]s|sin embargo", re.I)
CHANGE = re.compile(r"y eso lo cambia todo|eso lo cambia todo|y aqu[ií] es donde|pero no todo|hasta que", re.I)


def words(t):
    return re.findall(r"[a-záéíóúñü0-9]+", t.lower())


def analyze_transcript(seg, dur):
    full = " ".join(s["text"] for s in seg)
    w = words(full)
    first = lambda rx, lim=None: next((round(s["start"]) for s in seg if rx.search(s["text"]) and (lim is None or s["start"] < lim)), None)
    questions = len(re.findall(r"\?", full))
    return {
        "wpm": round(len(w) / (dur / 60)) if dur else None,
        "words": len(w),
        "opens_with_date": bool(re.search(r"\b(1[5-9]\d\d|20\d\d)\b|enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre|noche|mañana", seg[0]["text"][:120], re.I)) if seg else False,
        "turn_sec": first(TURN, 90),
        "bridge_sec": first(BRIDGE, 150),
        "cta_sec": first(CTA),
        "greeting_sec": first(GREET, 180),
        "questions_per_min": round(questions / (dur / 60), 2) if dur else None,
        "change_phrase_count": len(CHANGE.findall(full)),
    }


def ngrams(tokens, n):
    return zip(*(tokens[i:] for i in range(n)))


def analyze(handle):
    cat = json.load(open(f"{RAW}/catalog.json", encoding="utf-8"))
    vids = cat["videos"]
    since = CFG["reference"].get("current_format_since", "1900-01-01")
    long = [v for v in vids if v["duration_sec"] > 180 and v["published_at"][:10] >= since]
    views = [v["views"] for v in long]
    med = st.median(views)

    # titles
    t = [v["title"] for v in long]
    left = [x.split("|")[0].strip() for x in t if "|" in x]
    hooks = {
        "superlative": r"\bm[aá]s\b|\bmayor\b|\b[uú]nic[oa]\b|\bpeor\b",
        "question": r"¿",
        "danger_fear": r"peligros|temid|oscur|terror|aterr|siniestr",
        "secret_truth": r"ocult|secret|verdad|realmente",
        "mystery": r"misterio|enigma|sin resolver|sin respuesta|nadie",
        "person_subject": r"^(el|la) (hombre|mujer|niñ[oa]|hacker|jugador|estafador)\b",
        "number": r"\d",
    }
    hook_stats = {}
    for k, p in hooks.items():
        rx = re.compile(p, re.I)
        w = [v["views"] for v in long if rx.search(v["title"].split("|")[0])]
        wo = [v["views"] for v in long if not rx.search(v["title"].split("|")[0])]
        if w and wo:
            hook_stats[k] = {"n": len(w), "share": round(len(w) / len(long), 2),
                             "lift": round(st.median(w) / st.median(wo), 2)}
    left_first = Counter(" ".join(x.split()[:2]) for x in left).most_common(12)
    right_patterns = Counter(re.sub(r"[A-ZÁÉÍÓÚÑ][\w’'.-]*(\s+[A-Z0-9][\w’'.-]*)*", "X", x.split("|", 1)[1].strip())
                             for x in t if "|" in x).most_common(8)

    # schedule
    loc = [datetime.fromisoformat(v["published_at"].replace("Z", "+00:00")).astimezone(MX) for v in long]
    dates = sorted(d.date() for d in loc)
    gaps = [(b - a).days for a, b in zip(dates, dates[1:])]

    # descriptions
    desc = [v["description"] for v in long]
    first_lines = [d.strip().split("\n")[0] for d in desc if d.strip()]
    lines = Counter(l.strip() for d in desc for l in d.split("\n") if l.strip())
    boiler = [(l, n) for l, n in lines.most_common(40) if n >= max(3, len(desc) // 5)]
    hashtags = Counter(h.lower() for d in desc for h in re.findall(r"#\w+", d)).most_common(15)
    desc_len = [len(d) for d in desc]
    question_lines = [l for d in desc for l in d.split("\n") if "¿" in l and ("coment" in l.lower() or "💬" in l)]

    # tags
    tags = Counter(x.lower() for v in long for x in v["tags"])
    tag_n = [len(v["tags"]) for v in long]

    # transcripts
    tr = {}
    for v in long:
        p = f"{RAW}/transcripts/{v['id']}.json"
        if os.path.exists(p):
            seg = json.load(open(p, encoding="utf-8"))["segments"]
            tr[v["id"]] = {"title": v["title"], "views": v["views"], **analyze_transcript(seg, v["duration_sec"])}
    tv = list(tr.values())
    def med_of(k):
        xs = [x[k] for x in tv if x[k] is not None]
        return st.median(xs) if xs else None
    # signature phrases (repeated 4-grams across >= 30% of their scripts) -> banned for originality
    docs = []
    for vid in tr:
        seg = json.load(open(f"{RAW}/transcripts/{vid}.json", encoding="utf-8"))["segments"]
        docs.append(set(ngrams(words(" ".join(s["text"] for s in seg)), 4)))
    df = Counter(g for d in docs for g in d)
    stop4 = {"de la", "en el", "que se", "de los"}
    signature = [(" ".join(g), n) for g, n in df.most_common(400)
                 if n >= max(3, round(0.3 * len(docs))) and not all(w in {"de", "la", "el", "que", "en", "y", "a", "los", "las", "se", "un", "una", "del", "por", "con", "no", "lo", "es", "su", "al"} for w in g)][:40]

    summary = {
        "handle": handle, "channel": cat["title"], "subscribers": cat["subscribers"],
        "analyzed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "format_since": since,
        "videos": {"total": len(vids), "current_format": len(long), "median_views": med,
                   "duration_min": {"median": round(st.median(v["duration_sec"] for v in long) / 60, 1),
                                    "p25": round(sorted(v["duration_sec"] for v in long)[len(long) // 4] / 60, 1),
                                    "p75": round(sorted(v["duration_sec"] for v in long)[3 * len(long) // 4] / 60, 1)}},
        "titles": {"pipe_share": round(sum("|" in x for x in t) / len(t), 2),
                   "len_median": st.median(len(x) for x in t), "len_p90": sorted(len(x) for x in t)[int(.9 * len(t))],
                   "left_words_median": st.median(len(x.split()) for x in left),
                   "question_share": round(sum("¿" in x for x in t) / len(t), 2),
                   "emoji_share": round(sum(bool(re.search(r"[\U0001F300-\U0001FAFF]", x)) for x in t) / len(t), 2),
                   "allcaps_word_share": round(sum(bool(re.search(r"\b[A-ZÁÉÍÓÚÑ]{4,}\b", x)) for x in t) / len(t), 2),
                   "hooks": hook_stats, "left_openers": left_first, "right_patterns": right_patterns},
        "schedule": {"weekday": dict(Counter(WD[d.weekday()] for d in loc)),
                     "hour_median": st.median(d.hour for d in loc),
                     "gap_days_median": st.median(gaps) if gaps else None},
        "description": {"len_median": st.median(desc_len), "boilerplate_lines": boiler, "hashtags": hashtags,
                        "paragraphs_median": st.median(len([b for b in d.split("\n\n") if b.strip()]) for d in desc),
                        "subscribe_line_share": round(sum(bool(re.search(r"suscr[ií]b", d, re.I)) for d in desc) / len(desc), 2),
                        "share_with_comment_question": round(sum(any("¿" in l and ("coment" in l.lower() or "💬" in l) for l in d.split("\n")) for d in desc) / len(desc), 2)},
        "tags": {"per_video_median": st.median(tag_n), "common": tags.most_common(15)},
        "transcripts": {"n": len(tv), "wpm_median": med_of("wpm"),
                        "opens_with_date_share": round(sum(x["opens_with_date"] for x in tv) / len(tv), 2) if tv else None,
                        "turn_sec_median": med_of("turn_sec"), "bridge_sec_median": med_of("bridge_sec"),
                        "bridge_found_share": round(sum(x["bridge_sec"] is not None for x in tv) / len(tv), 2) if tv else None,
                        "cta_share": round(sum(x["cta_sec"] is not None for x in tv) / len(tv), 2) if tv else None,
                        "greeting_share": round(sum(x["greeting_sec"] is not None for x in tv) / len(tv), 2) if tv else None,
                        "questions_per_min_median": med_of("questions_per_min"),
                        "change_phrase_per_video_median": med_of("change_phrase_count"),
                        "signature_4grams": signature,
                        "per_video": tr},
    }
    save(f"{BASE}/data/benchmark/summary.json", summary)
    # their wording stays in raw/ (not committed): first sentences, endings, description samples
    samples = {"description_first_lines": first_lines, "comment_question_lines": question_lines, "scripts": {}}
    for v in long:
        p = f"{RAW}/transcripts/{v['id']}.json"
        if os.path.exists(p):
            seg = json.load(open(p, encoding="utf-8"))["segments"]
            samples["scripts"][v["id"]] = {"title": v["title"],
                                           "opening_120s": " ".join(x["text"] for x in seg if x["start"] < 120),
                                           "ending": " ".join(x["text"] for x in seg[-4:])}
    save(f"{RAW}/text_samples.json", samples)
    s = summary
    print(json.dumps({k: s[k] for k in ("videos", "schedule", "tags")}, ensure_ascii=False, indent=1))
    print(json.dumps({k: v for k, v in s["titles"].items()}, ensure_ascii=False)[:1500])
    print(json.dumps({k: v for k, v in s["description"].items()}, ensure_ascii=False)[:2500])
    print(json.dumps({k: v for k, v in s["transcripts"].items() if k != "per_video"}, ensure_ascii=False)[:2500])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["fetch", "analyze"])
    ap.add_argument("handle", nargs="?", default=CFG["reference"]["handle"])
    ap.add_argument("--top", type=int, default=15, help="transcripts for the N most viewed videos")
    ap.add_argument("--newest", type=int, default=10, help="transcripts for the N newest videos")
    a = ap.parse_args()
    fetch(a.handle, a.top, a.newest) if a.cmd == "fetch" else analyze(a.handle)


if __name__ == "__main__":
    main()
