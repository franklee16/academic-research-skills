# Datasets, Access, And Confidentiality

Use this before AI touches data or data descriptions.

## Data Sensitivity Classes

| Class | Examples | AI rule |
| --- | --- | --- |
| public aggregate | FRED, BEA, BLS, World Bank indicators | AI can help with public series IDs and code; log dates and transformations |
| public-use/registered microdata | IPUMS, public-use Eurostat, ESS | check terms; prefer metadata, codebooks, toy data |
| licensed institutional | WRDS, CRSP, Compustat, IBES, Bloomberg, FactSet | do not upload raw extracts unless license and institution allow |
| restricted/confidential | admin microdata, bank transactions, Nordic registers | no public AI upload without explicit approval |
| coauthored/private | drafts, referee reports, private notes | use only with consent and policy permission |

## Household Finance And Nordic Data

Useful sources include ECB HFCS, Eurostat public microdata, SHARE, ESS, LIS/LWS, Statistics Denmark, Statistics Sweden MONA, Statistics Norway, microdata.no, Sikt/NorLAG, Statistics Finland FIONA, and Statistics Iceland. These are access maps, not upload permission.

For Nordic register or household data, assume restricted remote access until proven otherwise. Use AI with metadata, questionnaires, codebooks, variable lists, toy rows, and synthetic examples.

## Copy-Ready Instruction

```text
Act as a data-access and AI-safety assistant for an economics/finance project.

First ask me for the dataset, provider, country, research use, access status, data sensitivity, and what materials I can safely share if I have not provided them.

Classify the data sensitivity. List what must not be uploaded to public AI. Suggest safer AI inputs such as metadata, variable dictionaries, public documentation, toy data, synthetic rows, or code only.

Identify license, institutional, IRB/ethics, journal, coauthor, data-provider, and output-disclosure rules I must check.

Propose a citation, version, access-date, and AI-use log.
```

## Dataset Access Checklist

Ask:

1. What is the dataset name, provider, version, and access date?
2. Is it public, licensed, restricted, confidential, embargoed, or coauthored?
3. Are cloud upload, public AI, external APIs, or MCP connectors allowed?
4. Can synthetic or toy data substitute for raw data?
5. What files must stay out of GitHub?
6. What citation and access statement belongs in the paper?
