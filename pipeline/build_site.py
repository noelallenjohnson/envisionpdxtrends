"""Envision Portland Trends: page template. All site wording lives in this file.
Reads pipeline/out/data.json and writes index.html at the top of the repository."""
import os
HERE=os.path.dirname(os.path.abspath(__file__))
D=open(os.path.join(HERE,'out','data.json')).read()
html=r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Envision Portland Trends</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@400;600;700&family=Libre+Franklin:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{ /* layout: white page, black slab headings, purple for brand, rules and controls; one reading column with wide figures; single light theme by choice */
  --purple:#500082; --purple-deep:#280050; --gold:#FFBE0A; --ink:#111; --ink2:#555; --rule:#E4E0E8; --wash:#F6F3F8; --page:#fff;
  --s75:#7A2FB5; --s14:#A86F00; --s574:#00909A; --band:#EDE9F1; --display:"Zilla Slab",Rockwell,Georgia,serif; --body:"Libre Franklin","Helvetica Neue",Arial,sans-serif; color-scheme:light}
*{box-sizing:border-box} html{scroll-behavior:smooth}
body{margin:0;background:var(--page);color:var(--ink);font:400 17px/1.6 var(--body)}
a{color:var(--purple)} a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
header.top{border-bottom:3px solid var(--purple);position:sticky;top:0;background:var(--page);z-index:5}
.bar{max-width:1080px;margin:0 auto;padding:12px 20px;display:flex;flex-wrap:wrap;gap:8px 28px;align-items:baseline;justify-content:flex-start}
.brand{font:700 22px/1.1 var(--display);color:var(--purple);text-decoration:none}
nav{display:flex;flex-wrap:wrap;gap:4px 18px} nav a{font:500 14px var(--body);text-decoration:none;color:var(--ink)} nav a:hover{color:var(--purple);text-decoration:underline}
main{max-width:1080px;margin:0 auto;padding:0 20px 80px}
.hero{padding:52px 0 20px;display:grid;gap:18px}
.eyebrow{font:600 13px var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--purple)}
h1{font:700 clamp(34px,5.4vw,60px)/1.05 var(--display);color:var(--ink);margin:0;max-width:18ch;text-wrap:balance}
.lede{font-size:20px;max-width:62ch;margin:0}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:0 24px;border-top:3px solid var(--ink);margin:16px 0 4px}
.tile{padding:16px 0 14px;border-bottom:1px solid var(--rule)} .tile b{display:block;font:700 40px/1 var(--display);color:var(--ink);font-variant-numeric:tabular-nums} .tile span{font-size:14px;color:var(--ink2);display:block;margin-top:6px;max-width:30ch}
section{padding:40px 0 8px;border-top:1px solid var(--rule);margin-top:34px}
h2{font:700 clamp(26px,3.4vw,38px)/1.12 var(--display);color:var(--ink);margin:0 0 10px;max-width:26ch;text-wrap:balance}
h3{font:600 20px/1.25 var(--display);margin:26px 0 6px}
p{max-width:66ch;margin:0 0 14px} .note{font-size:14px;color:var(--ink2);max-width:80ch}
figure{margin:22px 0 10px} figcaption{font:600 16px/1.35 var(--body);margin-bottom:4px} .sub{font-size:14px;color:var(--ink2);margin-bottom:10px}
.ctrl{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;margin:6px 0 10px}
.seg{display:inline-flex;border:1px solid var(--purple);border-radius:4px;overflow:hidden} .seg button{font:500 14px var(--body);padding:6px 12px;border:0;background:#fff;color:var(--purple);cursor:pointer} .seg button[aria-pressed=true]{background:var(--purple);color:#fff}
.tbtn{font:500 14px var(--body);padding:6px 12px;border:1px solid var(--rule);border-radius:4px;background:#fff;cursor:pointer;color:var(--ink)}
.thr{background:var(--wash);border-left:6px solid var(--purple);padding:14px 18px;margin:18px 0;display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;max-width:820px} .thr label{font-weight:600} .thr output{font:700 22px var(--display);min-width:3ch} input[type=range]{accent-color:var(--purple);width:220px}
.legend{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:14px;margin:4px 0 6px} .legend i{display:inline-block;width:12px;height:12px;border-radius:2px;margin-right:6px;vertical-align:-1px}
.chart{position:relative} svg{display:block;width:100%;height:auto} .ax{font:12px var(--body);fill:var(--ink2)} .grid{stroke:var(--rule)} .lab{font:600 12px var(--body);fill:var(--ink)} .bandl{font:600 11px var(--body);fill:var(--ink2)}
.tip{position:absolute;pointer-events:none;background:#fff;border:1px solid var(--ink);border-radius:4px;padding:8px 10px;font-size:13px;line-height:1.45;box-shadow:0 4px 14px rgba(40,0,80,.15);min-width:180px;display:none;z-index:3} .tip b{font-family:var(--display);font-size:15px}
.tw{overflow-x:auto;margin:8px 0} table{border-collapse:collapse;font-size:14px;font-variant-numeric:tabular-nums;min-width:520px} th,td{padding:6px 12px;border-bottom:1px solid var(--rule);text-align:right} th:first-child,td:first-child{text-align:left;white-space:nowrap} #eras td:nth-child(2),#eras th:nth-child(2){text-align:left} th{font-weight:600;border-bottom:2px solid var(--ink)}
table.wide td:first-child,table.wide th:first-child{min-width:220px;white-space:normal} table.wide td{vertical-align:top} table.wide td.l,table.wide th:nth-child(2){text-align:left} table.wide td.l{max-width:46ch}
.who{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px;margin:18px 0}
.who div{border-top:6px solid var(--c);padding-top:10px} .who h3{margin:0 0 4px} .who b{font:700 30px var(--display);font-variant-numeric:tabular-nums} .who p{font-size:15px;margin:6px 0 0}
.call{background:var(--wash);border-left:6px solid var(--gold);padding:16px 20px;margin:20px 0;max-width:74ch} .call p{margin:0}
.mapwrap{position:relative;max-width:820px;border:1px solid var(--rule)} canvas{display:block;width:100%;height:auto}
.yr{font:700 44px/1 var(--display);position:absolute;left:14px;top:10px;color:var(--ink)}
footer{border-top:3px solid var(--purple);margin-top:56px;padding:22px 0;font-size:14px;color:var(--ink2)} footer p{max-width:86ch;margin:0 0 8px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media (max-width:700px){.chart{overflow-x:auto;-webkit-overflow-scrolling:touch} .chart svg{width:760px;max-width:none} figure .sub::after{content:" Swipe the chart sideways to see earlier years.";font-style:italic} figure .sub.wait::after{content:" Swipe the chart sideways to see longer waits."} #rushtab td:first-child,#rushtab th:first-child{min-width:170px} #eras td:nth-child(2),#eras th:nth-child(2){min-width:190px} table{font-size:13px} th,td{padding:6px 9px}}
</style></head><body>
<header class="top"><div class="bar"><nav aria-label="Sections"><a href="#sources">Funding Sources</a><a href="#large">Investable?</a><a href="#where">Where $ Flows</a><a href="#approvals">Macro Shocks</a><a href="#time">City (dis)Approval</a><a href="#overcount">Honest Acctg</a><a href="#method">Method</a><a href="#about">About</a></nav></div></header>
<main id="top">
<div class="hero"><div class="eyebrow">This century's housing creation in Portland, Oregon &middot; 2000 to 2026</div>
<h1>How a city funds housing creation</h1>
<p class="lede">Housing production is a flow; thus, ratios and rates are the measures.</p>
<div class="tw" id="ctx"></div>
<p class="note">Homes are net new homes in completed projects, counted in the year the project was finished. Population: U.S. Census (2000, 2010, 2020) and the Portland State University estimate for 2025. Households: Census 2000 and 2010, and a 2026 private estimate (Esri). A check on the count: the Census reports 28,201 more housing units in Portland in 2010 than in 2000; whereas this dataset finds <span id="chk"></span> net new homes completed over the same years. The reason for the discrepancy is unknown; but affirms the scale and directionality implied by this data, which is through <span class="asof"></span>. A figure above 1.0 in the last column means more homes were completed than households were added; it does not measure price, vacancy, or need that existed before 2000.</p></div>

<section id="sources"><h2>Funding new homes</h2>
<p>New homes are funded by different sources of money. The size of a project is one way to understand this.</p>
<div class="thr"><label for="thr">Institutional investors scale; you can decide where "big money" starts via</label><input type="range" id="thr" min="50" max="100" step="5" value="75"><output id="thrv">75</output><span>homes per project. (Move the slider to reflect your definition; every chart on this page follows it.)</span></div>
<div class="who" id="who"></div>
<figure><figcaption>New homes each year, by source of capital</figcaption><div class="sub" id="sub1"></div>
<div class="ctrl"><div class="seg" role="group" aria-label="Date basis"><button id="b-iss" aria-pressed="true">By year permit issued</button><button id="b-st" aria-pressed="false">By year project applied</button></div><button class="tbtn" data-t="t1">Show table</button></div>
<div class="legend" id="lg1"></div><div class="chart" id="c1"></div><div class="tw" id="t1" hidden></div></figure>
<figure><figcaption>Each source's share of new homes, year by year</figcaption><div class="sub">Share of homes permitted, by year permit issued</div>
<div class="chart" id="c1b"></div></figure>
<p id="sharetext"></p>
<p id="voltext"></p>
<p class="note" id="fcnote"></p></section>

<section id="large"><h2>Large-project housing production is now entirely subsidized</h2>
<p>Institutional-scale projects are funded either by private investors or by public subsidy. Splitting them shows market rate investment forces historically power housing production.</p>
<figure><figcaption id="cap2"></figcaption><div class="sub">By year the first building permit was issued. Lighter bars are a projection.</div>
<div class="ctrl"><button class="tbtn" data-t="t2">Show table</button></div>
<div class="legend" id="lg2"></div><div class="chart" id="c2"></div><div class="tw" id="t2" hidden></div></figure>
<div class="call"><p id="callout" style="margin-bottom:10px"></p><p id="callout2"></p></div>
<figure><figcaption>Subsidized share of all homes permitted, year by year</figcaption><div class="sub">Subsidized homes as a share of homes permitted each year, across projects of every size. Dark lines show the average for each period.</div>
<div class="ctrl"><button class="tbtn" data-t="t9">Show table</button></div>
<div class="chart" id="c9"></div><div class="tw" id="t9" hidden></div></figure>
<p id="subshare"></p>
<p class="note">Subsidized means a project receiving state, local bond or federal tax-credit money, or university housing. A market-rate project that includes required inclusionary units is counted as market rate because it receives no public money: the below-market rents are paid for inside the building, by its market-rate renters. When a rule requires some rents to be below market and does not offset the cost, it subsidizes some residents through others. Economists describe such a requirement as a tax on new housing paired with a price ceiling on the required homes (<a href="https://openyls.law.yale.edu/entities/publication/201901c5-a5c4-4999-8850-1f1d7bdc3732">Ellickson, "The Irony of 'Inclusionary' Zoning," 1981</a>). Oregon law now reflects this: Senate Bill 1521, signed in March 2026, requires Portland-area cities with an inclusionary mandate to offset its cost in full through payments, tax exemptions or fee waivers (<a href="https://www.sightline.org/2026/03/05/oregons-new-path-to-inclusionary-housing-fully-funded-and-flexible/">Sightline Institute summary</a>). Tags for the largest and most recent projects were checked one by one; older and smaller projects rely on matching to public affordable-housing records.</p></section>

<section id="where"><h2>Where new homes are built is always changing</h2>
<p>Each dot is a project, sized by its number of homes and colored by its source of capital. Move through the years to see which parts of the city each source favoured, and when it left. (Who builds the 'burbs, in the core, proximate to transit, etc.)</p>
<div class="ctrl"><button class="tbtn" id="play">Play</button><input type="range" id="yr" min="2000" max="2026" step="1" value="2017" aria-label="Year"><div class="seg" role="group" aria-label="Map mode"><button id="m-year" aria-pressed="true">That year only</button><button id="m-cum" aria-pressed="false">Everything so far</button></div></div>
<div class="legend" id="lg4"></div>
<div class="mapwrap"><div class="yr" id="yrv">2017</div><canvas id="map" width="1640" height="1456" role="img" aria-label="Map of Portland showing housing projects by year"></canvas></div>
<p class="note" id="maptext"></p>
<p id="todtext"></p></section>

<section id="approvals"><h2>National recessions reset housing production flows</h2>
<p>The city's two approval systems, land use and building permit, decide when larger buildings can proceed. Slower approvals can be seen to align with smaller flows, especially when the flow is cut off by a national recession. The math is simple: the longer approval takes, the shorter the window of time in which market-rate-funded production can occur.</p>
<figure><figcaption>Homes approved in design and historic reviews, and how many went on to a building permit</figcaption><div class="sub">By year of land use decision. Shaded: the financial crisis, COVID, and the rise in inflation / rates.</div>
<div class="ctrl"><button class="tbtn" data-t="t3">Show table</button></div>
<div class="legend" id="lg3"></div><div class="chart" id="c3"></div><div class="tw" id="t3" hidden></div></figure>
<div class="tw" id="eras"></div>
<p id="lutext"></p>
<p class="note">Cases for 2010 to mid-2020 were transcribed by hand from city records; later cases were read from the written decisions. Cases before 2010 were read by script from the city's short case descriptions and are provisional. A case is linked to a building permit when the decision names the permit or when a permit of similar size was filed on the same site; some real links are missed, so the share lost is an upper estimate. Approvals from the last three years may still proceed.</p></section>

<section id="rush"><h2>Before and after the 2017 inclusionary housing requirement</h2>
<p>Portland adopted an inclusionary housing requirement that took effect on February 1, 2017.  For buildings of 20 or more homes, a fee, or below-market rents on a share of the homes was imposed; this tax being paid by the building's market rate renters (<a href="https://openyls.law.yale.edu/entities/publication/201901c5-a5c4-4999-8850-1f1d7bdc3732">Ellickson, 1981</a>). Applications on file before the deadline exempted a project, so vesting was an option in the sense finance theory uses the word: the right, without the obligation, to build later under the old rules. An option is worth paying for when the future is uncertain (<a href="https://www.jstor.org/stable/1814815">Titman, "Urban Land Prices Under Uncertainty," 1985</a>), which explains the rush to file; the record suggests this one often went unexercised. From February 2018 through 2019, homes permitted in projects of that size ran about <span id="izgap">22%</span> below the pace seen from 2014 to 2017.</p>
<figure><figcaption>Projects of 20 or more homes: land use applications filed and building permits issued, month by month</figcaption><div class="sub">Homes in each month's land use filings and in each month's building permits, 2011 to 2019. The line marks February 1, 2017.</div>
<div class="ctrl"><button class="tbtn" data-t="t7">Show table</button></div>
<div class="legend" id="lg7"></div><div class="chart" id="c7"></div><div class="tw" id="t7" hidden></div></figure>
<div class="tw" id="rushtab"></div>
<p id="rushtext"></p>
<p class="note">The 20-home line is the rule's own threshold and does not follow the slider above. Land use applications are design and historic reviews, which only projects in design overlay areas need; they are counted in the month the application was filed, whatever the later decision. The red boxes and arrows are interpretation: each arrow points about 13 months ahead, roughly the time a filed project takes to show up in permits (IH is inclusionary housing). An application counts as never reaching a permit when no building permit has been issued for it to date. It is linked to a building permit when the decision names the permit or a permit of similar size was filed on the same site; some real links are missed in every period, so the rates are upper estimates. Construction cost data is not part of this dataset: the cost explanation is an interpretation of the pattern.</p></section>

<section id="time"><h2>Getting to a permit takes about three times as long as in 2000</h2>
<figure><figcaption>Months to reach a building permit</figcaption><div class="sub">Median, by year. Shaded: the same three downturns.</div>
<div class="ctrl"><button class="tbtn" data-t="t5">Show table</button></div>
<div class="legend" id="lg5"></div><div class="chart" id="c5"></div><div class="tw" id="t5" hidden></div></figure>
<p id="durtext"></p>
<figure><figcaption>How long projects waited for a building permit, year by year</figcaption><div class="sub wait">The segment producing the least total housing has the fastest city services.  Note, for larger projects, the below wait times exclude their need to gain land use (design / zoning) approval; those add typically 6 to 12 months. Building permit times are from application to first permit issued. Press Play to watch the waits lengthen.</div>
<div class="ctrl"><button class="tbtn" id="dplay">Play</button><input type="range" id="dyr" min="2000" max="2026" step="1" value="2025" aria-label="Year permit issued"><button class="tbtn" data-t="t6">Show table</button></div>
<div class="chart keepleft" id="c6"></div><div class="tw" id="t6" hidden></div></figure>
<p class="note">Bars show the share of that size's projects issued a permit that year; the count is given at the right of each panel, and some years have only a handful of large projects. The last bar holds every wait of 30 months or more. The dashed lines mark the medians for the normal, higher volume housing production years. Records begin in January 2000, so permits issued in 2000 and 2001 cannot show waits longer than one to two years. 2026 is a partial year.</p>
<h3 style="font:700 22px var(--display);margin:34px 0 8px">With land use review included</h3>
<p>Larger projects in design overlay areas need a land use review before they can apply for a building permit. For projects of 75 or more homes whose review could be matched to a permit, this is the wait from filing the land use application to receiving the first building permit.</p>
<figure><figcaption>Large projects: months from land use filing to building permit</figcaption><div class="sub">Each dot is one project of 75 or more homes, placed at the year its first building permit was issued. Colored lines are the median for each kind of funding in each period, where at least three projects were permitted; the shaded band is the middle half of all projects. The number of projects in each period is in parentheses.</div>
<div class="ctrl"><button class="tbtn" data-t="t8">Show table</button></div>
<div class="legend" id="lg8"></div><div class="chart" id="c8"></div><div class="tw" id="t8" hidden></div></figure>
<div class="tw" id="luwtab"></div>
<p id="luwtext"></p>
<p class="note">Fixed at 75 homes; this table does not follow the slider. It counts only projects that reached a building permit, so projects still waiting are not included, and the number of projects is small.</p></section>

<section id="overcount"><h2>What the city's permit records count as new homes</h2>
<p>The city's permit system carries a "new units" figure on each permit, but adding that column up counts homes that were never added. These are the ways it happens, with the number found in the record for 2000 to 2026.</p>
<div class="tw"><table class="wide"><thead><tr><th>What the record shows</th><th>What actually happened</th><th>Records</th><th>Units or lots</th></tr></thead><tbody>
<tr><td>Demolish and replace</td><td class="l">A home is torn down and new housing built on the same site. Only the difference is new.</td><td>3,693 projects</td><td>4,604</td></tr>
<tr><td>Remodel recorded as a new unit</td><td class="l">A kitchen addition or bathroom remodel carries a new-unit figure, though no home is added.</td><td>576 permits</td><td>1,565</td></tr>
<tr><td>Hotel rooms recorded as units</td><td class="l">New hotels and motels carry a new-unit figure.</td><td>15 permits</td><td>1,057</td></tr>
<tr><td>Middle housing land divisions</td><td class="l">A land use approval splits an already-permitted fourplex or cottage cluster onto separate lots. The lots are not additional homes.</td><td>237 cases since 2020</td><td>1,026</td></tr>
<tr><td>Permits that expired</td><td class="l">Units on permits that were never built remain in the record.</td><td>428 permits</td><td>558</td></tr>
<tr><td>Whole project counted on every permit</td><td class="l">Each townhouse permit in a nine-home project shows nine units.</td><td>42 permits</td><td>206</td></tr>
<tr><td>Replacement or relocated homes</td><td class="l">Replacement manufactured homes, moved houses and fire rebuilds.</td><td>137 permits</td><td>157</td></tr>
</tbody></table></div>
</section>

<section id="method"><h2>About this data</h2>
<h3>Sources</h3><p>The land use and permit figures shown here come from the City of Portland's own records. The city has two approval steps for housing - land use approvals, where a project needs one, and building permit approvals. All counts are pulled from the city's official land use decisions - via City Auditor's Efiles archives. For building permit approvals, the City of Portland's public permit records are used via PortlandMaps. Distinction between market rate versus public/subsidized housing production comes from subsidy records of the Oregon Affordable Housing Inventory, Metro's Regulated Affordable Housing Inventory, the Portland Housing Bureau and Oregon Housing and Community Services - cross referenced to the specific building permit for each project. Every project counted here can be reviewed in the <a href="projects.html">project list</a>.</p>
<h3>What counts as a new home</h3><p>New construction, conversions of offices and hotels into housing, and homes added inside existing buildings such as accessory dwelling units. Remodels, hotels and replacements do not count. Demos that removed a home to build a new home in its place do not count as adding housing.</p>
<h3>Projects</h3><p>Because townhouses and subdivisions are approved as one project, but each home holds its own building permit, a 40 meters proximity and 270 days relationship was used to distinguish a discrete development. For example, a 14-home townhouse project counts once, at its real size (instead of as 14 specific, one unit development efforts.)</p>
<h3>Sources of capital</h3><p>Projects of 1 to 4 homes are typically funded from households with sufficient wealth to do so. Smaller development projects - from 5 homes up to the institutional thresholds - are typically funded by local and regional developers and investor groups. Larger projects at or above the minimum investment scale thresholds, be they rental or for sale, are those funded by institutional investment (or via public capital (i.e. city taxes, regional bond measures, federal low income housing tax credits, etc.))</p>
<h3>Projection</h3><p>The lighter bars for 2027 and 2028 count only projects already filed and awaiting a permit. They assume household-funded building continues at its recent pace, that between a quarter and 60% of pending mid-sized homes actually manifest into permitted new housing production, that most pending subsidized large projects proceed (60% to 90%), and that few pending market-rate large projects do (none to 25%). Projects not yet filed are not included.</p>
<h3>Limits</h3><p>Affordable-housing inventories lag by one to three years. Grouping by distance can occasionally join deals or split phases. Of about 17,000 projects, around 550 were reviewed individually; the rest follow the rules above. Where this site applies its own rules (grouping permits into projects, subtracting demolitions, tagging subsidy, and projecting 2027 and 2028), those are choices made here and not city figures. Each is described above, and every project can be checked in the project list.</p></section>

<section id="about"><h2>About this housing data visualization project</h2>
<p>Envision Portland Trends began in the summer of 2020 as a project to visualize the city's own housing data, built as applied learning in housing production, city governance and statistics / computer science realms. The effort was funded by Old i, LLC via federal COVID PPP stimulus to create socially helpful learning for Williams College students that also can enable better civic decision making. It is not a study. It is a mirror: the City of Portland's own land use and building permit records, organized so that anyone can see the patterns for themselves. Where the site interprets a pattern, it says so and cites its source.</p></section>
<footer><p>&copy; 2026 Conrad / Old i, LLC. All rights reserved. Data through <span id="asofm">November 2026</span>.</p>
<p>The underlying land use and building permit records are public records from the City of Portland.  The public sources are believed to be reliable, but are provided without warranty.  Note, that corrections are welcomed. The compiled, cleaned and classified data series, integrated with correlated info like public subsidies, along with the visualizations are the proprietary work of Conrad / Old i, LLC.</p>
<p>Please quote or reproduce figures and charts with acknowledgement: “Source: envisionpdxtrends.com / Old i, LLC” and we hope this work is helpful.  Republishing the data series in bulk or using it commercially requires written permission.</p></footer>
</main>
<script>
const D=__DATA__;
const css=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const C={big:css('--s75'),small:css('--s14'),mid:css('--s574'),grey:'#B9B2C2'};
const f=n=>Math.round(n).toLocaleString('en-US'), pct=n=>Math.round(n*100)+'%';
const $=id=>document.getElementById(id);
document.querySelectorAll('.asof').forEach(e=>e.textContent=D.asof);
let T=75, basis='iss';
const YEARS=[];for(let y=2000;y<=2026;y++)YEARS.push(y);
const BANDS=[{a:2008,b:2009,label:'Financial crisis'},{a:2020,b:2020,label:'Pandemic'},{a:2022,b:2023,label:'Rates rise'}];
// project fields: 0 x,1 y,2 year applied,3 year issued,4 gross,5 net,6 subsidy(1 market,2 subsidized),7 expired,8 year completed,9 months from permit application to permit (-1 none),10 within 800 m of MAX
const cls=u=>u<=4?0:(u<T?1:2);
function agg(){const idx=basis=='iss'?3:2;const A={};YEARS.forEach(y=>A[y]={y,c:[0,0,0],net:0,bm:0,bs:0,bmn:0,bsn:0});
  D.p.forEach(p=>{if(p[7])return;const a=A[p[idx]];if(!a)return;const k=cls(p[4]);a.c[k]+=p[4];a.net+=p[5];if(k==2){if(p[6]==2){a.bs+=p[4];a.bsn++}else{a.bm+=p[4];a.bmn++}}});return YEARS.map(y=>A[y])}
function forecast(rows){ // from projects already filed and not yet issued
  const pend=D.p.filter(p=>!p[7]&&p[3]==0&&p[2]>=2023);const s=[0,0,0,0];pend.forEach(p=>{const k=cls(p[4]);if(k==1)s[1]+=p[4];else if(k==2){if(p[6]==2)s[3]+=p[4];else s[2]+=p[4]}});
  const small=(rows[23].c[0]+rows[24].c[0]+rows[25].c[0])/3;const sp=[[2027,.6],[2028,.4]];
  return sp.map(([y,w])=>{const lo=[small*.85,s[1]*.25*w,(s[3]*.6)*w],hi=[small*1.1,s[1]*.6*w,(s[3]*.9+s[2]*.25)*w];const mid=lo.map((v,i)=>(v+hi[i])/2);
    return {y,fc:true,c:mid,lo:lo.reduce((a,b)=>a+b,0),hi:hi.reduce((a,b)=>a+b,0),bm:s[2]*.125*w,bs:s[3]*.75*w,bmlo:0,bmhi:s[2]*.25*w,bslo:s[3]*.6*w,bshi:s[3]*.9*w,pend:s}})}
function legend(id,items){$(id).innerHTML=items.map(i=>`<span><i style="background:${i[1]}${i[2]?';opacity:.4':''}"></i>${i[0]}</span>`).join('')}
function tipOn(el,tip,e,html){tip.innerHTML=html;tip.style.display='block';const b=el.getBoundingClientRect();let x=e.clientX-b.left+14;if(x>b.width-210)x=e.clientX-b.left-210;tip.style.left=x+'px';tip.style.top=(e.clientY-b.top-10)+'px'}
function bands(xOf,bw,m,ih,W){return BANDS.map(b=>{const x0=xOf(b.a),x1=xOf(b.b)+bw;if(x0==null)return '';return `<rect x="${x0}" y="${m.t}" width="${x1-x0}" height="${ih}" fill="var(--band)"/><text class="bandl" x="${(x0+x1)/2}" y="${m.t+11}" text-anchor="middle">${b.label}</text>`}).join('')}
function stacked(el,rows,series,opt={}){
  const W=1040,H=380,m={l:54,r:14,t:18,b:34},iw=W-m.l-m.r,ih=H-m.t-m.b,n=rows.length,bw=iw/n;
  const max=Math.max(...rows.map(r=>Math.max(r.vals.reduce((a,b)=>a+b,0),r.hi||0)));const step=max>6000?2000:max>2500?1000:max>1200?500:250,top=Math.ceil(max/step)*step,y=v=>m.t+ih-(v/top)*ih;
  const xOf=yr=>{const i=rows.findIndex(r=>r.y==yr);return i<0?null:m.l+i*bw};
  let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${opt.label||''}">`;if(opt.bands)s+=bands(xOf,bw,m,ih,W);
  for(let v=0;v<=top;v+=step){s+=`<line class="grid" x1="${m.l}" x2="${W-m.r}" y1="${y(v)}" y2="${y(v)}"/><text class="ax" x="${m.l-8}" y="${y(v)+4}" text-anchor="end">${f(v)}</text>`}
  rows.forEach((r,i)=>{let acc=0;const x=m.l+i*bw+bw*0.16,w=bw*0.68;
    r.vals.forEach((v,j)=>{if(v<=0)return;const y0=y(acc),y1=y(acc+v);acc+=v;const h=Math.max(y0-y1-2,1);s+=`<rect x="${x}" y="${y1}" width="${w}" height="${h}" rx="${r.vals.slice(j+1).every(z=>z<=0)?3:0}" fill="${series[j].color}"${r.fc?' opacity=".38"':(r.partial?' opacity=".6"':'')}/>`});
    if(r.fc&&r.hi!=null){const cx=x+w/2;s+=`<line x1="${cx}" x2="${cx}" y1="${y(r.lo)}" y2="${y(r.hi)}" stroke="var(--ink)" stroke-width="1.5"/><line x1="${cx-5}" x2="${cx+5}" y1="${y(r.hi)}" y2="${y(r.hi)}" stroke="var(--ink)" stroke-width="1.5"/><line x1="${cx-5}" x2="${cx+5}" y1="${y(r.lo)}" y2="${y(r.lo)}" stroke="var(--ink)" stroke-width="1.5"/>`}
    if(i%2==0||n<20)s+=`<text class="ax" x="${m.l+i*bw+bw/2}" y="${H-12}" text-anchor="middle">${r.y}${r.partial?'*':''}</text>`;
    if(opt.mark&&opt.mark(r))s+=`<text class="lab" x="${m.l+i*bw+bw/2}" y="${y(acc)-6}" text-anchor="middle">${opt.mark(r)}</text>`;
    s+=`<rect data-i="${i}" x="${m.l+i*bw}" y="${m.t}" width="${bw}" height="${ih}" fill="transparent"/>`});
  const fi=rows.findIndex(r=>r.fc);if(fi>0){const fx=m.l+fi*bw;s+=`<line x1="${fx}" x2="${fx}" y1="${m.t}" y2="${m.t+ih}" stroke="var(--ink2)" stroke-dasharray="4 4"/><text class="bandl" x="${fx+6}" y="${m.t+11}">Projection</text>`}
  s+=`</svg><div class="tip"></div>`;el.innerHTML=s;const tip=el.querySelector('.tip');
  el.querySelectorAll('rect[data-i]').forEach(rc=>{rc.addEventListener('mousemove',e=>{const r=rows[+rc.dataset.i],tot=r.vals.reduce((a,b)=>a+b,0);tipOn(el,tip,e,`<b>${r.y}${r.fc?' (projection)':(r.partial?' (partial year)':'')}</b><br>`+series.map((sr,j)=>`<i style="display:inline-block;width:9px;height:9px;border-radius:2px;background:${sr.color};margin-right:6px"></i>${sr.name}: <strong>${f(r.vals[j])}</strong>`).join('<br>')+`<br>Total: <strong>${f(tot)}</strong>`+(r.fc&&r.hi!=null?`<br>Range: ${f(r.lo)} to ${f(r.hi)}`:'')+(r.extra?'<br>'+r.extra:''))});rc.addEventListener('mouseleave',()=>tip.style.display='none')})}
function lines(el,years,series,opt={}){
  const W=1040,H=340,m={l:54,r:200,t:18,b:34},iw=W-m.l-m.r,ih=H-m.t-m.b,n=years.length,bw=iw/n;const all=series.flatMap(s=>s.v.filter(v=>v!=null));
  const top=opt.top||Math.ceil(Math.max(...all)/(opt.step||5))*(opt.step||5),step=opt.step||5,y=v=>m.t+ih-(v/top)*ih,x=i=>m.l+i*bw+bw/2;const xOf=yr=>{const i=years.indexOf(yr);return i<0?null:m.l+i*bw};
  let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${opt.label||''}">`;if(opt.bands)s+=bands(xOf,bw,m,ih,W);
  for(let v=0;v<=top+1e-9;v+=step){s+=`<line class="grid" x1="${m.l}" x2="${W-m.r}" y1="${y(v)}" y2="${y(v)}"/><text class="ax" x="${m.l-8}" y="${y(v)+4}" text-anchor="end">${opt.fmt?opt.fmt(v):v}</text>`}
  years.forEach((yr,i)=>{if(i%2==0)s+=`<text class="ax" x="${x(i)}" y="${H-12}" text-anchor="middle">${yr}</text>`});
  const ends=[];series.forEach(sr=>{let d='',pen=false;sr.v.forEach((v,i)=>{if(v==null){pen=false;return}d+=(pen?'L':'M')+x(i)+' '+y(v);pen=true});s+=`<path d="${d}" fill="none" stroke="${sr.color}" stroke-width="2.5" stroke-linejoin="round"/>`;let li=sr.v.length-1;while(li>0&&sr.v[li]==null)li--;s+=`<circle cx="${x(li)}" cy="${y(sr.v[li])}" r="4.5" fill="${sr.color}" stroke="#fff" stroke-width="2"/>`;ends.push({y:y(sr.v[li]),name:sr.name,val:sr.v[li]})});
  ends.sort((a,b)=>a.y-b.y);for(let i=1;i<ends.length;i++)if(ends[i].y-ends[i-1].y<30)ends[i].y=ends[i-1].y+30;
  ends.forEach(e=>{s+=`<text class="lab" x="${W-m.r+10}" y="${e.y-2}">${e.name}</text><text class="ax" x="${W-m.r+10}" y="${e.y+13}">${opt.fmt?opt.fmt(e.val):e.val}</text>`});
  s+=`<line id="xh" y1="${m.t}" y2="${m.t+ih}" stroke="var(--ink2)" stroke-width="1" visibility="hidden"/><rect class="hit" x="${m.l}" y="${m.t}" width="${iw}" height="${ih}" fill="transparent"/></svg><div class="tip"></div>`;el.innerHTML=s;
  const tip=el.querySelector('.tip'),hit=el.querySelector('.hit'),xh=el.querySelector('#xh'),svg=el.querySelector('svg');
  hit.addEventListener('mousemove',e=>{const b=svg.getBoundingClientRect(),px=(e.clientX-b.left)/b.width*W,i=Math.max(0,Math.min(n-1,Math.floor((px-m.l)/bw)));xh.setAttribute('x1',x(i));xh.setAttribute('x2',x(i));xh.setAttribute('visibility','visible');tipOn(el,tip,e,`<b>${years[i]}</b><br>`+series.map(sr=>`<i style="display:inline-block;width:9px;height:9px;border-radius:2px;background:${sr.color};margin-right:6px"></i>${sr.name}: <strong>${sr.v[i]==null?'no data':(opt.fmt?opt.fmt(sr.v[i]):sr.v[i])}</strong>`).join('<br>'))});
  hit.addEventListener('mouseleave',()=>{tip.style.display='none';xh.setAttribute('visibility','hidden')})}
function table(id,head,rows){$(id).innerHTML='<table><thead><tr>'+head.map(h=>`<th>${h}</th>`).join('')+'</tr></thead><tbody>'+rows.map(r=>'<tr>'+r.map((c,i)=>`<td>${i&&typeof c=='number'?f(c):c??''}</td>`).join('')+'</tr>').join('')+'</tbody></table>'}
document.querySelectorAll('.tbtn[data-t]').forEach(b=>b.addEventListener('click',()=>{const t=$(b.dataset.t);t.hidden=!t.hidden;b.textContent=t.hidden?'Show table':'Hide table'}));
// ---- context tiles (independent of threshold)
(function(){const comp=(a,b)=>D.p.filter(p=>p[8]>=a&&p[8]<=b).reduce((s,p)=>s+p[5],0);const P=D.pop;
  const h1=comp(2000,2009),h2=comp(2010,2019),h3=comp(2020,2025),h4=comp(2010,2026);const d1=P.p2010-P.p2000,d2=P.p2020-P.p2010,d3=P.p2025-P.p2020;
  $('chk').textContent=f(h1);
  table('ctx',['Period','Net new homes completed','Change in population','Homes per 100 added residents','Change in households','Homes per added household'],[['2000 to 2010',h1,d1,Math.round(h1/d1*100),P.h2010-P.h2000,(h1/(P.h2010-P.h2000)).toFixed(2)],['2010 to 2020',h2,d2,Math.round(h2/d2*100),'',''],['2020 to 2025',h3,d3,'population fell','',''],['2010 to 2026',h4,'','',P.h2026-P.h2010,(h4/(P.h2026-P.h2010)).toFixed(2)]])})();
// ---- threshold-dependent
function render(){
  $('thrv').textContent=T;const rows=agg(),iss=(basis=='iss')?rows:(()=>{const b=basis;basis='iss';const r=agg();basis=b;return r})();
  const tot=iss.reduce((a,r)=>a+r.c[0]+r.c[1]+r.c[2],0),sh=[0,1,2].map(k=>iss.reduce((a,r)=>a+r.c[k],0)/tot);
  const NM=['Wealthy Households','Local / Regional Wealth','Institutional / Public Capital Allocation'],RG=['1 to 4 units','5 to '+(T-1)+' units',T+' or more units'],CL=[C.small,C.mid,C.big];
  $('who').innerHTML=[0,1,2].map(k=>`<div style="--c:${CL[k]}"><h3>${NM[k]}</h3><b>${pct(sh[k])}</b> of homes since 2000<p>${['Projects typically of '+RG[0]+' via detached homes, accessory dwelling units and small "plexes."','Projects typically of '+RG[1]+'. Smaller apartment and townhouse developments.','Projects typically of '+RG[2]+'. Larger apartment buildings and subdivisions.'][k]}</p></div>`).join('');
  const S1=[0,1,2].map(k=>({name:NM[k]+' ('+RG[k]+')',color:CL[k]}));legend('lg1',S1.map(s=>[s.name,s.color]).concat(basis=='iss'?[['Projection from projects already filed','#777',1]]:[]));
  const fc=forecast(iss);let r1=rows.map(r=>({y:r.y,vals:r.c,partial:r.y==2026}));if(basis=='iss')r1=r1.concat(fc.map(r=>({y:r.y,vals:r.c,fc:true,lo:r.lo,hi:r.hi})));
  $('sub1').textContent=basis=='iss'?'Homes in projects by year the first permit was issued, before demolitions. Lighter bars are a projection based on city\'s land use approval system.':'Homes in projects by year the project applied, before demolitions.';
  stacked($('c1'),r1,S1,{label:'New homes by year and source of capital',bands:true});
  table('t1',['Year',RG[0],RG[1],RG[2],'Total','Net of demolitions'],rows.map(r=>[r.y+(r.y==2026?'*':''),r.c[0],r.c[1],r.c[2],r.c[0]+r.c[1]+r.c[2],r.net]));
  lines($('c1b'),YEARS,[0,1,2].map(k=>({name:['Wealthy Households','Local / Regional','Institutional / Public'][k],color:CL[k],v:iss.map(r=>{const t=r.c[0]+r.c[1]+r.c[2];return t?Math.round(r.c[k]/t*100):null})})),{top:80,step:20,fmt:v=>v+'%',bands:true,label:'Share of homes by source of capital'});
  const era=(a,b,k)=>{const rr=iss.filter(r=>r.y>=a&&r.y<=b),t=rr.reduce((s,r)=>s+r.c[0]+r.c[1]+r.c[2],0);return rr.reduce((s,r)=>s+r.c[k],0)/t};
  $('sharetext').innerHTML=`Housing production mix changes; for example, in 2014 to 2019, larger projects created <strong>${pct(era(2014,2019,2))}</strong> of new homes, while local households created <strong>${pct(era(2014,2019,0))}</strong>. But today, from 2024 to 2026 the institutional share is <strong>${pct(era(2024,2026,2))}</strong>. Thus, households and locals together fund <strong>${pct(era(2024,2026,0)+era(2024,2026,1))}</strong> of a smaller housing production flow. Note how household-funded building is fairly steady through booms and recessions as it is non-market in nature.`;
  const pd=fc[0].pend;$('fcnote').textContent=`Projection: ${f(pd[1])} homes in mid-sized projects, ${f(pd[3])} in subsidized large projects and ${f(pd[2])} in market-rate large projects have applied since 2023 and await a permit. The lighter bars show a middle estimate of how many are permitted in 2027 and 2028, with a range. See Method.`;
  // large
  $('cap2').textContent=`Homes in projects of ${T} or more, by funding`;const S2=[{name:'Market rate',color:C.big},{name:'Subsidized',color:C.small}];legend('lg2',S2.map(s=>[s.name,s.color]));
  stacked($('c2'),iss.map(r=>({y:r.y,vals:[r.bm,r.bs],partial:r.y==2026,extra:`Projects: ${r.bmn} market rate, ${r.bsn} subsidized`})).concat(fc.map(r=>({y:r.y,vals:[r.bm,r.bs],fc:true,lo:r.bmlo+r.bslo,hi:r.bmhi+r.bshi}))),S2,{label:'Large projects by funding',mark:r=>(!r.fc&&r.y==2025&&r.vals[0]==0)?'No market-rate permits':'',bands:true});
  table('t2',['Year','Market rate: homes','Subsidized: homes','Market rate: projects','Subsidized: projects'],iss.map(r=>[r.y+(r.y==2026?'*':''),r.bm,r.bs,r.bmn,r.bsn]));
  let last=null;D.p.forEach(p=>{if(!p[7]&&p[3]&&cls(p[4])==2&&p[6]!=2&&(!last||p[3]>last))last=p[3]});const since=iss.filter(r=>r.y>last),sN=since.reduce((a,r)=>a+r.bsn,0),sU=since.reduce((a,r)=>a+r.bs,0),bm=iss.reduce((a,r)=>a+r.bm,0),bs=iss.reduce((a,r)=>a+r.bs,0);
  $('callout').innerHTML=last>=2026?`Market-rate projects of ${T} or more homes are still reaching permits in 2026 under this definition.`:`<strong>No market-rate project of ${T} or more homes has received a building permit since ${last}.</strong> From ${last+1} through 2026 to date, every project of that size to reach a permit was affordable / income restricted (i.e. subsidized by taxpayers): ${sN} projects with ${f(sU)} homes.`;
  $('callout2').innerHTML=`Since 2000, large market-rate projects supplied ${f(bm)} homes and large subsidized projects ${f(bs)}.`;
  drawMap();drawDist(true);extras();drawSubShare()}
$('thr').addEventListener('input',e=>{T=+e.target.value;render()});
[['b-iss','iss'],['b-st','st']].forEach(([id,key])=>$(id).addEventListener('click',()=>{basis=key;$('b-iss').setAttribute('aria-pressed',key=='iss');$('b-st').setAttribute('aria-pressed',key=='st');render()}));
// ---- map
let mapYear=2017,mapCum=false,timer=null;const cv=$('map'),cx=cv.getContext('2d');
function poly(r,sx,sy){cx.beginPath();r.forEach((p,i)=>{i?cx.lineTo(p[0]*sx,p[1]*sy):cx.moveTo(p[0]*sx,p[1]*sy)});cx.closePath()}
function drawMap(){const W=cv.width,H=cv.height,sx=W/1000,sy=H/1000;cx.clearRect(0,0,W,H);cx.fillStyle='#FAF9FB';cx.fillRect(0,0,W,H);
  cx.fillStyle='#fff';cx.strokeStyle='#9A93A3';cx.lineWidth=2;D.b.forEach(r=>{poly(r,sx,sy);cx.fill();cx.stroke()});
  cx.fillStyle='#D5E3EC';D.w.forEach(r=>{poly(r,sx,sy);cx.fill()});
  const line=(ps,col,w,dash)=>{cx.strokeStyle=col;cx.lineWidth=w;cx.lineJoin='round';cx.lineCap=dash?'butt':'round';cx.setLineDash(dash||[]);ps.forEach(p=>{cx.beginPath();p.forEach((q,i)=>{i?cx.lineTo(q[0]*sx,q[1]*sy):cx.moveTo(q[0]*sx,q[1]*sy)});cx.stroke()})};line(D.mx,'#fff',7);line(D.mx,'#0B5D1E',4,[5,6]);line(D.fw,'#fff',7);line(D.fw,'#111',3.5);cx.setLineDash([]);
  const CL=[C.small,C.mid,C.big];const pts=D.p.filter(p=>!p[7]&&p[3]&&p[0]>=0&&(mapCum?p[3]<=mapYear:p[3]==mapYear)).sort((a,b)=>b[4]-a[4]);const n=[0,0,0];
  pts.forEach(p=>{const k=cls(p[4]);n[k]+=p[4];const r=Math.max(2.2,Math.sqrt(p[4])*1.7);cx.beginPath();cx.arc(p[0]*sx,p[1]*sy,r,0,6.2832);cx.globalAlpha=mapCum&&p[3]<mapYear?0.28:0.8;cx.fillStyle=CL[k];cx.fill();cx.globalAlpha=1;if(r>5){cx.strokeStyle='#fff';cx.lineWidth=1.5;cx.stroke()}});
  $('yrv').textContent=mapYear;$('yr').value=mapYear;
  $('maptext').textContent=(mapCum?`Through ${mapYear}: `:`${mapYear}: `)+`${f(n[0])} homes from household wealth, ${f(n[1])} from local and regional capital, ${f(n[2])} from institutional and public capital. Dots are placed at the project's permit address. Outline: Portland city limits; blue: rivers; black: interstates and US 26; dotted dark green: MAX light rail as it runs today.`}
legend('lg4',[['Wealthy Households',C.small],['Local / Regional Wealth',C.mid],['Institutional / Public Capital Allocation',C.big]]);$('lg4').innerHTML+='<span><i style="background:#111;height:4px;width:22px;vertical-align:3px"></i>I-5, I-84, I-205, I-405 and US 26 west</span><span><i style="background:repeating-linear-gradient(90deg,#0B5D1E 0 4px,transparent 4px 8px);height:4px;width:24px;vertical-align:3px;border-radius:0"></i>MAX light rail</span>';
$('yr').addEventListener('input',e=>{mapYear=+e.target.value;drawMap()});
[['m-year',false],['m-cum',true]].forEach(([id,v])=>$(id).addEventListener('click',()=>{mapCum=v;$('m-year').setAttribute('aria-pressed',!v);$('m-cum').setAttribute('aria-pressed',v);drawMap()}));
$('play').addEventListener('click',()=>{if(timer){clearInterval(timer);timer=null;$('play').textContent='Play';return}$('play').textContent='Pause';if(mapYear>=2026)mapYear=1999;timer=setInterval(()=>{mapYear++;drawMap();if(mapYear>=2026){clearInterval(timer);timer=null;$('play').textContent='Play'}},700)});
// ---- distribution of permit waits, by year and project size (follows the threshold)
let dYear=2025,dTimer=null,dA=null,dS=null,dCur=null,dRaf=0;const NB=16,BINW=2,REFY=[2007,2016,2022]; // 2-month bins; the last holds 30+. REFY: years whose medians are drawn as dashed reference lines
function distData(){const A={};YEARS.forEach(y=>A[y]={h:[0,1,2].map(()=>Array(NB).fill(0)),v:[[],[],[]]});
  D.p.forEach(p=>{if(p[9]<0||!A[p[3]])return;const k=cls(p[4]);A[p[3]].h[k][Math.min(NB-1,Math.floor(p[9]/BINW))]++;A[p[3]].v[k].push(p[9])});
  const med=a=>{if(!a.length)return null;a.sort((x,y)=>x-y);const m=a.length>>1;return a.length%2?a[m]:(a[m-1]+a[m])/2};
  YEARS.forEach(y=>{A[y].med=A[y].v.map(med);A[y].n=A[y].v.map(a=>a.length)});return A}
function drawDist(rebuild){const el=$('c6');
  const W=1040,m={l:54,r:14},iw=W-m.l-m.r,bw=iw/NB,PH=118,HD=30,GAP=14,T0=6,H=T0+3*(HD+PH)+2*GAP+46;
  const NM=['Wealthy Households','Local / Regional Wealth','Institutional / Public Capital Allocation'],RG=['1 to 4 units','5 to '+(T-1)+' units',T+' or more units'],CL=[C.small,C.mid,C.big];
  const py=k=>T0+k*(HD+PH+GAP)+HD, xm=v=>m.l+Math.min(v,BINW*(NB-1)+BINW/2)/BINW*bw;
  if(rebuild||!dS){dA=distData();
    const tops=[0,1,2].map(k=>{const mx=Math.max(...YEARS.map(y=>dA[y].n[k]?Math.max(...dA[y].h[k])/dA[y].n[k]:0));const st=mx>.6?.25:mx>.3?.2:.1;return {top:Math.min(1,Math.ceil(mx/st-1e-9)*st),st}});
    let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Share of projects by months waited for a building permit, by project size, for the selected year">`;
    [0,1,2].forEach(k=>{const y0=py(k),tp=tops[k];
      s+=`<rect x="${m.l}" y="${y0-HD+9}" width="12" height="12" rx="2" fill="${CL[k]}"/><text class="lab" x="${m.l+19}" y="${y0-HD+20}" style="font-size:14px">${NM[k]} (${RG[k]})</text><text class="ax" id="ds${k}" x="${W-m.r}" y="${y0-HD+20}" text-anchor="end" style="font-size:13px"></text>`;
      for(let v=0;v<=tp.top+1e-9;v+=tp.st){const yy=y0+PH-(v/tp.top)*PH;s+=`<line class="grid" x1="${m.l}" x2="${W-m.r}" y1="${yy}" y2="${yy}"/><text class="ax" x="${m.l-8}" y="${yy+4}" text-anchor="end">${Math.round(v*100)}%</text>`}
      for(let i=0;i<NB;i++)s+=`<rect id="db${k}_${i}" x="${m.l+i*bw+1}" width="${bw-2}" y="${y0+PH}" height="0" rx="3" fill="${CL[k]}"/>`;
      REFY.forEach((ry,j)=>{s+=`<line id="dr${k}_${j}" y1="${y0}" y2="${y0+PH}" stroke="var(--ink2)" stroke-width="1.5" stroke-dasharray="4 4"/><text class="bandl" id="drl${k}_${j}" y="${y0+26+j*13}">${ry}</text>`});
      s+=`<line id="dm${k}" y1="${y0-4}" y2="${y0+PH}" stroke="var(--ink)" stroke-width="2.5"/><text class="lab" id="dml${k}" y="${y0+11}"></text>`;
      s+=`<line x1="${m.l}" x2="${W-m.r}" y1="${y0+PH}" y2="${y0+PH}" stroke="var(--ink2)"/>`;
      for(let i=0;i<NB;i++)s+=`<rect data-k="${k}" data-i="${i}" x="${m.l+i*bw}" y="${y0}" width="${bw}" height="${PH}" fill="transparent"/>`});
    const ay=py(2)+PH;for(let v=0;v<=24;v+=6)s+=`<text class="ax" x="${m.l+v/BINW*bw}" y="${ay+17}" text-anchor="middle">${v}</text>`;
    s+=`<text class="ax" x="${m.l+(NB-.5)*bw}" y="${ay+17}" text-anchor="middle">30+</text><text class="ax" x="${m.l+iw/2}" y="${ay+38}" text-anchor="middle">Months from permit application to permit issued</text>`;
    s+=`<text id="dyv" x="${W-m.r}" y="${py(0)+52}" text-anchor="end" style="font:700 44px var(--display);fill:var(--ink)"></text></svg><div class="tip"></div>`;
    el.innerHTML=s;dS={tops};dCur=null;const tip=el.querySelector('.tip');
    el.querySelectorAll('rect[data-k]').forEach(rc=>{rc.addEventListener('mousemove',e=>{const k=+rc.dataset.k,i=+rc.dataset.i,a=dA[dYear],c=a.h[k][i];tipOn(el,tip,e,`<b>${dYear}: ${i==NB-1?'30 months or more':i*BINW+' to '+(i+1)*BINW+' months'}</b><br><i style="display:inline-block;width:9px;height:9px;border-radius:2px;background:${CL[k]};margin-right:6px"></i>${NM[k]}: <strong>${f(c)}</strong> project${c==1?'':'s'}`+(a.n[k]?` (${pct(c/a.n[k])})`:'')+(a.med[k]!=null?`<br>Median wait: <strong>${a.med[k].toFixed(1)} months</strong>`:''))});rc.addEventListener('mouseleave',()=>tip.style.display='none')})}
  const a=dA[dYear],tgt={h:a.h.map((r,k)=>r.map(c=>a.n[k]?c/a.n[k]/dS.tops[k].top*PH:0)),med:a.med.map(v=>v==null?null:xm(v))};
  $('dyv').textContent=dYear+(dYear==2026?'*':'');$('dyr').value=dYear;
  [0,1,2].forEach(k=>{$('ds'+k).textContent=a.n[k]?`${f(a.n[k])} project${a.n[k]==1?'':'s'} · median ${a.med[k].toFixed(1)} months`:'No permits issued';
    REFY.forEach((ry,j)=>{const mv=dA[ry].med[k],rx=mv==null||dYear==ry?null:xm(mv),ln=$('dr'+k+'_'+j),lb=$('drl'+k+'_'+j);[ln,lb].forEach(e=>e.setAttribute('visibility',rx==null?'hidden':'visible'));if(rx!=null){ln.setAttribute('x1',rx);ln.setAttribute('x2',rx);lb.setAttribute('x',rx+5);lb.setAttribute('text-anchor','start')}})});
  const put=st=>{[0,1,2].forEach(k=>{const y0=py(k);st.h[k].forEach((h,i)=>{const b=$('db'+k+'_'+i);b.setAttribute('y',y0+PH-h);b.setAttribute('height',Math.max(h,0))});
    const ln=$('dm'+k),lb=$('dml'+k),x=st.med[k];ln.setAttribute('visibility',x==null?'hidden':'visible');lb.setAttribute('visibility',x==null?'hidden':'visible');if(x!=null){ln.setAttribute('x1',x);ln.setAttribute('x2',x);const right=x<W-m.r-150;lb.setAttribute('x',right?x+6:x-6);lb.setAttribute('text-anchor',right?'start':'end');lb.textContent='Median '+dYear}})};
  cancelAnimationFrame(dRaf);const from=dCur,still=matchMedia('(prefers-reduced-motion:reduce)').matches;
  if(!from||still){dCur=tgt;put(tgt)}else{const t0=performance.now(),D0=450;const step=now=>{const u=Math.min(1,(now-t0)/D0),e=u<.5?2*u*u:1-Math.pow(-2*u+2,2)/2;
      const st={h:tgt.h.map((r,k)=>r.map((v,i)=>from.h[k][i]+(v-from.h[k][i])*e)),med:tgt.med.map((v,k)=>v==null?null:(from.med[k]==null?v:from.med[k]+(v-from.med[k])*e))};put(st);dCur=st;if(u<1)dRaf=requestAnimationFrame(step);else dCur=tgt};dRaf=requestAnimationFrame(step)}
  const RL=i=>i==NB-1?'30 or more':i*BINW+' to '+(i+1)*BINW;
  table('t6',['Months waited ('+dYear+')',RG[0],RG[1],RG[2]],Array.from({length:NB},(_,i)=>[RL(i),a.h[0][i],a.h[1][i],a.h[2][i]]).concat([['All projects',a.n[0],a.n[1],a.n[2]],['Median months',...a.med.map(v=>v==null?'':v.toFixed(1))]]))}
$('dyr').addEventListener('input',e=>{dYear=+e.target.value;drawDist()});
$('dplay').addEventListener('click',()=>{if(dTimer){clearInterval(dTimer);dTimer=null;$('dplay').textContent='Play';return}$('dplay').textContent='Pause';if(dYear>=2026)dYear=1999;dTimer=setInterval(()=>{dYear++;drawDist();if(dYear>=2026){clearInterval(dTimer);dTimer=null;$('dplay').textContent='Play'}},900)});
// ---- the rush to file before the 1 Feb 2017 inclusionary housing rule (fixed 20-home threshold)
drawWaits();
(function(){const Z=D.iz;if(!Z)return;const n=Z.lu.length,y0=Z.start[0],mi=(y,m)=>(y-y0)*12+m-1,MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],ml=i=>MN[i%12]+' '+(y0+Math.floor(i/12));
  const W=1040,m={l:54,r:14},iw=W-m.l-m.r,bw=iw/n,PH=150,HD=28,GAP=14,T0=4,NP=2,H=T0+NP*(HD+PH)+(NP-1)*GAP+30,cut=mi(2017,2),w0=mi(2016,1);
  const PN=[{t:'Land use applications filed (design and historic review)',d:Z.lu.map(r=>[r[0],r[1]]),s:['Went on to a building permit','Never reached a building permit'],c:[C.mid,C.grey],u:'application',k:Z.lu.map(r=>r[2])},
            {t:'Building permits issued',d:Z.iss.map(r=>[r[0],0]),s:['Homes permitted'],c:[C.big],u:'project',k:Z.iss.map(r=>r[1])}];
  legend('lg7',[['Land use application went on to a building permit',C.mid],['Never reached a building permit',C.grey],['Building permits issued',C.big]]);
  let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Monthly homes in land use applications filed and in building permits issued, projects of 20 or more homes, 2011 to 2019">`;
  PN.forEach((p,k)=>{const py=T0+k*(HD+PH+GAP)+HD,mx=Math.max(...p.d.map(r=>r[0]+r[1])),st=mx>1500?500:mx>800?250:mx>400?200:100,top=Math.ceil(mx/st)*st,yy=v=>py+PH-(v/top)*PH;
    s+=`<rect x="${m.l+w0*bw}" y="${py}" width="${(cut-w0)*bw}" height="${PH}" fill="var(--band)"/>`+(k==0?`<text class="bandl" x="${m.l+(w0+cut)/2*bw}" y="${py+11}" text-anchor="middle">2016 to Jan 2017</text>`:'');
    s+=`<text class="lab" x="${m.l}" y="${py-9}" style="font-size:14px">${p.t}</text>`;
    for(let v=0;v<=top;v+=st)s+=`<line class="grid" x1="${m.l}" x2="${W-m.r}" y1="${yy(v)}" y2="${yy(v)}"/><text class="ax" x="${m.l-8}" y="${yy(v)+4}" text-anchor="end">${f(v)}</text>`;
    p.d.forEach((r,i)=>{let acc=0;r.forEach((v,j)=>{if(v<=0)return;const a=yy(acc),b=yy(acc+v);acc+=v;s+=`<rect x="${m.l+i*bw+.75}" y="${b}" width="${bw-1.5}" height="${Math.max(a-b-(j?1:0),1)}" rx="1.5" fill="${p.c[j]}"/>`})});
    s+=`<line x1="${m.l}" x2="${W-m.r}" y1="${py+PH}" y2="${py+PH}" stroke="var(--ink2)"/><line x1="${m.l+cut*bw}" x2="${m.l+cut*bw}" y1="${py-4}" y2="${py+PH}" stroke="var(--ink)" stroke-width="2"/>`+(k==0?`<text class="lab" x="${m.l+cut*bw+7}" y="${py+11}">Rule takes effect, Feb 1, 2017</text>`:'');
    for(let i=0;i<n;i++)s+=`<rect data-k="${k}" data-i="${i}" x="${m.l+i*bw}" y="${py}" width="${bw}" height="${PH}" fill="transparent"/>`});
  // interpretation overlay: the vesting rush, the stall, and where each shows up in permits about a year later
  {const RED='#B3261E',X=i=>m.l+i*bw,pA=T0+HD,pB=T0+(HD+PH+GAP)+HD,bt=pA+20,bb=pA+PH+9,e2=cut+12,lag=13,ye=pB+PH*.5;
   const halo='paint-order:stroke;stroke:#fff;stroke-width:4px;stroke-linejoin:round',tx=(x,y,t,sz)=>`<text x="${x}" y="${y}" style="font:500 ${sz||14}px var(--body);fill:${RED};${halo}">${t}</text>`;
   s+=`<g pointer-events="none"><defs><marker id="izah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 1L9 5L0 9z" fill="${RED}"/></marker></defs>`;
   [[w0,cut-.25],[cut+.25,e2]].forEach(([a,b])=>{s+=`<rect x="${X(a)}" y="${bt}" width="${X(b)-X(a)}" height="${bb-bt}" fill="none" stroke="${RED}" stroke-width="1.5" stroke-dasharray="6 4"/>`});
   [[w0,w0+lag],[cut,cut+lag],[e2,e2+lag]].forEach(([a,b])=>{s+=`<line x1="${X(a)}" y1="${bb}" x2="${X(b)}" y2="${ye}" stroke="${RED}" stroke-width="1.5" stroke-dasharray="6 4" marker-end="url(#izah)"/>`});
   s+=tx(X(w0)+5,pA+PH*.5,'Pre-IH vesting')+tx(X(cut)+18,pA+PH*.5,'Post-IH stall');
   s+=['~ similar','production','flows'].map((t,i)=>tx(X(cut)+7,pB+14+i*15,t,13)).join('')+['lower production','period'].map((t,i)=>tx(X(cut+12.5),pB+14+i*15,t,13)).join('')+'</g>'}
  const ay=T0+NP*(HD+PH)+(NP-1)*GAP;for(let i=0;i<n;i+=12)s+=`<line x1="${m.l+i*bw}" x2="${m.l+i*bw}" y1="${ay}" y2="${ay+5}" stroke="var(--ink2)"/><text class="ax" x="${m.l+(i+6)*bw}" y="${ay+18}" text-anchor="middle">${y0+i/12}</text>`;
  s+=`</svg><div class="tip"></div>`;const el=$('c7');el.innerHTML=s;const tip=el.querySelector('.tip');
  el.querySelectorAll('rect[data-k]').forEach(rc=>{rc.addEventListener('mousemove',e=>{const p=PN[+rc.dataset.k],i=+rc.dataset.i,r=p.d[i];tipOn(el,tip,e,`<b>${ml(i)}</b><br>`+p.s.map((nm,j)=>`<i style="display:inline-block;width:9px;height:9px;border-radius:2px;background:${p.c[j]};margin-right:6px"></i>${nm}: <strong>${f(r[j])}</strong> homes`).join('<br>')+`<br>${p.k[i]} ${p.u}${p.k[i]==1?'':'s'}`)});rc.addEventListener('mouseleave',()=>tip.style.display='none')});
  table('t7',['Month','Land use applications filed','Homes in them','of which never reached a permit','Building permits issued: homes'],Z.lu.map((r,i)=>[ml(i),r[2],r[0]+r[1],r[1],Z.iss[i][0]]));
  // project-level failure to build: the pre-rule window against the 2011 to 2019 cycle
  const agg=(a,b,skip)=>{let c=0,ok=0,h=0,hn=0;for(let i=a;i<b;i++){if(skip&&i>=skip[0]&&i<skip[1])continue;const r=Z.lu[i];c+=r[2];ok+=r[3];h+=r[0]+r[1];hn+=r[1]}return {c,fail:c-ok,h,hn}};
  const cyc=agg(0,n),win=agg(w0,cut),rest=agg(0,n,[w0,cut]);
  table('rushtab',['Land use applications filed in','Projects','Never reached a building permit','Failure-to-build rate','Homes proposed','Homes never permitted','Share of homes never permitted'],[['January 2016 to January 2017, before the rule',win],['The rest of 2011 to 2019',rest],['All of 2011 to 2019',cyc]].map(([nm,r])=>[nm,r.c,r.fail,pct(r.fail/r.c),r.h,r.hn,pct(r.hn/r.h)]));
  const yr=(A,y,g)=>A.slice(mi(y,1),mi(y,1)+12).reduce((t,r)=>t+g(r),0),ys=[2014,2015,2016,2017,2018,2019],iy=ys.map(y=>yr(Z.iss,y,r=>r[0])),ly=ys.map(y=>yr(Z.lu,y,r=>r[0]+r[1]));
  const ru=agg(mi(2016,12),cut),base=agg(mi(2013,1),mi(2016,1)),a1=agg(cut,mi(2018,2));
  {const pk=Z.iss.slice(mi(2014,1),mi(2018,1)).reduce((t,r)=>t+r[0],0)/48,af=Z.iss.slice(mi(2018,2),n).reduce((t,r)=>t+r[0],0)/(n-mi(2018,2));$('izgap').textContent=pct(1-af/pk)} // permits per month after the stall (Feb 2018 on) against the 2014 to 2017 pace
  $('rushtext').innerHTML=`In December 2016 and January 2017, developers filed <strong>${ru.c} land use applications for ${f(ru.h)} homes</strong>, about ${Math.round((ru.c/2)/(base.c/36))} times the monthly pace of 2013 to 2015. In the twelve months after the rule took effect, ${a1.c} were filed. Building permits did not follow that surge and stall: from 2014 through 2019, homes permitted ranged from ${f(Math.min(...iy))} to ${f(Math.max(...iy))} a year, while homes in land use applications ranged from ${f(Math.min(...ly))} to ${f(Math.max(...ly))}. That pattern is consistent with housing economics. In the short run, builders, lenders and trades cannot expand quickly, so supply responds less to demand than it does over the long run, and the cost of creating each home rises when activity rises (<a href="https://doi.org/10.1086/261560">Topel and Rosen, "Housing Investment in the United States," 1988</a>). Operations science describes the same behavior: as a production system nears its capacity, waits and costs climb steeply (Hopp and Spearman, <i>Factory Physics</i>). Price is what smooths the flow, and projects at the margin of feasibility no longer pencil. The option did not pay out for many who bought it: <strong>${win.fail} of the ${win.c} projects that filed from January 2016 through January 2017 (${pct(win.fail/win.c)}) never reached a building permit</strong>, against ${pct(rest.fail/rest.c)} for the rest of the 2011 to 2019 cycle.`})();
// ---- figures that back the charts: volume by period, subsidized share, transit proximity, land use waits
function extras(){const live=D.p.filter(p=>!p[7]&&p[3]),sum=(a,b,g)=>live.filter(p=>p[3]>=a&&p[3]<=b&&(!g||g(p))).reduce((t,p)=>t+p[4],0);
  const per=(a,b)=>f(Math.round(sum(a,b)/(b-a+1)));
  $('voltext').innerHTML=`Homes permitted per year, all sizes: <strong>${per(2000,2009)}</strong> in 2000 to 2009, <strong>${per(2010,2019)}</strong> in 2010 to 2019, <strong>${per(2020,2023)}</strong> in 2020 to 2023 and <strong>${per(2024,2026)}</strong> in 2024 to 2026, with 2026 to date.`;
  const sh=(a,b)=>pct(sum(a,b,p=>p[6]==2)/sum(a,b));
  $('subshare').innerHTML=`Across projects of every size, subsidized homes were <strong>${sh(2010,2019)}</strong> of homes permitted in 2010 to 2019 and <strong>${sh(2024,2026)}</strong> in 2024 to 2026.`;
  const nr=[0,1,2].map(k=>{const d=live.filter(p=>cls(p[4])==k&&p[0]>=0);return d.filter(p=>p[10]).reduce((t,p)=>t+p[4],0)/d.reduce((t,p)=>t+p[4],0)});
  $('todtext').innerHTML=`Since 2000, <strong>${pct(nr[2])}</strong> of homes in projects of ${T} or more units were permitted within 800 meters (about half a mile) of a MAX light rail line as it runs today, compared with ${pct(nr[1])} for projects of 5 to ${T-1} units and ${pct(nr[0])} for projects of 1 to 4 units.`;
  const W=D.luw;if(W){const m=v=>v==null?'':v.toFixed(1)+' months';
    table('luwtab',['Projects of 75 or more homes with a land use review','Permitted 2010 to 2019','Permitted since March 2020'],[['Land use filing to building permit (median)',m(W.before.med),m(W.since.med)],['Middle half of projects',W.before.q1.toFixed(0)+' to '+W.before.q3.toFixed(0)+' months',W.since.q1.toFixed(0)+' to '+W.since.q3.toFixed(0)+' months'],['Land use review itself (median)',m(W.before.rev),m(W.since.rev)],['Land use approval to building permit (median)',m(W.before.ap),m(W.since.ap)],['Building permit application to issue (median)',m(W.before.bp),m(W.since.bp)],['Projects',W.before.n,W.since.n]]);
    $('luwtext').innerHTML=`Since March 2020 the median wait from land use filing to building permit is <strong>${W.since.med.toFixed(1)} months</strong>, against ${W.before.med.toFixed(1)} in 2010 to 2019. The two kinds of funding differ sharply: ${W.sub.med.toFixed(1)} months for subsidized projects (${W.sub.n} projects) and ${W.mkt.med.toFixed(1)} months for market-rate projects (${W.mkt.n} projects). Several of those market-rate projects held a land use approval for years before applying for a building permit, so that wait is not all city processing time.`}}
// ---- land use filing to permit, project by project (fixed 75 homes), and subsidized share by year
function drawWaits(){const W=D.luw;if(!W||!W.pts)return;const el=$('c8'),P=W.pts,CL={1:C.big,2:C.small},NM={1:'Market rate',2:'Subsidized'};
  const PER=[[2003,2007],[2008,2012],[2013,2016],[2017,2019],[2020,2023],[2024,2026]],y0=2003,y1=2026,ny=y1-y0+1;
  const Wd=1040,H=420,m={l:54,r:14,t:16,b:52},iw=Wd-m.l-m.r,ih=H-m.t-m.b,bw=iw/ny,top=96,yy=v=>m.t+ih-(Math.min(v,top)/top)*ih,xl=y=>m.l+(y-y0)*bw;
  const med=a=>{if(!a.length)return null;const b=[...a].sort((p,q)=>p-q),k=b.length>>1;return b.length%2?b[k]:(b[k-1]+b[k])/2},qt=(a,q)=>{const b=[...a].sort((p,r)=>p-r),i=(b.length-1)*q,lo=Math.floor(i);return b[lo]+(b[Math.min(lo+1,b.length-1)]-b[lo])*(i-lo)};
  legend('lg8',[['Market rate',C.big],['Subsidized',C.small],['Middle half of all projects in the period','#D9D4DE']]);
  let s=`<svg viewBox="0 0 ${Wd} ${H}" role="img" aria-label="Months from land use filing to building permit for each large project, by year permitted and funding">`;const rows=[];
  PER.forEach(([a,b],i)=>{const d=P.filter(p=>p[0]>=a&&p[0]<=b),x0=xl(a)+3,x1=xl(b+1)-3,all=d.map(p=>p[1]);
    if(d.length>=4){const q1=qt(all,.25),q3=qt(all,.75);s+=`<rect x="${x0}" y="${yy(q3)}" width="${x1-x0}" height="${yy(q1)-yy(q3)}" fill="#D9D4DE" opacity=".55" rx="3"/>`}
    s+=`<text class="ax" x="${(x0+x1)/2}" y="${H-10}" text-anchor="middle">${a} to ${b} (${d.length})</text>`+(i?`<line x1="${xl(a)}" x2="${xl(a)}" y1="${m.t}" y2="${m.t+ih+26}" stroke="var(--rule)"/>`:'');
    const row=[a+' to '+b,d.length,d.length?med(all).toFixed(1):'',d.length>=4?qt(all,.25).toFixed(0)+' to '+qt(all,.75).toFixed(0):''];[1,2].forEach(k=>{const v=d.filter(p=>p[2]==k).map(p=>p[1]);row.push(v.length,v.length?med(v).toFixed(1):'')});rows.push(row)});
  for(let v=0;v<=top;v+=12)s+=`<line class="grid" x1="${m.l}" x2="${Wd-m.r}" y1="${yy(v)}" y2="${yy(v)}"/><text class="ax" x="${m.l-8}" y="${yy(v)+4}" text-anchor="end">${v}</text>`;
  s+=`<text class="ax" x="${m.l-40}" y="${m.t+4}" text-anchor="start" style="font-size:11px"></text>`;
  for(let y=y0;y<=y1;y++)s+=`<text class="ax" x="${xl(y)+bw/2}" y="${m.t+ih+17}" text-anchor="middle">${String(y).slice(2)}</text>`;
  const cnt={};P.forEach((p,i)=>{if(p[0]<y0)return;const j=cnt[p[0]]=(cnt[p[0]]||0)+1,off=((j%5)-2)*bw*.16;s+=`<circle data-i="${i}" cx="${xl(p[0])+bw/2+off}" cy="${yy(p[1])}" r="5.5" fill="${CL[p[2]]}" stroke="#fff" stroke-width="2"/>`});
  PER.forEach(([a,b])=>{const x0=xl(a)+3,x1=xl(b+1)-3;[1,2].forEach(k=>{const v=P.filter(p=>p[0]>=a&&p[0]<=b&&p[2]==k).map(p=>p[1]);if(v.length<3)return;const mv=med(v);s+=`<line x1="${x0}" x2="${x1}" y1="${yy(mv)}" y2="${yy(mv)}" stroke="#fff" stroke-width="6"/><line x1="${x0}" x2="${x1}" y1="${yy(mv)}" y2="${yy(mv)}" stroke="${CL[k]}" stroke-width="3"/><text class="lab" x="${k==1?x1-4:x0+4}" y="${yy(mv)+(k==1?-7:17)}" text-anchor="${k==1?'end':'start'}" style="paint-order:stroke;stroke:#fff;stroke-width:4px">${mv.toFixed(0)} mo</text>`})});
  s+=`<line x1="${m.l}" x2="${Wd-m.r}" y1="${m.t+ih}" y2="${m.t+ih}" stroke="var(--ink2)"/><text class="ax" x="${m.l}" y="${m.t-3}">Months</text></svg><div class="tip"></div>`;el.innerHTML=s;const tip=el.querySelector('.tip');
  el.querySelectorAll('circle[data-i]').forEach(c=>{const p=P[+c.dataset.i];c.addEventListener('mousemove',e=>tipOn(el,tip,e,`<b>Permitted ${p[0]}</b><br><i style="display:inline-block;width:9px;height:9px;border-radius:50%;background:${CL[p[2]]};margin-right:6px"></i>${NM[p[2]]}, ${f(p[3])} homes<br>Land use filing to permit: <strong>${p[1].toFixed(1)} months</strong>`));c.addEventListener('mouseleave',()=>tip.style.display='none')});
  table('t8',['Permitted in','Projects','Median months, all','Middle half, months','Market-rate projects','Market-rate median','Subsidized projects','Subsidized median'],rows)}
function drawSubShare(){const el=$('c9'),live=D.p.filter(p=>!p[7]&&p[3]),tot={},sub={};live.forEach(p=>{tot[p[3]]=(tot[p[3]]||0)+p[4];if(p[6]==2)sub[p[3]]=(sub[p[3]]||0)+p[4]});
  const sh=YEARS.map(y=>tot[y]?(sub[y]||0)/tot[y]:0),PER=[[2000,2009],[2010,2019],[2020,2023],[2024,2026]];
  const W=1040,H=320,m={l:54,r:14,t:18,b:34},iw=W-m.l-m.r,ih=H-m.t-m.b,n=YEARS.length,bw=iw/n,top=.5,yy=v=>m.t+ih-(Math.min(v,top)/top)*ih,xOf=yr=>{const i=YEARS.indexOf(yr);return i<0?null:m.l+i*bw};
  let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Subsidized homes as a share of all homes permitted, by year">`+bands(xOf,bw,m,ih,W);
  for(let v=0;v<=top+1e-9;v+=.1)s+=`<line class="grid" x1="${m.l}" x2="${W-m.r}" y1="${yy(v)}" y2="${yy(v)}"/><text class="ax" x="${m.l-8}" y="${yy(v)+4}" text-anchor="end">${Math.round(v*100)}%</text>`;
  YEARS.forEach((y,i)=>{const h=yy(0)-yy(sh[i]);s+=`<rect x="${m.l+i*bw+2}" y="${yy(sh[i])}" width="${bw-4}" height="${Math.max(h,0)}" rx="3" fill="${C.small}"/>`+(i%2==0?`<text class="ax" x="${m.l+i*bw+bw/2}" y="${H-12}" text-anchor="middle">${y}${y==2026?'*':''}</text>`:'')});
  const rows=YEARS.map((y,i)=>[String(y),sub[y]||0,tot[y]||0,pct(sh[i])]);
  PER.forEach(([a,b])=>{const t=YEARS.filter(y=>y>=a&&y<=b).reduce((q,y)=>q+(tot[y]||0),0),u=YEARS.filter(y=>y>=a&&y<=b).reduce((q,y)=>q+(sub[y]||0),0),v=u/t,x0=xOf(a)+2,x1=xOf(b)+bw-2;
    s+=`<line x1="${x0}" x2="${x1}" y1="${yy(v)}" y2="${yy(v)}" stroke="#fff" stroke-width="6"/><line x1="${x0}" x2="${x1}" y1="${yy(v)}" y2="${yy(v)}" stroke="var(--ink)" stroke-width="2.5"/><text class="lab" x="${(x0+x1)/2}" y="${yy(v)-8}" text-anchor="middle" style="paint-order:stroke;stroke:#fff;stroke-width:4px">${a} to ${b}: ${pct(v)}</text>`;rows.push([a+' to '+b,u,t,pct(v)])});
  s+=`<line x1="${m.l}" x2="${W-m.r}" y1="${yy(0)}" y2="${yy(0)}" stroke="var(--ink2)"/>`;YEARS.forEach((y,i)=>{s+=`<rect data-i="${i}" x="${m.l+i*bw}" y="${m.t}" width="${bw}" height="${ih}" fill="transparent"/>`});
  s+=`</svg><div class="tip"></div>`;el.innerHTML=s;const tip=el.querySelector('.tip');
  el.querySelectorAll('rect[data-i]').forEach(r=>{const i=+r.dataset.i,y=YEARS[i];r.addEventListener('mousemove',e=>tipOn(el,tip,e,`<b>${y}</b><br>Subsidized: <strong>${pct(sh[i])}</strong> of homes permitted<br>${f(sub[y]||0)} of ${f(tot[y]||0)} homes`));r.addEventListener('mouseleave',()=>tip.style.display='none')});
  table('t9',['Year or period','Subsidized homes','All homes permitted','Subsidized share'],rows)}
$('asofm').textContent=D.asof.replace(/ \d+,/,''); // footer date follows the data: "November 10, 2026" -> "November 2026"
// ---- approvals and duration (independent of threshold)
(function(){const L=D.lu,yrs=[];for(let y=2002;y<=2026;y++)yrs.push(y);const by={};L.forEach(r=>by[r.y]=r);
  const S3=[{name:'Went on to a building permit',color:C.mid},{name:'No permit issued so far',color:C.grey}];legend('lg3',S3.map(s=>[s.name,s.color]));
  stacked($('c3'),yrs.map(y=>{const r=by[y]||{units:0,perm:0,cases:0,cp:0,mo:null};return {y,vals:[r.perm,r.units-r.perm],partial:y>=2024,extra:`${r.cp} of ${r.cases} approvals permitted`+(y<2010?'<br>Provisional':'')}}),S3,{label:'Homes approved and share reaching a permit',bands:true});
  table('t3',['Decision year','Homes approved','Reached a permit','Approvals','Approvals permitted'],L.map(r=>[r.y+(r.y>=2024?'*':(r.y<2010?' (provisional)':'')),r.units,r.perm,r.cases,r.cp]));
  const E=[['2002 to 2004','Approved well before the financial crisis',2002,2004],['2005 to 2007','Approved in the run-up to the financial crisis',2005,2007],['2008 to 2009','Approved during the financial crisis',2008,2009],['2010 to 2016','Recovery and expansion',2010,2016],['2017 to 2019','Approved in the run-up to the pandemic',2017,2019],['2020 to 2021','Approved during the pandemic',2020,2021],['2022 to 2023','Approved as interest rates rose',2022,2023]];
  const er=E.map(e=>{const rr=L.filter(r=>r.y>=e[2]&&r.y<=e[3]),u=rr.reduce((a,r)=>a+r.units,0),p=rr.reduce((a,r)=>a+r.perm,0);return [e[0],e[1],u,p,u-p,pct(p/u)]});
  table('eras',['Decisions made','Period','Homes approved','Reached a permit','Lost or stalled','Share reaching a permit'],er);
  $('lutext').innerHTML=`Each downturn leaves a gap. Approvals that do proceed typically take about 10 months to reach a permit and roughly two more years to build, so today's approvals point to homes about three years out.`;
  const dy=[];for(let y=2000;y<=2026;y++)dy.push(y);const dm={};D.dur.forEach(r=>dm[r.y]=r.m);
  const S5=[{name:'Application to permit',color:C.big,v:dy.map(y=>dm[y]??null)},{name:'Land use decision to permit',color:C.mid,v:dy.map(y=>by[y]&&by[y].mo!=null&&by[y].cp>=4?by[y].mo:null)}];legend('lg5',S5.map(s=>[s.name+(s.name[0]=='A'?' (projects of 5+ homes, by year issued)':' (by year of decision)'),s.color]));
  lines($('c5'),dy,S5,{step:5,fmt:v=>v+' mo',bands:true,label:'Months to reach a building permit'});
  table('t5',['Year','Permit application to permit, median months','Land use decision to permit, median months'],dy.map(y=>[y,dm[y]??'',by[y]&&by[y].mo!=null&&by[y].cp>=4?by[y].mo:'']));
  $('durtext').innerHTML=`For projects of five or more homes, the median time from applying for a building permit to receiving it was <strong>${dm[2000]} months in 2000</strong>, about ${dm[2010]} in 2010 and <strong>${dm[2025]} months in 2025</strong>. It has stayed near ${Math.round((dm[2021]+dm[2022]+dm[2023]+dm[2024]+dm[2025])/5)} months since 2021.`})();
render();
if(innerWidth<=700)document.querySelectorAll('.chart:not(.keepleft)').forEach(c=>c.scrollLeft=c.scrollWidth);
</script></body></html>'''
open(os.path.join(HERE,'..','index.html'),'w').write(html.replace('__DATA__',D)); print('index.html written',len(html))
import runpy; runpy.run_path(os.path.join(HERE,'build_projects_page.py'))
