"""Build static product pages with SEO tags, JSON-LD and a conversion layout."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data" / "products.json").read_text(encoding="utf-8"))
OUT = ROOT / "docs"
BASE = "https://mynulislam95.github.io/shop-pdp-seo-lab"
SHOP = "HoofLab Shop"


def esc(text: object) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def page_shell(title: str, description: str, canonical: str, body: str, json_ld: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{esc(canonical)}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{esc(canonical)}">
  <link rel="stylesheet" href="styles.css">
  {json_ld}
</head>
<body>
  <header class="top">
    <a class="logo" href="index.html">{esc(SHOP)}</a>
    <nav>
      <a href="index.html">Catalog</a>
      <a href="seo.html">SEO notes</a>
    </nav>
  </header>
  {body}
  <footer>
    <p>Portfolio catalog for product-page SEO, UX and conversion. Not a live checkout.</p>
  </footer>
</body>
</html>
"""


def product_json_ld(p: dict) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": p["name"],
        "description": p["short"],
        "sku": p["slug"],
        "brand": {"@type": "Brand", "name": SHOP},
        "offers": {
            "@type": "Offer",
            "priceCurrency": "EUR",
            "price": p["price_eur"],
            "availability": "https://schema.org/InStock",
        },
    }
    blob = json.dumps(payload, ensure_ascii=False)
    return f'<script type="application/ld+json">{blob}</script>'


def render_pdp(p: dict) -> str:
    specs = "".join(
        f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in p["specs"].items()
    )
    benefits = "".join(f"<li>{esc(b)}</li>" for b in p["benefits"])
    faq = "".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>"
        for q, a in p["faq"]
    )
    related = [x for x in DATA if x["slug"] != p["slug"] and x["category"] == p["category"]][:2]
    if len(related) < 2:
        related = [x for x in DATA if x["slug"] != p["slug"]][:2]
    rel = "".join(
        f'<a class="card small" href="{esc(x["slug"])}.html"><strong>{esc(x["name"])}</strong><span>€{x["price_eur"]}</span></a>'
        for x in related
    )
    title = f"{p['name']} | {SHOP}"
    description = p["short"][:155]
    canonical = f"{BASE}/{p['slug']}.html"
    body = f"""
  <main class="pdp">
    <p class="crumbs"><a href="index.html">Catalog</a> / {esc(p['category'])} / {esc(p['name'])}</p>
    <div class="hero">
      <div class="visual" aria-hidden="true">{esc(p['category'])}</div>
      <div>
        <h1>{esc(p['name'])}</h1>
        <p class="lead">{esc(p['short'])}</p>
        <p class="price">€{p['price_eur']}</p>
        <p class="problem"><strong>Problem it solves.</strong> {esc(p['problem'])}</p>
        <p class="who"><strong>Who it is for.</strong> {esc(p['audience'])}</p>
        <a class="cta" href="#faq">See fit questions</a>
        <p class="micro">Demo catalog, no payment. CTA shows conversion placement.</p>
      </div>
    </div>
    <h2>Why this page is built this way</h2>
    <ul class="benefits">{benefits}</ul>
    <h2>Specs</h2>
    <table class="specs">{specs}</table>
    <h2 id="faq">Questions before a yard would buy</h2>
    {faq}
    <h2>Keep browsing</h2>
    <div class="grid">{rel}</div>
  </main>
"""
    return page_shell(title, description, canonical, body, product_json_ld(p))


def render_index() -> str:
    cards = "".join(
        f"""<a class="card" href="{esc(p['slug'])}.html">
          <span class="kicker">{esc(p['category'])}</span>
          <strong>{esc(p['name'])}</strong>
          <p>{esc(p['short'])}</p>
          <span class="price">€{p['price_eur']}</span>
        </a>"""
        for p in DATA
    )
    body = f"""
  <main>
    <h1>Hoof care products with clear product pages</h1>
    <p class="lead">Six SKUs. Each page has a problem, a buyer, specs, FAQ, internal links, meta tags and Product JSON-LD. Built as a shop-operator lab, not a theme demo.</p>
    <div class="grid">{cards}</div>
  </main>
"""
    return page_shell(
        f"{SHOP} | Product catalog",
        "Demo hoof-care catalog used to practise PDP SEO, UX and conversion structure.",
        f"{BASE}/index.html",
        body,
    )


def render_seo() -> str:
    body = """
  <main class="prose">
    <h1>What this catalog is for</h1>
    <p>A shop owner does not start with a new brand colour. They start with the product page: can a rider find it, understand it, and trust the next click.</p>
    <h2>On-page SEO on every PDP</h2>
    <ul>
      <li>Unique title and meta description under typical SERP length</li>
      <li>Canonical URL, Open Graph, H1 = product name</li>
      <li>Breadcrumb, FAQ, specs table, internal links to related SKUs</li>
      <li>Product JSON-LD with price and availability</li>
    </ul>
    <h2>Conversion structure</h2>
    <ul>
      <li>Problem and audience above the fold</li>
      <li>One primary CTA, then proof (specs + FAQ)</li>
      <li>No fake checkout. The CTA is labelled as a demo on purpose</li>
    </ul>
    <h2>How to run</h2>
    <pre>python3 generate_site.py
python3 check_seo.py
pytest -q</pre>
  </main>
"""
    return page_shell(
        f"SEO and conversion notes | {SHOP}",
        "How the HoofLab catalog implements technical SEO and product-page conversion.",
        f"{BASE}/seo.html",
        body,
    )


def main() -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(render_index(), encoding="utf-8")
    (OUT / "seo.html").write_text(render_seo(), encoding="utf-8")
    for p in DATA:
        (OUT / f"{p['slug']}.html").write_text(render_pdp(p), encoding="utf-8")
    css_src = ROOT / "styles.css"
    (OUT / "styles.css").write_text(css_src.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Wrote {2 + len(DATA)} HTML files to {OUT}")


if __name__ == "__main__":
    main()
