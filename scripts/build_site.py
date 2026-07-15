#!/usr/bin/env python3
"""
build_site.py
--------------
Kayakhod jami3 les fichiers .md f posts/ o kaybnihom f site static (HTML)
f dossier docs/ (bach GitHub Pages ykhdem 3lih direct).

Kaykhdem b Jinja2 templates li kaynin f templates/.
"""

import shutil
from pathlib import Path

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader
from slugify import slugify

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "posts"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
OUTPUT_DIR = ROOT / "docs"  # GitHub Pages kayqra men /docs f branche main

SITE_NAME = "Mon Blog"
SITE_DESCRIPTION = "Articles générés et mis à jour automatiquement."


def load_posts():
    posts = []
    if not POSTS_DIR.exists():
        return posts
    for md_file in sorted(POSTS_DIR.glob("*.md"), reverse=True):
        post = frontmatter.load(md_file)
        html_content = markdown.markdown(post.content, extensions=["extra", "toc"])
        slug = md_file.stem
        posts.append(
            {
                "title": post.get("title", "Sans titre"),
                "date": str(post.get("date", "")),
                "category": post.get("category", "general"),
                "description": post.get("description", ""),
                "content": html_content,
                "slug": slug,
                "url": f"posts/{slug}.html",
            }
        )
    return posts


def build():
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "posts").mkdir(exist_ok=True)

    # copy static assets (css)
    dest_static = OUTPUT_DIR / "static"
    if dest_static.exists():
        shutil.rmtree(dest_static)
    shutil.copytree(STATIC_DIR, dest_static)

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    posts = load_posts()

    # --- index page ---
    index_tpl = env.get_template("index.html")
    (OUTPUT_DIR / "index.html").write_text(
        index_tpl.render(
            site_name=SITE_NAME,
            site_description=SITE_DESCRIPTION,
            posts=posts,
        ),
        encoding="utf-8",
    )

    # --- individual post pages ---
    post_tpl = env.get_template("post.html")
    for post in posts:
        out_path = OUTPUT_DIR / "posts" / f"{post['slug']}.html"
        out_path.write_text(
            post_tpl.render(site_name=SITE_NAME, post=post),
            encoding="utf-8",
        )

    print(f"[OK] Site mbni f: {OUTPUT_DIR} ({len(posts)} articles)")


if __name__ == "__main__":
    build()
