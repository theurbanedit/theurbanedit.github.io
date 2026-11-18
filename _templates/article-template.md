---
# ------------------------------------------------------------------
# ARTICLE TEMPLATE — copy this file into _posts/ and rename it:
#   _posts/YYYY-MM-DD-your-article-slug.md
# The slug (after the date) becomes the URL: /your-article-slug/
# Dates in the future are NOT published until that date has passed
# and the site is rebuilt.
# ------------------------------------------------------------------
title: "Your Headline Goes Here"
# 140–160 characters. Used as the subtitle, meta description and social text.
description: "One or two sentences that tell readers exactly what they will get from this article."
date: 2026-11-18 09:00:00 +0500
# updated: 2026-12-01            # optional: set when you substantially revise the article
# First category = primary section (breadcrumb, label, URL of section).
# Use slugs from _data/categories.yml
categories: [coworking, business]
tags: [remote-work, office-design, productivity]
author: "The Urban Edit Editorial Team"
# Images: 1600x1000 for `image`, 800x500 for `thumbnail` (JPG or WebP, < 300 KB)
image: /assets/images/posts/your-article-slug.jpg
thumbnail: /assets/images/posts/your-article-slug-800.jpg
image_alt: "Describe what the image shows for people who cannot see it"
image_credit: "Photo: Photographer Name / Source (licence)"
# featured: true                 # eligible for homepage hero/secondary slots
# trending: true                 # eligible for the Trending strip
# seo_title: "Shorter title for search results"   # optional override
# canonical_url: "https://original-source.com/..." # only if republished from elsewhere
sources:
  - title: "Name of the report, study or page"
    publisher: "Organisation (year)"
    url: "https://example.org/source"
---

Your opening paragraph. Make it count: this becomes the excerpt if no description is set, and it gets the decorative drop cap.

<!--more-->

## First section heading

Use `##` for main sections (they appear in the automatic table of contents) and `###` for sub-sections.

Link to other articles with relative URLs, e.g. [how coworking spaces are changing modern work]({{ '/how-coworking-spaces-are-changing-modern-work/' | relative_url }}).

Link to external sources normally: [Google Search Central](https://developers.google.com/search). External links open in a new tab automatically.

![Describe the image here (alt text)]({{ '/assets/images/posts/your-inline-image.jpg' | relative_url }}){: loading="lazy" width="1600" height="1000"}
*Caption in italics directly under the image.*

> A pull quote or key idea worth highlighting.

## Second section heading

- Bullet lists work
- Like this

1. Numbered lists too
2. Like this

<div class="callout" markdown="1">
### Key takeaway
Use a callout box for summaries, tips or checklists.
</div>
