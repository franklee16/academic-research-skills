# HTML Report Template

Create a zero-build static `index.html` inside the Field Map Workspace. It must be readable by opening the file directly in a browser.

## Required Sections

1. Field Boundary
2. Seed Set Overview
3. Search Strategy
4. Research Clusters
5. Paper Table
6. Research Opportunities
7. Reading Order / Next Actions

## Report Rules

- Link to markdown files using relative links.
- Do not require React, Vite, npm, a server, or external JavaScript.
- Inline CSS is acceptable.
- Add an inline, no-dependency Markdown preview overlay that intercepts local `.md` links, fetches the Markdown file, renders it in a full-screen readable card, and closes via a visible close button, backdrop click, or Escape.
- Keep each Markdown link's original relative `href` so the report degrades to normal navigation if JavaScript or local file reads are unavailable.
- The Markdown preview renderer must handle headings, paragraphs, unordered and ordered lists, blockquotes, fenced code, inline code, links, and simple pipe tables.
- Keep the report readable and printable.
- Use tables for paper lists and opportunity summaries.
- Use anchor links for navigation.
- Do not copy every paper note into the HTML; summarize and link out.

## Minimal Skeleton

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{Field Name} Field Map</title>
  <style>
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.55;
      color: #1f2933;
      background: #f7f8fa;
    }
    main {
      max-width: 1120px;
      margin: 0 auto;
      padding: 40px 20px;
    }
    section {
      margin: 32px 0;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      background: #ffffff;
    }
    th,
    td {
      border: 1px solid #d8dee8;
      padding: 10px 12px;
      text-align: left;
      vertical-align: top;
    }
    th {
      background: #eef2f7;
    }
    a {
      color: #2457a6;
    }
  </style>
</head>
<body>
  <main>
    <h1>{Field Name} Field Map</h1>
    <nav>
      <a href="#boundary">Boundary</a>
      <a href="#seed-set">Seed Set</a>
      <a href="#strategy">Search Strategy</a>
      <a href="#clusters">Clusters</a>
      <a href="#papers">Papers</a>
      <a href="#opportunities">Opportunities</a>
      <a href="#next-actions">Next Actions</a>
    </nav>

    <section id="boundary">
      <h2>Field Boundary</h2>
      <p><a href="field_boundary.md">Open field_boundary.md</a></p>
    </section>

    <section id="seed-set">
      <h2>Seed Set Overview</h2>
    </section>

    <section id="strategy">
      <h2>Search Strategy</h2>
      <p><a href="search_strategy.md">Open search_strategy.md</a></p>
    </section>

    <section id="clusters">
      <h2>Research Clusters</h2>
      <p><a href="research_clusters.md">Open research_clusters.md</a></p>
    </section>

    <section id="papers">
      <h2>Paper Table</h2>
    </section>

    <section id="opportunities">
      <h2>Research Opportunities</h2>
      <p><a href="research_opportunities.md">Open research_opportunities.md</a></p>
    </section>

    <section id="next-actions">
      <h2>Reading Order / Next Actions</h2>
    </section>
  </main>
</body>
</html>
```
