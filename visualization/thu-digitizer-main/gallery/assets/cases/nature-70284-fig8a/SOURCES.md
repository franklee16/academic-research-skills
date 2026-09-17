# Sources, rights, and provenance

Retrieved on 2026-07-21 from first-party publisher, author-repository, and institutional-repository endpoints.

## Article and figure

- Article: Petra Sieber et al., "Climate response to Nature Future scenarios in a regional Earth System Model", *Nature Communications* 17, 4017 (2026), DOI [10.1038/s41467-026-70284-8](https://doi.org/10.1038/s41467-026-70284-8).
- Official Figure 8 PNG: <https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41467-026-70284-8/MediaObjects/41467_2026_70284_Fig8_HTML.png>
- Official article PDF: <https://link.springer.com/content/pdf/10.1038/s41467-026-70284-8.pdf>
- Official figure page: <https://www.nature.com/articles/s41467-026-70284-8/figures/8>
- Local official PNG: `original/41467_2026_70284_Fig8_HTML.png`, SHA-256 `030221d33457598cab08442d0af1d0add749a16aaa6860c4124862b2b5c07d3e`, 2001 x 1235 pixels.
- Figure 8a is the complete top row: two horizontal diverging simple-bar subplots for NfN-SSP1. The left subplot is temperature sensitivity in grid cells (degrees C per percent change); the right subplot is contribution to the regional temperature response (degrees C). Bars are means across 200 ridge fits. Error intervals are the 2.5th-97.5th bootstrap percentiles.

The article and its images are licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/), unless a separate credit line states otherwise. No separate credit line excludes Figure 8. This bundle identifies the article and authors, links the license, and identifies its modifications.

Modifications made here: review-only panel crops, detector overlays, a pixel-space recreation, consolidated CSV/JSON reports, and a validation-coverage graphic. Numeric measurement used the exact unresampled official PNG, not the crops.

## Supplementary data and mapping evidence

- Description of Additional Supplementary Files: <https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-026-70284-8/MediaObjects/41467_2026_70284_MOESM3_ESM.pdf>
- Supplementary Data 3: <https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-026-70284-8/MediaObjects/41467_2026_70284_MOESM6_ESM.xlsx>
- Author code: <https://github.com/pesieber/Sieber-etal-2026_NCOMMS>
- Article-cited code DOI: <https://doi.org/10.5281/zenodo.18511016>
- Author code license: MIT, copyright Petra Sieber (2026), recorded in the downloaded repository archive.

The official supplementary-file description says Supplementary Data 3 contains regional and scenario climate summaries. It does not describe the per-land-cover-transition ridge sensitivities, contributions, and intervals plotted in Figure 8a. The author notebook `5_PFT-transitions_Ridge.ipynb` maps Figure 8 to four generated files:

- `ridgeOutputs/std_T2m_nfn_coefmean.csv`
- `ridgeOutputs/std_T2m_nfn_coefci.csv`
- `ridgeOutputs/std_T2m_nfn_contribmean.csv`
- `ridgeOutputs/std_T2m_nfn_contribci.csv`

Those generated CSVs are absent from the downloaded code archive. Consequently, Supplementary Data 3 was retained as official source evidence but was not used to fill or correct the primary raster-extraction CSV.

Direct workbook inspection was not performed because the required `load_workspace_dependencies` capability was unavailable and `@oai/artifact-tool` was not importable in this environment. No fallback Excel parser was used. The official one-page supplementary description was read with `pdfplumber` under the PDF skill.

## Institutional dataset

- ETH Research Collection: <https://doi.org/10.3929/ethz-c-000795598>
- Item UUID: `c1c0290d-1889-4bff-83e1-5a10fdc649a6`
- ORIGINAL bundle UUID: `8df7de86-9981-4da1-996e-b72d7737f8e0`
- `data.zip`: bitstream UUID `71076fc5-8f8d-469e-8fc0-2824984f1804`, 12,885,635,127 bytes, repository MD5 `da744f8928a5b50a0dbfcd1681119f94`.
- `dataset_README.txt`: bitstream UUID `a7ec07f3-61ec-4d62-b6c7-2b29b0a36376`, repository MD5 `97fd12001bd4dce0df21975733721e5f`; the downloaded local file matches this MD5.

The 12.9 GB `data.zip` was not downloaded because it contains the broader analysis inputs rather than a small, direct Figure 8 source table. Repository metadata and the README were retained under `provenance/` and `original/`.

