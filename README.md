# The Urban Edit

*Ideas, Spaces & Stories for Modern Living.*

The source for **[theurbanedit.github.io](https://theurbanedit.github.io/)**, an independent multi-category digital magazine built with **Jekyll** and hosted free on **GitHub Pages**. There's no database, no framework and no build tooling to install: you write articles in Markdown, push, and GitHub builds the site.

---

## How the project is organised

```
_config.yml            Site settings (title, URL, newsletter, contact email, per-page count)
_data/
  categories.yml       All sections: name, short label, intro, colour, subcategories
  navigation.yml       Header menu, "More" dropdown and footer links
  homepage.yml         Homepage curation: hero, secondary, trending, category rows
  social.yml           Social profile links (hidden until filled in)
_posts/                Articles (one Markdown file each)
_topics/               One tiny file per category -> creates /fashion/, /business/ ...
_layouts/              Page templates (home, post, category, page, default)
_includes/             Reusable components (header, footer, cards, SEO, newsletter ...)
_templates/            article-template.md, copy this for new articles (not published)
assets/css/main.css    All styles (colours/fonts are variables at the top)
assets/js/main.js      Menu, search, table of contents, pagination, share buttons
assets/images/posts/   Article images
assets/images/brand/   Logo, favicon, default social image
articles/              /articles/, the full archive
about.md, contact.md, privacy-policy.md, terms.md, editorial-policy.md
search.html + search.json   Client-side search (no external service)
robots.txt, 404.html   (sitemap.xml and feed.xml are generated automatically)
tools/make_covers.py   Script that generated the launch illustrations (optional)
```

---

## 1. Add a new article

1. Copy `_templates/article-template.md` into `_posts/`.
2. Rename it `YYYY-MM-DD-your-article-slug.md`, e.g. `2026-12-02-best-coworking-cafes-in-lisbon.md`.
   The URL becomes `https://theurbanedit.github.io/best-coworking-cafes-in-lisbon/`.
3. Fill in the front matter (the part between the `---` lines):

   | Field | Required | Notes |
   |---|---|---|
   | `title` | yes | Headline |
   | `description` | yes | 140–160 chars; subtitle + meta description |
   | `date` | yes | Publication date. **Future dates are hidden until that date.** |
   | `updated` | no | Shows "Updated …" and sets `dateModified` in structured data |
   | `categories` | yes | Slugs from `_data/categories.yml`. The **first** one is the primary section |
   | `tags` | no | Lower-case, hyphenated |
   | `author` | no | Defaults to "The Urban Edit Editorial Team" |
   | `image` / `thumbnail` | recommended | 1600×1000 and 800×500 |
   | `image_alt` | yes if image | Describe the image |
   | `image_credit` | recommended | Photographer / source / licence |
   | `featured`, `trending` | no | `true` makes it eligible for homepage slots |
   | `sources` | recommended | List of `title`, `publisher`, `url`, rendered as "Sources & further reading" |
   | `seo_title`, `canonical_url`, `noindex` | no | SEO overrides |
   | `sample` | no | Adds the "launch edition" AI-assisted note. Remove it once you've reviewed or rewritten a launch article |

4. Write the body in Markdown. Use `##` and `###` headings. `##` headings automatically build the table of contents.
5. Commit and push (see section 6). The article appears on the homepage, its category pages, the archive, search, the RSS feed and the sitemap automatically. Related articles are chosen automatically too.

**Internal links:** `[anchor text]({{ '/article-slug/' | relative_url }})`. Using `relative_url` keeps links working if the site address changes.

## 2. Upload images

1. Use images you own, created, or have a licence for (e.g. Unsplash/Pexels licence, purchased stock, your own photos). Record the credit in `image_credit`.
2. Export two sizes: **1600×1000** (`image`) and **800×500** (`thumbnail`), JPG or WebP, ideally under ~300 KB and ~120 KB.
3. Put them in `assets/images/posts/`, named after the article slug: `my-slug.jpg` and `my-slug-800.jpg`.
4. **On GitHub.com:** open the repo → `assets/images/posts` → **Add file → Upload files** → drag them in → **Commit changes**.

Every image is lazy-loaded (except the article hero), has fixed dimensions to prevent layout shift, and uses `srcset` so phones download the small version.

## 3. Add a category (or subcategory)

1. Add an entry to `_data/categories.yml` (copy an existing block; choose a unique `slug`).
2. Create `_topics/<slug>.md` containing only:
   ```yaml
   ---
   category: <slug>
   ---
   ```
   This creates the archive page at `/<slug>/`.
3. Optional: add it to the header in `_data/navigation.yml` (`main` or `more`), or to the homepage rows in `_data/homepage.yml` (`sections`).

It then appears in the mobile menu, footer and "Explore every section" list automatically.
**Subcategories:** list them under `subcategories:` in the category entry and use those slugs as `tags` on articles. Tag links lead to search results for that tag.

## 4. Edit homepage features

Open `_data/homepage.yml`:

- `hero`: slug of the cover story.
- `secondary`: up to three slugs shown beside the hero.
- `trending`: four slugs for the Trending strip.
- `latest_count`: number of articles in "Latest".
- `sections`: which category rows appear, in order.

Leave any of them empty and the site falls back to automatic choices (newest `featured: true` articles, newest `trending: true`, and so on).

## 5. Update navigation

`_data/navigation.yml`:

```yaml
main:                      # header bar
  - title: "Home"
    url: /
  - category: fashion      # label + URL come from categories.yml
more:                      # "More" dropdown
  - category: travel
  - title: "All articles"
    url: /articles/
footer:                    # footer "The magazine" column
  - title: "About"
    url: /about/
```

Social icons: add profile URLs in `_data/social.yml`. Empty entries stay hidden.

## 6. Publish changes

**Option A: in the browser (no software needed)**
Open the file on GitHub → pencil icon (Edit) → make changes → **Commit changes**. For new files use **Add file → Create new file** (type `_posts/2026-12-02-my-slug.md` as the name).

**Option B: on your computer with Git**
```bash
git pull
# add or edit files
git add .
git commit -m "Add article: My headline"
git push
```

GitHub Pages rebuilds automatically, usually within 1–3 minutes. Check progress under the repo's **Actions** tab ("pages build and deployment"). If a build fails, the log shows the file and line with the problem, which is usually a YAML typo in front matter (unbalanced quotes, or a tab instead of spaces).

**Preview locally (optional):** install Ruby, then `bundle install` and `bundle exec jekyll serve`, then open http://localhost:4000.

## 7. Connect the newsletter

The sign-up form is honest by default: it tells readers sign-ups open soon and **stores nothing**. To go live:

1. Create an account with a provider (Buttondown, Mailchimp, Kit/ConvertKit, Beehiiv, MailerLite…).
2. Find its **embedded/HTML form** code and copy the form's `action="…"` URL and the email input's `name` (often `email` or `EMAIL`).
3. In `_config.yml`:
   ```yaml
   newsletter:
     action: "https://buttondown.com/api/emails/embed-subscribe/YOURNAME"
     email_field: "email"
   ```
4. Update `privacy-policy.md` to name the provider. Push.

## 8. Connect a custom domain later

1. Buy a domain from any registrar.
2. In the repo: **Settings → Pages → Custom domain** → enter e.g. `www.theurbanedit.com` → Save. (GitHub adds a `CNAME` file.)
3. At your registrar's DNS settings:
   - `www` → **CNAME** → `theurbanedit.github.io`
   - apex `theurbanedit.com` → **A** records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (optional AAAA: `2606:50c0:8000::153`, `…8001::153`, `…8002::153`, `…8003::153`)
4. Wait for DNS (minutes to hours), then tick **Enforce HTTPS**.
5. Change `url:` in `_config.yml` to `https://www.theurbanedit.com` so canonicals, sitemap and feed use the new domain.
6. Verify the domain in Google Search Console and submit `/sitemap.xml`.

## 9. Other settings in `_config.yml`

- `contact_email`: shows an email address on the Contact page.
- `twitter_username`: adds `twitter:site` to cards.
- `per_page`: articles per page on category/archive pages.
- If the repository is ever **not** named `<account>.github.io`, set `baseurl: "/repo-name"`.

## SEO features included

Unique titles and meta descriptions, canonical URLs, Open Graph + Twitter/X cards, JSON-LD (NewsMediaOrganization + WebSite with SearchAction on the homepage; BlogPosting + BreadcrumbList on articles; CollectionPage + BreadcrumbList on sections), visible breadcrumbs, `sitemap.xml` (jekyll-sitemap), `feed.xml` RSS/Atom (jekyll-feed), `robots.txt`, clean URLs, internal linking and related articles, semantic HTML5, descriptive alt text, a noindexed search page and a custom 404.

## Content notes

The 12 launch articles are marked `sample: true`, which adds a short "launch edition" note saying they were prepared with AI-assisted drafting. Review or rewrite each one, then remove `sample: true`. The launch illustrations are original abstract artwork generated by `tools/make_covers.py`; replace them with licensed photography whenever you like.
