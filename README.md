# HoofLab Shop — product-page SEO and conversion lab

A small catalog of six hoof-care SKUs. Each product detail page has a problem, a buyer, specs, FAQ, internal links, meta tags and Product JSON-LD.

This is a **shop-operator lab**, not a theme. There is no checkout. The point is: can a visitor understand the product, and can a search engine read the page.

Live pages: [https://mynulislam95.github.io/shop-pdp-seo-lab/](https://mynulislam95.github.io/shop-pdp-seo-lab/)

## What to open first

1. [Catalog](https://mynulislam95.github.io/shop-pdp-seo-lab/index.html)
2. One PDP, e.g. [Sensor Hoof Boot](https://mynulislam95.github.io/shop-pdp-seo-lab/sensor-hoof-boot.html)
3. [SEO notes](https://mynulislam95.github.io/shop-pdp-seo-lab/seo.html)

On a PDP you should see:

- Unique `<title>` and meta description
- Canonical + Open Graph
- H1 = product name
- Breadcrumb, specs table, FAQ
- Related products (internal links)
- `Product` JSON-LD with price
- One labelled demo CTA (no fake payment)

## Run locally

```bash
python3 generate_site.py
python3 check_seo.py
pytest -q
```

Open `docs/index.html` in a browser.

## Layout

```text
data/products.json   Source of truth for SKUs
generate_site.py     Writes static HTML
check_seo.py         Fails if a page is missing core SEO
docs/                GitHub Pages output
tests/test_seo.py
```

## Why it exists

E-commerce work is mostly product pages: structure, copy, technical SEO, and a page that still works on a phone. This repo is that loop in public.

Mynul Islam
