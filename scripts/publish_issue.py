#!/usr/bin/env python3
"""Weekly Meta Ads Intel auto-publish.

Fetches active fitness coaching ads from the Meta Ad Library, sends them to
Claude, asks for a structured issue JSON matching the issues.json schema,
prepends the new issue and saves the file. The GitHub Action commits and
pushes the updated issues.json and purges the jsDelivr CDN.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
from anthropic import Anthropic

REPO_ROOT = Path(__file__).resolve().parent.parent
ISSUES_PATH = REPO_ROOT / "issues.json"

META_TOKEN = os.environ["META_ACCESS_TOKEN"]
ANTHROPIC_KEY = os.environ["ANTHROPIC_API_KEY"]
NICHE = os.environ.get("NICHE", "Fitness Coaching")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-6")

SEARCH_TERMS = [
    "online fitness coaching",
    "personal trainer program",
    "fitness transformation program",
]
META_API = "https://graph.facebook.com/v25.0/ads_archive"
COUNTRIES = ["US"]
LIMIT = 50


def fetch_ads():
    """Pull active ads from Meta Ad Library across multiple search terms."""
    all_ads = []
    for term in SEARCH_TERMS:
        params = {
            "access_token": META_TOKEN,
            "search_terms": term,
            "ad_reached_countries": json.dumps(COUNTRIES),
            "ad_active_status": "ACTIVE",
            "fields": (
                "ad_creative_bodies,ad_creative_link_titles,"
                "ad_delivery_start_time,page_name,ad_snapshot_url"
            ),
            "limit": LIMIT,
        }
        try:
            r = requests.get(META_API, params=params, timeout=60)
            r.raise_for_status()
            data = r.json().get("data", [])
            print(f"[meta] {term}: {len(data)} ads", flush=True)
            for ad in data:
                ad["_search_term"] = term
            all_ads.extend(data)
        except Exception as e:
            print(f"[meta] {term} failed: {e}", flush=True)
    return all_ads


def slim_ads(ads, cap=80):
    """Keep only signal-rich fields, cap total volume to keep prompt small."""
    seen = set()
    out = []
    for ad in ads:
        bodies = ad.get("ad_creative_bodies") or []
        body = bodies[0] if bodies else ""
        if not body:
            continue
        key = (ad.get("page_name", ""), body[:120])
        if key in seen:
            continue
        seen.add(key)
        titles = ad.get("ad_creative_link_titles") or []
        out.append({
            "page": ad.get("page_name", ""),
            "started": ad.get("ad_delivery_start_time", "")[:10],
            "title": (titles[0] if titles else "")[:200],
            "body": body[:600],
            "term": ad.get("_search_term", ""),
        })
        if len(out) >= cap:
            break
    return out


def build_prompt(ads, issue_num, issue_date):
    schema_example = {
        "num": issue_num,
        "date": issue_date,
        "slug": f"fitness-{issue_date}",
        "title": "Short punchy title without a colon, max 90 chars",
        "summary": "One sentence summary used in the archive grid card, max 200 chars",
        "tags": ["Fitness Coaching", "Tag2", "Tag3"],
        "featuredTitle": "Meta Ads Weekly Brief - Fitness Coaching",
        "featuredDesc": "<strong>One bold lead</strong> with one or two key data points wrapped in <strong> tags",
        "featuredMeta": ["7 min read", "X hooks - Y angles", "3 ad ideas inside", "100+ advertisers"],
        "insight": "Single sentence headline insight for the featured card",
        "insightFooter": "Stat 1 - Stat 2",
        "contentHtml": "FULL HTML of the brief, see structure rules below"
    }

    html_rules = """
contentHtml structure (must match exactly, use the same CSS class names and tags):

<div class="brief-hero">
  <div class="brief-eyebrow">Report 00N - Week of MMM DD-DD - Fitness Coaching - X min read</div>
  <h1>Meta Ads Weekly Brief - Fitness Coaching</h1>
  <div class="brief-meta">
    <div><strong>Date</strong> - MMM DD, YYYY</div>
    <div><strong>Niche</strong> - Online Fitness Coaching</div>
    <div><strong>Advertisers studied</strong> - 100+</div>
    <div><strong>Active ads analyzed</strong> - 1000+</div>
  </div>
</div>

<h2>Winning Hooks This Week</h2>
<p>intro</p>
<ol>
  <li><em>"Hook copy"</em><p><strong>Label</strong> - explanation</p></li>
  ... 5 to 7 hooks
</ol>

<h2>Copy Angles That Are Working</h2>
<h3>1. Angle name</h3><p>...</p>
... 5 angles

<div class="callout"><strong>Emotional triggers in play this week:</strong> ...</div>

<h2>Format Performance Hierarchy (2026 Andromeda Era)</h2>
<table>
  <thead><tr><th>Format</th><th>Status</th><th>Best Use</th></tr></thead>
  <tbody><tr><td>...</td><td>...</td><td>...</td></tr> ... 6-8 rows</tbody>
</table>
<p><strong>Optimal duration:</strong> ...</p>
<p><strong>Mobile share:</strong> ...</p>

<h2>Andromeda Diversity Rules (Critical for 2026)</h2>
<div class="callout">...</div>
<p><strong>Pack System (what top advertisers run):</strong></p>
<ul>...</ul>

<h2>Fresh vs. Oversaturated</h2>
<div class="split-table">
  <div class="split-col fresh"><h4>Fresh - Test These</h4><ul>...</ul></div>
  <div class="split-col stale"><h4>Oversaturated - Retire</h4><ul>...</ul></div>
