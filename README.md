# 🚀 Blog Automatique (Free) — Content AI + Auto-publish + Ads

Blog static li kayb9a itzid articles f 3ando b des intervalles automatiques,
b7al des vrais news, en utilisant une **API free** (Groq), o kaykhdem **b la
mochkil f flous** (0 dh/mois si mab9itch tzid un domaine payant).

---

## 📦 Chnou kayn f had projet

```
blog-project/
├── scripts/
│   ├── generate_post.py   # kaydir call Groq API o kaykhalq article jdid
│   └── build_site.py      # kaybni le site HTML final f docs/
├── templates/              # HTML templates (Jinja2) + ad slots
├── static/style.css        # design dyal site
├── posts/                  # articles f Markdown (source)
├── docs/                   # 🔥 hada li GitHub Pages kaydir serve (auto-généré)
├── topics.txt               # liste dyal sujets li kaytkhtaro random
├── .github/workflows/
│   └── auto-publish.yml    # cron job li kaydir kolchi automatiquement
├── requirements.txt
└── README.md (had fichier)
```

---

## 🛠️ Étape 1 — Créer un repo GitHub

1. Créer un compte GitHub gratuit (si mazal 3andekch): https://github.com
2. Créer un new repository (public, bach GitHub Pages ykhdem free)
3. Uploader tous les fichiers dyal had projet f had repo (drag & drop wla git push)

---

## 🔑 Étape 2 — Prendre une clé API Groq (100% gratuite)

1. Aller sur https://console.groq.com
2. Sajel (free, b Google account wla email)
3. Aller à "API Keys" → Create API Key → copier la clé (bda b `gsk_...`)

> Groq kayt3ti free tier généreuse bezaf (des milliers de requêtes/jour),
> o kayjib des modèles Llama vites bezaf. Momkin tbedel b Gemini API b nafss
> le principe si bghiti (khass ghi tbedel `scripts/generate_post.py`).

---

## 🔒 Étape 3 — Ajouter la clé comme Secret GitHub

1. F repo dyalek → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret**
3. Name: `GROQ_API_KEY`
4. Value: colle la clé li khdit men Groq
5. Save

---

## 🌐 Étape 4 — Activer GitHub Pages

1. F repo → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / folder: **`/docs`**
4. Save

Ba3d chi minutes, site dyalek ghadi ykon live f:
`https://<username>.github.io/<repo-name>/`

---

## ▶️ Étape 5 — Test manuel (avant ma texpecti l'automation)

Localement (wla f Codespaces):

```bash
pip install -r requirements.txt
export GROQ_API_KEY="gsk_xxxxxxxxxxxx"
python scripts/generate_post.py     # kaykhalq wa7ed article jdid f posts/
python scripts/build_site.py        # kaybni le site f docs/
```

Puis push:
```bash
git add posts/ docs/ used_topics.json
git commit -m "premier article"
git push
```

Ou, plus simple: aller f GitHub → tab **Actions** → workflow "Auto-publish blog
post" → **Run workflow** (bouton manuel), bach tjarreb bla ma tmchi l terminal.

---

## ⏰ Étape 6 — L'automation (b GitHub Actions, déjà configurée)

Le fichier `.github/workflows/auto-publish.yml` kaydir:
1. Kaykhtar topic jdid (bla tkrar, thanks à `used_topics.json`)
2. Kaydir call Groq API bach ykhalq l'article
3. Kaybni le site static
4. Kaydir commit + push automatiquement

Par défaut, kaykhdem **kul nhar f 8h UTC**. Bach tbedel l'fréquence (kul 6h,
kul semana, etc.), bedel `cron: "0 8 * * *"` f `.github/workflows/auto-publish.yml`.
Des exemples: https://crontab.guru

⚠️ GitHub Actions scheduled workflows khass repo ykon **actif** (chi commit/
activité daymen daymen) — GitHub kayd disable les workflows automatiques ba3d
~60 jours bla activité. Solution: dir chi commit manuel mera fi chhar, wla
khalih ykhdem b workflow_dispatch.

---

## 💰 Étape 7 — Ajouter les publicités (Google AdSense — gratuit)

Les templates (`templates/base.html`, `index.html`, `post.html`) déjà fihom
**5 emplacements pubs jahzin**:

| Emplacement | Fichier | Description |
|---|---|---|
| Banner top | `base.html` | fouq site kamel |
| Sidebar | `base.html` | jnib content |
| In-feed | `index.html` | kul 3 articles f la page d'accueil |
| In-article | `post.html` | f nnos dyal chaque article |
| Footer | `base.html` | taht kolchi |

**Bach tfe3lhom:**

1. Sajel f https://www.google.com/adsense (free, khass site ykon accessible/live)
2. Google ghadi i3tik un ID b7al `ca-pub-1234567890123456`
3. F `templates/base.html`, neḥi l'commentaire `<!-- -->` men script principal
   f `<head>` o 3wed `ca-pub-XXXXXXXXXXXXXXXX` b l'ID dyalek
4. Dir nafss chi f kul `<!-- ... -->` dyal ad-slot li bghiti tfe3el (banner,
   sidebar, in-feed, in-article, footer) — 3wed `data-ad-client` o
   `data-ad-slot` b les valeurs li Google ghadi i3tik mnin tkhalq chaque unité
5. Push, o Google ghadi ydir review (kaywali chi youmayn) qbel ma tbdaw tban
   des vraies pubs

> Had emplacements déjà stylés bien (CSS f `static/style.css`) — mab9ach
> khasek tbedel design, ghir dir paste dyal code AdSense.

---

## 🎨 Personnalisation

- **Design**: bedel `static/style.css` (couleurs, fonts, etc.)
- **Nom du site**: bedel `SITE_NAME` f `scripts/build_site.py`
- **Topics**: zid/n9es lignes f `topics.txt`
- **Style d'écriture**: bedel `system_prompt` / `user_prompt` f
  `scripts/generate_post.py` (ton, langue, longueur...)
- **Modèle AI**: momkin tbedel `GROQ_MODEL` b modèle akhor (llama-3.3-70b-versatile
  ghadi ta3ti quality a7sen walakin ashwiya abta2)

---

## ❓ Troubleshooting

- **Workflow ma khddemch**: check tab "Actions" f GitHub, chouf l'log dyal l'erreur
- **"GROQ_API_KEY machi mawjouda"**: verifier Secret f Settings → Secrets → Actions
- **Site mab9ach live**: verifier Pages settings (branch=main, folder=/docs)
- **Pubs mab9ach ban**: AdSense kayakhod chi youmayn bach ydir review, o khass
  site ykon 3ando contenu kafi (chi 10-15 articles) bach yqbel domain dyalek
