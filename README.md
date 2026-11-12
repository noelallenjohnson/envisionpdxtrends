# Envision Portland Trends

Source for [envisionpdxtrends.com](https://envisionpdxtrends.com): how housing gets created in Portland, Oregon, by source of capital, 2000 to 2026. A project of Old i, LLC.

## What is here

| Path | What it is |
|---|---|
| `index.html` | The website. One self-contained page, rebuilt by the refresh. Do not edit by hand. |
| `projects.html` | The project list: a searchable table of every project counted. Also rebuilt by the refresh. |
| `pipeline/build_site.py` | The page template. All of the site's wording lives here. |
| `pipeline/build_projects_page.py` | The template for the project list page. |
| `pipeline/refresh.py` | Pulls City of Portland permit records and applies the counting rules. |
| `pipeline/frozen/` | Decisions and inputs that a person reviewed. The refresh never changes these. |
| `pipeline/out/` | What the last refresh produced. |

## The quarterly refresh

On the 5th of January, April, July and October, GitHub runs `refresh.py` and then `build_site.py`, and publishes the result. It can also be run at any time from the Actions tab: choose "Refresh site data", then "Run workflow".

Each refresh:

1. Pulls building permits, demolition permits and land use cases from the PortlandMaps permit feed.
2. Groups permits into projects, nets out demolitions, and tags each project by size and subsidy.
3. Applies every reviewed call in `frozen/reviewed_projects.csv`. Those always win over the rules.
4. Re-links land use approvals to permits, so approval-to-permit rates and timings stay current.
5. Stops without publishing if totals move more than expected in one quarter (a sign the city feed changed).

After a refresh, look at `pipeline/out/new_projects_to_review.csv`. It lists projects of five or more homes that are new since the November 2026 review and were tagged by rule only. To correct one, add a row to `frozen/reviewed_projects.csv`.

## What does not refresh by itself

- Population and household figures (`frozen/population.json`).
- The affordable-housing records used to find subsidized projects (`frozen/subsidy_records.csv`, gathered November 2026). New subsidized projects are still caught by permit wording, and otherwise appear in the review list.
- Unit counts for land use cases filed after November 2026 come from the city's short description, not the written decision, and are provisional.
- The page covers 2000 to 2026. Extending it to 2027 means editing the template.

## Counting rules

- New construction, conversions of non-residential buildings, and units added inside existing buildings count. Remodels, hotels, replacements and moves do not.
- Permits within 40 metres and 270 days of each other are one project.
- Net new is gross units minus homes demolished on the same site.
- Size classes by gross units: 1 to 4, 5 to 74, and 75 or more.
- Subsidized means state, local bond or tax-credit money, or university housing. Inclusionary housing alone is market rate. No evidence means market rate.

Data: City of Portland, Portland Permitting & Development, via PortlandMaps.
