# Strategic Analyst

A McKinsey-style strategic analysis assistant that helps executives, investors, students, and industry entrants build systematic industry认知 and make data-driven decisions.

## When to Use

Activate this skill when the user needs:
- Industry analysis or market research
- Competitive landscape assessment
- Market entry strategy support
- Investment decision backing
- Strategic framework application (Porter's Five Forces, TAM-SAM-SOM, PESTEL, etc.)

Typical triggers:
- "帮我分析XX行业"
- "战略分析"
- "竞争格局"
- "市场研究"
- "麦肯锡"
- "进入XX行业"

## How It Works

1. **Needs Diagnosis**: Identify user identity (CEO/executive/student/entrant) and core decision problem.
2. **Multi-source Data Collection**: Auto-search latest industry data via Tavily/WebSearch. Extract tables from PDFs, dynamic web pages, and images (OCR).
3. **Framework-driven Analysis**: Apply 6 classic frameworks:
   - Industry Structure (Porter's Five Forces)
   - Market Sizing (TAM-SAM-SOM)
   - Competitive Landscape
   - Trend Analysis (PESTEL)
   - Value Chain
   - Key Success Factors
4. **Mandatory Artifact**: Save `data_collection.md` — a forced intermediate log of all search queries, tools used, source URLs, and raw snippets.
5. **Report Generation**: Output both Markdown and HTML reports. HTML tables support hover-to-download PNG/SVG buttons.
6. **Quality Gate**: Auto-check structure, framework usage, professional tone, data backing, and source-link completeness before delivery.

## Key Files

- `skill.yaml` — Skill configuration
- `agent_instructions.md` — Agent persona, data transparency rules, and professional boundaries
- `tools/data_collector.py` — Structured data collection with source URLs and credibility ratings
- `tools/report_generator.py` — Dual-format report generator (Markdown + HTML) with table-download JS
- `tools/quality_gate.py` — Automated quality checks
- `frameworks/` — 6 analysis framework templates
- `templates/` — Report templates (executive summary, student edition, full report)
- `checklists/` — Pre-analysis, data collection, quality check, and boundary checklists
- `data_sources/` — General and industry-specific data source guides

## Prerequisites

**Tavily API Key is required** for deep research-grade search.
- Sign up at https://tavily.com to get an API key.
- Add it to `settings.json` under `mcpServers.tavily`:

```json
{
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@0.1.4"],
      "env": {
        "TAVILY_API_KEY": "tvly-your-api-key"
      }
    }
  }
}
```

If Tavily is not configured, the skill will fall back to WebSearch, but deep research capabilities will be limited.

## Output Standards

- All key data (market size, growth forecasts, competitive shares) must include source links in `[source](URL)` Markdown format.
- Credibility star ratings (★★★★★ to ★☆☆☆☆) are required for every data point.
- HTML reports use a professional black/red/gray financial-research style with clickable source links and table image downloads.
- No "action list" or "next steps" sections per style guide.
