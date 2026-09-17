# Motivation Supplement: {{DECK_TITLE}}

**Source deck:** `{{DECK_PATH}}`  
**Generated:** {{DATE}}  
**Messages covered:** {{MESSAGE_COUNT}}

---

## Message A: {{MESSAGE_TEXT}}

### News Evidence

| # | Headline | Source | Date | Rel. | Cred. | Suggested Bullet |
|---|----------|--------|------|------|-------|------------------|
| 1 | {{headline}} | {{source}} | {{date}} | {{rel}} | {{cred}} | "{{suggested_bullet}}" |

### Business Cases

| # | Company | Sector | Event | Source | Date | Suggested Bullet |
|---|---------|--------|-------|--------|------|------------------|
| 1 | {{company}} | {{sector}} | {{event_type}} | {{source}} | {{date}} | "{{suggested_bullet}}" |

### Suggested Beamer Content

```latex
\begin{frame}{{{SLIDE_TITLE}}}
\begin{center}
\begin{tikzpicture}
\node[factbox, fill=DeepRed!8] at (0, 0)
    {\textbf{{{FACT_HEADLINE}}}\\[0.2cm]
     {{FACT_BODY}}\\[0.1cm]
     {\scriptsize\textcolor{WarmGray}{Source: {{SOURCE}}}}};
\end{tikzpicture}
\end{center}
\vfill
\end{frame}
```

---

## Message B: {{MESSAGE_TEXT}}

[Same structure as Message A]

---

## Integration Notes

- **Slide X — Title**: Use Message A news bullet for the motivation frame.
- **Slide Y — Title**: Use Message B case bullet in the results transition.
- **Missing support**: [List any message that did not get strong coverage.]

---

## Sources

1. {{citation with URL}}
2. {{citation with URL}}
