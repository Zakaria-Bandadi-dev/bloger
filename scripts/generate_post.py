#!/usr/bin/env python3
"""
generate_post.py
-----------------
Kaydir call l'API free dyal Groq (https://console.groq.com) bach ykhalq
article jdid kul mera li khddamha (cron/GitHub Actions).

Bach ykon "hasri" (unique) f kul run:
  - Kaykhtar topic li mazal ma tsajlch (used_topics.json)
  - Kaykhtar "angle" random (guide, listicle, opinion, case-study...)
  - Kaydir prompt mzyan li kayqol l'model ykteb b style dyalo, mafisha copy-paste

Environment variable methlouba:
  GROQ_API_KEY  -> free API key men https://console.groq.com/keys
"""

import os
import re
import json
import random
import datetime
from pathlib import Path

import requests
from slugify import slugify

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "posts"
TOPICS_FILE = ROOT / "topics.txt"
USED_TOPICS_FILE = ROOT / "used_topics.json"

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
# Model free o serie3 bezaf 3la Groq. Momkin tbedlha b "llama-3.3-70b-versatile"
GROQ_MODEL = "llama-3.1-8b-instant"

ANGLES = [
    "un guide pratique étape par étape",
    "une liste (listicle) avec des points concrets",
    "un article d'opinion argumenté",
    "une comparaison avant/après avec des exemples réels",
    "un article basé sur des erreurs courantes à éviter",
    "un format questions/réponses (FAQ)",
]


def load_topics():
    topics = []
    with open(TOPICS_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            title, category = [p.strip() for p in line.split("|")]
            topics.append({"title": title, "category": category})
    return topics


def load_used():
    if USED_TOPICS_FILE.exists():
        return json.loads(USED_TOPICS_FILE.read_text(encoding="utf-8"))
    return []


def save_used(used):
    USED_TOPICS_FILE.write_text(json.dumps(used, ensure_ascii=False, indent=2), encoding="utf-8")


def pick_topic():
    topics = load_topics()
    used = load_used()
    remaining = [t for t in topics if t["title"] not in used]
    if not remaining:
        # dorna 3la kolchi -> nbdaw mn jdid (reset dyal cycle)
        remaining = topics
        used = []
    topic = random.choice(remaining)
    used.append(topic["title"])
    save_used(used)
    return topic


def call_groq(topic_title, category, angle):
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY machi mawjouda. Dir export GROQ_API_KEY=xxx "
            "wla zidha f GitHub Secrets."
        )

    system_prompt = (
        "Tu es un rédacteur web professionnel francophone. Tu écris des articles de blog "
        "originaux, naturels, bien structurés en Markdown, jamais génériques ou robotiques. "
        "Varie toujours le ton, les exemples et la structure d'un article à l'autre."
    )

    user_prompt = f"""Écris un article de blog complet en français sur le sujet suivant :
"{topic_title}"

Contraintes :
- Format de rédaction demandé : {angle}
- Longueur : 500 à 800 mots
- Structure en Markdown avec un titre H1 (#), des sous-titres H2 (##)
- Ton naturel, humain, pas de répétitions creuses
- Termine par une courte conclusion actionnable
- Ne mets AUCUN texte avant le titre H1 ni après la conclusion (pas de "Voici l'article:")

Ensuite, sur une DERNIÈRE ligne séparée, donne une méta-description SEO de 150-160
caractères maximum, précédée EXACTEMENT de "META: " (sans guillemets).
"""

    resp = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.9,
            "max_tokens": 1800,
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def parse_response(raw_text):
    meta_match = re.search(r"META:\s*(.+)$", raw_text.strip(), re.MULTILINE)
    description = meta_match.group(1).strip() if meta_match else ""
    body = raw_text
    if meta_match:
        body = raw_text[: meta_match.start()].strip()

    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "Article sans titre"

    return title, description, body


def save_post(title, description, category, body):
    POSTS_DIR.mkdir(exist_ok=True)
    today = datetime.date.today().isoformat()
    slug = slugify(title)[:60]
    filename = f"{today}-{slug}.md"
    filepath = POSTS_DIR / filename

    frontmatter = (
        "---\n"
        f'title: "{title}"\n'
        f"date: {today}\n"
        f"category: {category}\n"
        f'description: "{description}"\n'
        "---\n\n"
    )

    filepath.write_text(frontmatter + body, encoding="utf-8")
    print(f"[OK] Article jdid tsajel: {filepath}")
    return filepath


def main():
    topic = pick_topic()
    angle = random.choice(ANGLES)
    print(f"[..] Topic: {topic['title']} | Angle: {angle}")

    raw = call_groq(topic["title"], topic["category"], angle)
    title, description, body = parse_response(raw)
    save_post(title, description, topic["category"], body)


if __name__ == "__main__":
    main()
