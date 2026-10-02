import re
from collections import Counter


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def exact_match(prediction: str, reference: str) -> float:
    return 1.0 if normalize_text(prediction) == normalize_text(reference) else 0.0


def character_error_rate(prediction: str, reference: str) -> float:
    p, r = list(prediction or ""), list(reference or "")
    if not r:
        return 0.0 if not p else 1.0
    prev = list(range(len(r) + 1))
    for i, pc in enumerate(p, 1):
        cur = [i]
        for j, rc in enumerate(r, 1):
            cur.append(min(cur[j - 1] + 1, prev[j] + 1, prev[j - 1] + (pc != rc)))
        prev = cur
    return prev[-1] / len(r)


def cer_score(prediction: str, reference: str) -> float:
    return max(0.0, 1.0 - character_error_rate(prediction, reference))


def token_f1(prediction: str, reference: str) -> float:
    p = Counter(normalize_text(prediction).split())
    r = Counter(normalize_text(reference).split())
    overlap = sum((p & r).values())
    if not p or not r:
        return 1.0 if not p and not r else 0.0
    precision = overlap / sum(p.values())
    recall = overlap / sum(r.values())
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def bbox_iou(a: dict, b: dict) -> float:
    ax1, ay1, ax2, ay2 = a["x"], a["y"], a["x"] + a["width"], a["y"] + a["height"]
    bx1, by1, bx2, by2 = b["x"], b["y"], b["x"] + b["width"], b["y"] + b["height"]
    ix1, iy1, ix2, iy2 = max(ax1, bx1), max(ay1, by1), min(ax2, bx2), min(ay2, by2)
    inter = max(0, ix2 - ix1) * max(0, iy2 - iy1)
    union = a["width"] * a["height"] + b["width"] * b["height"] - inter
    return inter / union if union else 0.0


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0
