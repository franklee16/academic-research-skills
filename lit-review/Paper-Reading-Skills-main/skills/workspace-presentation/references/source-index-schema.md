# Source Index Schema

`public/source-index.json` lists the source files exposed by a Workspace Presentation. It does not copy source markdown; it records how the React app can link to and preview the original files.

## Shape

```json
{
  "schemaVersion": 1,
  "sourceRoot": "/absolute/path/to/workspace/experiment-designs/field/method",
  "files": [
    {
      "id": "claim_evidence_map",
      "label": "claim_evidence_map.md",
      "path": "/absolute/path/to/claim_evidence_map.md",
      "relativePath": "claim_evidence_map.md",
      "readUrl": "/@fs//absolute/path/to/claim_evidence_map.md",
      "openHref": "/absolute/path/to/claim_evidence_map.md",
      "workflow": "experiment-design",
      "displayCategory": "summarize-then-link",
      "exists": true
    }
  ]
}
```

## Required Fields

- `schemaVersion`: currently `1`.
- `sourceRoot`: absolute path to the selected source workspace or chain root.
- `files`: source files that may be shown, summarized, linked, or previewed.

Each file needs:

- `id`: stable id used by manifest modules and summaries.
- `label`: short display label.
- `path`: absolute source path.
- `relativePath`: path relative to the source root when possible.
- `readUrl`: Vite-readable URL, usually `/@fs/{absolute-source-path}`.
- `workflow`: detected workflow type.
- `displayCategory`: `primary-display`, `summarize-then-link`, or `link-only`.
- `exists`: whether the file was present during generation.

## Vite File Serving

The template's `vite.config.ts` allows serving files from the repository root when the presentation lives at `workspace/presentations/{slug}/`. If the source workspace is outside that root, update `server.fs.allow` in the generated presentation or generate `readUrl` values that the local server can serve.
