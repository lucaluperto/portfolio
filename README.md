# Luca Luperto · Portfolio

Case studies in growth and digital marketing, published at **[lucaluperto.it](https://lucaluperto.it)**.

| Case study | What it shows |
|---|---|
| [Comedy Week](https://lucaluperto.it/comedy-week.html) | 32.8M organic Instagram views from a creator programme, and what per-video tracking revealed |
| [Azzurro Club](https://lucaluperto.it/azzurro-ads.html) | Moving a 13-hotel group from OTAs to direct bookings (20% → 70% of revenue) |
| [Italy Food PRN](https://lucaluperto.it/italy-food-prn.html) | Zero to 80,000 followers by rebuilding content production |
| [Kolms Creative](https://lucaluperto.it/kolms-creative.html) | A content service for luxury hotels, built and sold to 30+ clients |

## How it's built

Plain static HTML, CSS and JavaScript hosted on GitHub Pages. The production pages, styles, scripts, images and CSV datasets currently live in the repository root.

The HTML files are the current source of truth. `build.py` is a legacy generator from an earlier directory structure and must not be run against the production branch until it has been refactored; it still expects `data/` and `assets/` directories that no longer exist.

The Comedy Week dataset (`comedy-week.csv`) has one row per collaboration: edition, creator, views per channel and link to the video.

Contact: lucaluperto99@gmail.com · [LinkedIn](https://www.linkedin.com/in/lupertoluca)