</div>
<div class="callout"><strong>Creative fatigue warning:</strong> ...</div>

<h2>3 Actionable Ad Ideas - Ready to Brief</h2>
<div class="idea-card">
  <h3>Idea #1 - Name (Format)</h3>
  <div class="field"><div class="field-label">Format</div><div class="field-value">...</div></div>
  <div class="field"><div class="field-label">Hook</div><div class="field-value"><em>"..."</em></div></div>
  <div class="field"><div class="field-label">Structure</div><div class="field-value">...</div></div>
  <div class="field"><div class="field-label">CTA</div><div class="field-value">"..."</div></div>
  <div class="field"><div class="field-label">Why brief</div><div class="field-value">...</div></div>
</div>
... 3 idea cards total

<div class="brief-cta">
  <h3>Want this applied to your account?</h3>
  <p>Free 20-min audit - I'll run this week's insights against your live ads and show you what to change.</p>
  <a href="https://api.leadconnectorhq.com/widget/bookings/discovery-call-aleksaadvision" target="_blank" rel="noopener">Book Free Audit Call</a>
</div>

<div class="brief-sources">
  <strong>Research sources:</strong> Meta Ad Library, plus public industry articles. Synthesized from active advertisers in the niche.<br><br>
  <strong>Next report:</strong> <span class="next-monday">every Monday</span>.
</div>
"""

    rules = """
HARD RULES:
- NEVER use em dashes (the U+2014 character). Use hyphens, commas, colons, or periods.
- Every claim must be grounded in the ad data provided or in well known 2026 Meta ads context. Do not invent specific advertiser names or fake numbers that you cannot back up from the data.
- Use real hook copy patterns observed across multiple ads. Generalize hooks rather than quoting verbatim.
- Tone: tactical, no fluff, written for a Meta Ads buyer.
- Output STRICT JSON only. No markdown, no code fences, no commentary.
"""

    user_msg = f"""You are generating issue #{issue_num} of the Weekly Meta Ads Intel newsletter for Aleksa, a Meta Ads Manager who serves online fitness coaches. Today is {issue_date}.

Below is real ad data pulled from the Meta Ad Library this morning ({len(ads)} active ads from {len(SEARCH_TERMS)} search variations). Synthesize the patterns and produce ONE JSON object matching the schema example.

ACTIVE FITNESS COACHING ADS (sample):
{json.dumps(ads, indent=2)[:60000]}

SCHEMA EXAMPLE (return JSON in this exact shape, do not include any extra fields):
{json.dumps(schema_example, indent=2)}

CONTENT_HTML RULES:
{html_rules}

{rules}

Return JSON only.
"""
    return user_msg


def call_claude(prompt):
    client = Anthropic(api_key=ANTHROPIC_KEY)
    print(f"[claude] calling {ANTHROPIC_MODEL}, prompt size {len(prompt)} chars", flush=True)
    resp = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in resp.content if hasattr(b, "text"))
    print(f"[claude] response {len(text)} chars, stop={resp.stop_reason}", flush=True)
    return text


def parse_issue_json(text):
    text = text.strip()
    if text.startswith("```"):
        first_nl = text.find("\n")
        text = text[first_nl + 1:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON object found in response: {text[:300]}")
    return json.loads(text[start:end + 1])


def sanitize(issue):
    """Strip em dashes if Claude slipped one through."""
    def fix(s):
        if isinstance(s, str):
            return s.replace("—", " - ").replace("–", "-")
        if isinstance(s, list):
            return [fix(x) for x in s]
        if isinstance(s, dict):
            return {k: fix(v) for k, v in s.items()}
        return s
    return fix(issue)


def main():
    today = datetime.now(timezone.utc).date()
    iso_date = today.isoformat()

    issues_doc = json.loads(ISSUES_PATH.read_text(encoding="utf-8"))
    existing_nums = [i.get("num", 0) for i in issues_doc.get("issues", [])]
    issue_num = (max(existing_nums) + 1) if existing_nums else 1
    print(f"[publish] new issue #{issue_num} dated {iso_date}", flush=True)

    if any(i.get("date") == iso_date for i in issues_doc["issues"]):
        print(f"[publish] issue for {iso_date} already exists, skipping", flush=True)
        return 0

    ads = fetch_ads()
    slim = slim_ads(ads)
    print(f"[publish] {len(slim)} unique ads after dedup", flush=True)
    if len(slim) < 5:
        print("[publish] too few ads pulled, aborting", flush=True)
        return 1

    prompt = build_prompt(slim, issue_num, iso_date)
    raw = call_claude(prompt)
    issue = parse_issue_json(raw)
    issue = sanitize(issue)

    required = {"num", "date", "slug", "title", "summary", "tags",
                "featuredTitle", "featuredDesc", "featuredMeta",
                "insight", "insightFooter", "contentHtml"}
    missing = required - set(issue.keys())
    if missing:
        raise ValueError(f"issue missing fields: {missing}")

    issue["num"] = issue_num
    issue["date"] = iso_date
    issue["slug"] = f"fitness-{iso_date}"

    issues_doc["issues"].insert(0, issue)
    issues_doc["lastUpdated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if "futurePlaceholders" in issues_doc and issues_doc["futurePlaceholders"] > 0:
        issues_doc["futurePlaceholders"] -= 1

    ISSUES_PATH.write_text(
        json.dumps(issues_doc, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"[publish] wrote {ISSUES_PATH}, total issues {len(issues_doc['issues'])}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
