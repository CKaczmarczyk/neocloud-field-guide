# Neocloud Field Guide

Source for https://ckneocloudguide.vercel.app (Kinetic Yard / Third Prime).

- `src/compute-yard.html` — the guide page (same file as the Claude artifact).
- `export/` — snapshot of the guide's database (briefings, companies, reports, metrics, themes, scenarios) and report PDFs under `export/assets/`.
- `build_site.py` — assembles `site/` (run by Vercel on each push).

A scheduled Claude task re-exports `export/` from the live guide and pushes weekly; pushes deploy automatically through Vercel.
