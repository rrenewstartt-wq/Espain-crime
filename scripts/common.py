"""Shared helpers: config, script parsing, text utilities, check reporting."""
import json
import os
import re
import unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FMT = json.load(open(f"{BASE}/config/format.json", encoding="utf-8"))
CHANNEL = json.load(open(f"{BASE}/config/channel.json", encoding="utf-8"))
RAW = f"{BASE}/data/benchmark/raw"


def fold(text):
    """Lowercase and strip accents, for accent-insensitive matching."""
    t = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def words(text):
    return re.findall(r"[a-záéíóúñü0-9]+", text.lower())


def sentences(text):
    """Split narration into sentences; keeps ¿…? questions whole."""
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?…])\s+(?=[¿¡A-ZÁÉÍÓÚÑ0-9\"“])", text)
    return [p.strip() for p in parts if p.strip()]


def load_script(path):
    """Parse episodes/<ep>/script.md -> (meta, [(act_id, [sentences])]).

    Lines starting with '>' are screen notes, '[^n]' are footnote markers: both are dropped.
    """
    raw = open(path, encoding="utf-8").read()
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.split("#")[0].strip().strip('"').strip("'")
        raw = raw[m.end():]
    acts, cur = [], None
    for line in raw.splitlines():
        h = re.match(r"^##\s+([\w-]+)", line)
        if h:
            cur = (h.group(1).lower(), [])
            acts.append(cur)
            continue
        if cur is None or not line.strip() or line.lstrip().startswith(">") or line.startswith("#"):
            continue
        cur[1].append(line.strip())
    out = []
    for act, lines in acts:
        text = re.sub(r"\[\^[\w-]+\]", "", " ".join(lines))
        out.append((act, sentences(text)))
    return meta, out


def narration_text(acts):
    return " ".join(s for _, ss in acts for s in ss)


def ngrams(tokens, n):
    return set(zip(*(tokens[i:] for i in range(n))))


class Report:
    """Collects PASS / WARN / FAIL lines and prints a table."""

    def __init__(self, title):
        self.title, self.rows = title, []

    def add(self, level, check, detail=""):
        self.rows.append((level, check, detail))

    def ok(self, cond, check, detail="", fail="FAIL"):
        self.add("PASS" if cond else fail, check, detail)
        return cond

    @property
    def failed(self):
        return any(r[0] == "FAIL" for r in self.rows)

    def print(self, as_json=False):
        if as_json:
            print(json.dumps({"title": self.title, "failed": self.failed,
                              "rows": [dict(zip(("level", "check", "detail"), r)) for r in self.rows]},
                             ensure_ascii=False, indent=1))
            return
        icon = {"PASS": "✅", "WARN": "⚠️ ", "FAIL": "❌"}
        print(f"\n{self.title}")
        for lvl, chk, det in self.rows:
            print(f"  {icon[lvl]} {chk}" + (f" — {det}" if det else ""))
        n = {k: sum(r[0] == k for r in self.rows) for k in ("PASS", "WARN", "FAIL")}
        print(f"  → PASS {n['PASS']} · WARN {n['WARN']} · FAIL {n['FAIL']}")
