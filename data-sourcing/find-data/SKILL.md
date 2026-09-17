---
name: find-data
description: Help researchers identify and catalog relevant datasets for empirical research. Use this skill whenever a user asks to find data, locate datasets, identify data sources, or asks "what data exists for...", "where can I get data on...", "is there a dataset that...", or similar. Also trigger when the user describes a research question and needs to know what data could support it, asks about data availability for a particular topic or geography, wants to compare data sources, or mentions needing panel data, cross-sectional data, or time-series data for a project. Trigger on mentions of "find data", "data search", "dataset", "data source", "microdata", "administrative data", "survey data", "public-use data", "restricted data", or when the user specifies parameters like time windows, geographic levels, or data frequency in the context of research. Also trigger when the user asks for help downloading, scraping, or structuring a dataset that has been identified.
---

# Find Data Skill

Help researchers discover, evaluate, and catalog datasets for empirical research projects.

This skill conducts comprehensive, creative searches across government databases, public repositories, academic replication archives, NGO reports, and structured web content to identify datasets matching a researcher's needs. It goes well beyond the obvious sources.

---

# Input Parameters

Gather the following from the user before searching. If any are missing, ask.

| Parameter | Required | Description | Examples |
|-----------|----------|-------------|----------|
| **Topic / research question** | Yes | The substantive area or specific question | "effect of ICE enforcement on mental health", "childcare labor supply" |
| **Time window** | Yes | The years or date range needed | 2010–2023, pre/post 2012, monthly 2005–2020 |
| **Data frequency** | Yes | How granular in time | Annual, quarterly, monthly, weekly, daily |
| **Level of analysis** | Yes | Geographic and/or unit level | National, state, county, ZIP, census tract, individual, firm, school, hospital |
| **Topic filter** | Optional | Broad domain to focus the search | Health, crime, education, labor, immigration, housing, environment |
| **Outcome vs. treatment data** | Optional | Whether the user needs outcome measures, policy/treatment variation, or both | "I need the outcome side — mental health measures at the county-month level" |

If the user provides a research question rather than structured parameters, infer the parameters and confirm them before proceeding.

---

# Search Strategy

The goal is to be **thorough and creative**, not just to list the obvious datasets everyone already knows. A good data search for a researcher should surface sources they haven't already thought of.

## Phase 1: Systematic search across source categories

For each category below, conduct targeted web searches combining the user's topic, geography, and time parameters. Use multiple search queries per category — vary keywords, use acronyms, try both the agency name and the dataset name.

### Category A: Federal statistical agencies and surveys
Census Bureau (ACS, CPS, decennial, SIPP, ASE, CBP, QWI), BLS (QCEW, JOLTS, OES, CES, ATUS), BEA (REIS, GDP by state/metro), NCHS (NVSS, NHIS, NHANES, NAMCS, NHAMCS), CDC (BRFSS, WONDER, WISQARS, YRBSS, PRAMS), SAMHSA (NSDUH, TEDS, N-SSATS), DOJ/BJS (NCVS, UCR/NIBRS, NPS, NCRP, LEMAS), DOE/NCES (CCD, IPEDS, ECLS, NAEP, ELS, HSLS), HHS (MEPS, MAX/TAF Medicaid, CMS Medicare), USDA (SNAP QC, FNS data, ERS), HUD (HMDA, PIC, LIHTC), EPA (TRI, AQS, ECHO), SSA (administrative earnings, OASDI), IRS (SOI), Federal Reserve (SCF, SHED, Call Reports), DHS (immigration statistics yearbook), ICE (detention, removals), DOL (UI claims, WARN), FEMA, FDA, NIH/NCI (SEER), AHRQ (HCUP, SID, NIS).

### Category B: State and local government data
State health departments, vital statistics offices, child welfare agencies (state-level NCANDS extracts), state court systems (PACER for federal, state judiciary sites for state), departments of corrections, state education agencies, state labor/workforce agencies, police departments (some publish incident-level data), medical examiner/coroner offices, state insurance commissioners, state Medicaid agencies, county assessor/recorder offices.

### Category C: Academic and research data repositories
ICPSR, Harvard Dataverse, OpenICPSR, Roper Center, IPUMS (CPS, ACS, NHIS, ATUS, DHS, NHGIS, Terra), Stanford Open Policing Project, Opportunity Insights, Chetty/Hendren mobility data, Eviction Lab, Police Scorecard, Marshall Project, Vera Institute, Gun Violence Archive, RAND datasets, Urban Institute, Replication packages from published papers in the relevant literature (search AEA registry, journal supplementary materials, authors' websites, GitHub).

### Category D: International and cross-country sources
WHO, World Bank (WDI, microdata), OECD, UN agencies, Eurostat, DHS Program (Demographic and Health Surveys), LSMS, European Social Survey, Latinobarómetro, country-specific statistical offices.

### Category E: Private, NGO, and organizational data
Robert Wood Johnson Foundation (County Health Rankings), KFF, Annie E. Casey (KIDS COUNT), Guttmacher Institute, March of Dimes (PeriStats), National Alliance on Mental Illness, National Council on Aging, foundations and think tanks that publish data (Brookings, AEI, Pew, Gallup), industry associations, professional organizations, hospital/insurer data (some publicly available).

### Category F: Creative and non-traditional sources
This is where the skill should shine. Think beyond conventional datasets:

- **Structured web content that could be scraped**: memorial/honor pages (ODMP for police line-of-duty deaths, fallen firefighter databases), court filing databases, state licensing board records, inspection reports (OSHA, restaurant health, nursing homes), public meeting minutes, campaign finance records, lobbying disclosures, government contract databases (USASpending, FPDS), charity tax filings (IRS 990s via ProPublica), FDA adverse event reports (FAERS), medical board disciplinary actions, environmental permit databases, building permit records, property transaction records, utility rate filings, public salary databases.
- **Social media and digital trace data**: Google Trends, Twitter/X Academic API (historical), Reddit data (Pushshift archive), Yelp/Google reviews, news article archives (NewsBank, ProQuest, media cloud), Wayback Machine for historical web content.
- **Call/hotline data**: 988/crisis hotline data (Vibrant Emotional Health), poison control center data (AAPCC), domestic violence hotline logs, 311/911 call data from cities.
- **Administrative byproducts**: FOIA-able records, state sunshine law requests, public records databases, declassified records.
- **Satellite and geospatial**: nighttime lights (VIIRS/DMSP), land use/land cover (NLCD), air quality satellite data (NASA), traffic data (FHWA, state DOTs), cell phone mobility data (SafeGraph, Streetlight — some periods publicly available).

### Category G: Restricted-access and application-required data
IRS administrative tax data (via Census RDC), SSA earnings records, state Medicaid claims (via DUA), Medicare claims (CMS RDC or ResDAC), LEHD/LODES, restricted Census microdata (via FSRDC), FBI NIBRS restricted files, NCANDS child-level data (via NDACAN), state vital records with identifiers, VA health records, prison administrative records, employer-employee matched data (LEHD), credit bureau data (via Fed or research agreements), EHR data (via health system partnerships).

## Phase 2: Targeted deep-dive searches

After the systematic pass, run additional web searches for:

1. **Recent working papers** using data on the topic (search NBER, SSRN, Google Scholar for "[topic] [method]" papers from the last 2–3 years — their data sections reveal sources)
2. **Data appendices and replication files** from closely related published work
3. **Data inventories and guides** (e.g., "guide to crime data", "[topic] data resources for researchers")
4. **Government data catalog searches** (data.gov, specific agency data portals)
5. **Specialized data aggregators** for the topic area

## Phase 3: Verify and enrich

For each promising dataset identified:

1. **Visit the actual data page** (use web_fetch) to confirm availability, format, and coverage
2. **Check for a data dictionary or codebook** — link it if available
3. **Note the access mechanism** — direct download, API, application, FOIA, RDC, etc.
4. **Identify the actual file format(s)** available
5. **Assess time and geographic coverage** against the user's parameters
6. **Note any known limitations** — sampling, suppression, definitional changes, missing years

---

# Output Format

Organize all identified datasets into three tiers, then present each with a structured entry.

```markdown
# Dataset Search Results

**Research question:** [user's question/topic]
**Parameters:** [time window] | [frequency] | [level of analysis] | [topic filter]
**Date of search:** [YYYY-MM-DD]

---

## Tier 1: Publicly Available and Ready to Use

Datasets that can be downloaded now with no application or agreement required.

### [Dataset Name] ([Abbreviation])

| Field | Detail |
|-------|--------|
| **Source** | [Agency/organization] |
| **Access** | [Direct download URL or portal] |
| **Format** | [CSV, Stata .dta, SAS, fixed-width, API, Excel, etc.] |
| **Level** | [Individual, county, state, etc.] |
| **Time coverage** | [Start–End, frequency] |
| **Data dictionary** | [Link if available, or "not available — would need to be constructed from documentation"] |
| **Novelty** | [Commonly used / Moderately known / Underutilized / Novel] |

**What it contains:** [2–3 sentence description of key variables relevant to the user's question]

**Limitations:** [Representativeness, suppression cells, definitional breaks, missing periods, measurement issues]

**How to get it:** [Step-by-step: go to URL, select parameters, download — be specific]

---

## Tier 2: Publicly Available but Requires Scraping or Processing

Data that exists on the public web but is not in a ready-to-analyze format.

### [Source Name]

| Field | Detail |
|-------|--------|
| **Source** | [URL] |
| **Current format** | [HTML tables, PDFs, interactive dashboards, individual records on web pages] |
| **Target format** | [What it would look like after processing — CSV with columns X, Y, Z] |
| **Level** | [What unit of observation could be constructed] |
| **Time coverage** | [What periods are available] |
| **Scraping complexity** | [Low / Medium / High — with brief explanation] |
| **Novelty** | [Commonly used / Moderately known / Underutilized / Novel] |

**What it contains:** [Description of available information]

**Limitations:** [Completeness, consistency over time, legal/ToS considerations for scraping]

**How to obtain:** [Scraping approach — what tools, what the page structure looks like, whether an API is hidden behind the frontend, whether pagination is involved]

---

## Tier 3: Restricted-Access Data

Datasets that require applications, data use agreements, or secure access.

### [Dataset Name]

| Field | Detail |
|-------|--------|
| **Source** | [Agency/organization] |
| **Access mechanism** | [RDC, DUA, application, FOIA, partnership] |
| **Format** | [If known] |
| **Level** | [Individual, county, etc.] |
| **Time coverage** | [Start–End] |
| **Typical approval timeline** | [Weeks/months/years] |
| **Cost** | [If applicable — RDC fees, data purchase costs] |
| **Novelty** | [Commonly used / Moderately known / Underutilized / Novel] |

**What it contains:** [Key variables]

**Limitations:** [Output disclosure review, cell suppression, restrictions on linking]

**How to access:**
1. [Step-by-step application process]
2. [Who to contact — specific office, email, or URL]
3. [What is required — IRB approval, proposal, DUA, institutional affiliation]
4. [Tips — e.g., "processing times are faster if you apply through a Census RDC rather than directly"]

---

## Summary Table

| Dataset | Tier | Level | Frequency | Coverage | Format | Novelty |
|---------|------|-------|-----------|----------|--------|---------|
| ... | 1/2/3 | ... | ... | ... | ... | ... |

---

## Suggested Combinations

[If relevant, suggest how datasets could be linked or combined to answer the research question. Note which identifiers enable merging — FIPS codes, year, SSN (in restricted settings), etc.]

---

## Next Steps

[Offer to help with any of the following:]
- Download and inspect specific Tier 1 datasets
- Write scraping code for Tier 2 sources
- Draft a data access application for Tier 3 sources
- Construct a data dictionary for a source that lacks one
- Merge or harmonize multiple datasets
```

---

# Post-Search Assistance

When the user asks for follow-up help after the initial search, the skill should assist with:

## Downloading and inspecting data
- Fetch data files via URL or API
- Load into Python/Stata and describe contents (variables, observations, time coverage, missingness)
- Check whether the data matches what was advertised

## Scraping
- Write Python scraping scripts (requests + BeautifulSoup, or Selenium for dynamic pages)
- Handle pagination, rate limiting, and error recovery
- Parse PDFs with tabula-py or pdfplumber
- Structure raw scraped content into analysis-ready formats
- Respect robots.txt and terms of service — flag legal concerns

## Data access applications
- Draft research proposals or data use agreement applications
- Help write IRB protocols for restricted data
- Identify the correct contact person or office
- Suggest institutional resources (e.g., Census RDC locations, NCHS RDC)

## Data dictionary construction
- When a codebook doesn't exist, build one by inspecting the data, documentation, and related papers
- Document variable names, types, value labels, missing codes, and notes

---

# Important Guidance

- **Err on the side of inclusion.** It's better to surface a dataset that turns out to be slightly off-target than to miss something useful. The researcher can filter; they can't discover what you didn't show them.
- **Be honest about limitations.** Don't oversell a dataset. If coverage is spotty, say so. If the variable the user needs is a rough proxy, say so.
- **Prioritize novelty.** The researcher probably already knows about the CPS and the ACS. The real value of this skill is surfacing the less obvious sources — the ODMP memorial database, the state-level court filing records, the FOIA-able administrative data, the replication file from a 2023 working paper that assembled a novel dataset.
- **Verify before reporting.** Use web_fetch to confirm that links work, that the data is actually available in the described format, and that coverage matches what you claim. Stale links and defunct portals erode trust.
- **Search broadly, report precisely.** Run many searches, but only include datasets in the output that are genuinely relevant to the user's parameters.
- **Think like a research assistant who has been given two days to find every possible data source.** Be resourceful, creative, and exhaustive.
