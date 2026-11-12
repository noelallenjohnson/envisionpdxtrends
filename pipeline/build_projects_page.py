"""Envision Portland Trends: the project list page (projects.html).
A searchable, sortable table of every project the site counts. Rebuilt with each refresh."""
import os, json, csv
HERE = os.path.dirname(os.path.abspath(__file__))
rows = []
OUT = {'Completed': 0, 'Issued': 1, 'In review': 2, 'Expired': 3}
num = lambda v: int(float(v)) if v not in ('', None) else 0
import re
def nice(t):
    t = (t or '').title()
    t = re.sub(r"'S\b", "'s", t)
    t = re.sub(r'\b(Nw|Ne|Sw|Se)\b', lambda m: m.group(1).upper(), t)
    return re.sub(r'(\d)(St|Nd|Rd|Th)\b', lambda m: m.group(1) + m.group(2).lower(), t)
from datetime import datetime
def day(v):
    return datetime.strptime(v[:10], '%Y-%m-%d') if v else None
with open(os.path.join(HERE, 'out', 'projects.csv'), newline='') as f:
    for r in csv.DictReader(f):
        fund = 1 if r['SUBSIDY'] == 'Market rate' else (2 if r['SUBSIDY'] == 'Subsidized' else 0)
        oc = next(v for k, v in OUT.items() if r['OUTCOME'].startswith(k))
        seen, appr, iss = day(r['LAND_USE_FIRST_SEEN']), day(r['LAND_USE_APPROVED']), day(r['FIRST_ISSUED'])
        mo = round((iss - seen).days / 365.25, 1) if seen and iss and iss >= seen else 0  # in years  # land use case first seen -> first building permit issued
        rows.append([nice(r['PROJECT_ADDRESS']), nice(r['NEIGHBORHOOD']), num(r['YEAR_FIRST_SET_UP']), num(r['YEAR_FIRST_ISSUED']),
                     num(r['GROSS_NEW_UNITS']), num(r['DEMOLISHED_UNITS']), num(r['NET_NEW_UNITS']), fund, oc, r['FIRST_APPLICATION'], num(r['PERMITS']), appr.year if appr else 0, mo])
asof = json.load(open(os.path.join(HERE, 'out', 'summary.json')))['asof']
html = r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Project list | Envision Portland Trends</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@400;600;700&family=Libre+Franklin:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{--purple:#500082;--gold:#FFBE0A;--ink:#111;--ink2:#555;--rule:#E4E0E8;--wash:#F6F3F8;--page:#fff;--s75:#7A2FB5;--s14:#A86F00;--s574:#00909A;--display:"Zilla Slab",Rockwell,Georgia,serif;--body:"Libre Franklin","Helvetica Neue",Arial,sans-serif;color-scheme:light}
*{box-sizing:border-box} body{margin:0;background:var(--page);color:var(--ink);font:400 16px/1.55 var(--body)}
a{color:var(--purple)} a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
header.top{border-bottom:3px solid var(--purple)} .bar{max-width:1180px;margin:0 auto;padding:12px 20px} .bar a{font:500 14px var(--body);text-decoration:none} .bar a:hover{text-decoration:underline}
main{max-width:1180px;margin:0 auto;padding:0 20px 70px}
.eyebrow{font:600 13px var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--purple);margin-top:40px}
h1{font:700 clamp(30px,4.6vw,48px)/1.08 var(--display);margin:8px 0 10px} p{max-width:74ch;margin:0 0 12px} .note{font-size:14px;color:var(--ink2)}
.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px 14px;background:var(--wash);border-left:6px solid var(--purple);padding:14px 16px;margin:20px 0 10px}
.filters label{display:grid;gap:4px;font:600 13px var(--body)} .filters .wide{grid-column:span 2}
input,select{font:400 15px var(--body);padding:7px 9px;border:1px solid #B9B2C2;border-radius:4px;background:#fff;color:var(--ink);width:100%}
.yrs{display:flex;gap:6px;align-items:center} .yrs span{font-weight:400}
.sum{font:600 16px var(--body);margin:14px 0 6px} .sum b{font:700 20px var(--display);font-variant-numeric:tabular-nums}
.tw{overflow-x:auto;border-top:3px solid var(--ink)} table{border-collapse:collapse;width:100%;min-width:900px;font-size:14px;font-variant-numeric:tabular-nums}
th,td{padding:7px 10px;border-bottom:1px solid var(--rule);text-align:left;vertical-align:top} td.n,th.n{text-align:right}
th{font-weight:600;border-bottom:2px solid var(--ink);white-space:nowrap;background:#fff;position:sticky;top:0}
th button{font:inherit;font-weight:600;background:none;border:0;padding:0;cursor:pointer;color:var(--ink)} th button:hover{color:var(--purple)} th[aria-sort] button{color:var(--purple)}
tbody tr:hover{background:var(--wash)} .dot{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px} .sub{color:var(--ink2);font-size:13px}
.pg{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:14px 0} .pg button{font:500 14px var(--body);padding:6px 14px;border:1px solid var(--purple);border-radius:4px;background:#fff;color:var(--purple);cursor:pointer} .pg button:disabled{border-color:var(--rule);color:#aaa;cursor:default}
footer{border-top:3px solid var(--purple);margin-top:40px;padding:20px 0;font-size:14px;color:var(--ink2)}
@media (max-width:700px){.filters .wide{grid-column:auto}}
</style></head><body>
<header class="top"><div class="bar"><a href="./">&larr; Back to Envision Portland Trends</a></div></header>
<main>
<div class="eyebrow">Housing creation in Portland, Oregon &middot; 2000 to 2026</div>
<h1>Project list</h1>
<p>Every project counted on this site, from City of Portland building permit records through __ASOF__. Search by address, neighborhood or permit number, narrow the list with the filters, and select a column heading to sort.</p>
<div class="filters">
<label class="wide">Search<input id="q" type="search" placeholder="Address, neighborhood or permit number" autocomplete="off"></label>
<label>Project size<select id="fs"><option value="">All sizes</option><option value="0">1 to 4 homes</option><option value="1">5 to 74 homes</option><option value="2">75 or more homes</option></select></label>
<label>Funding<select id="ff"><option value="">All</option><option value="1">Market rate</option><option value="2">Subsidized</option><option value="0">Not tagged (1 to 4 homes)</option></select></label>
<label>Status<select id="fo"><option value="">All</option><option value="0">Completed</option><option value="1">Permit issued</option><option value="2">In review</option><option value="3">Expired or cancelled</option></select></label>
<label>Year applied<span class="yrs"><input id="y0" type="number" min="2000" max="2026" value="2000" aria-label="From year"><span>to</span><input id="y1" type="number" min="2000" max="2026" value="2026" aria-label="To year"></span></label>
</div>
<div class="sum" id="sum" aria-live="polite"></div>
<div class="tw"><table><thead><tr id="hd"></tr></thead><tbody id="tb"></tbody></table></div>
<div class="pg"><button id="prev" type="button">Previous</button><span id="pos"></span><button id="next" type="button">Next</button></div>
<p class="note">One row is one project: building permits filed within 40 meters and 270 days of each other are grouped. New homes are the homes the project adds; net new is new homes minus homes demolished on the same site. LU approved is the year the city approved the project's land use review. Approval Time is the number of years, to the nearest tenth, from the day the city first received that land use application to the day the first building permit was issued. Both are shown for projects that went through a design or historic review that could be matched to the project; they are blank for projects that needed no such review, and for land divisions. Funding is tagged for projects of five or more homes: subsidized means state, local bond or federal tax-credit money, or university housing, and a market-rate project with required inclusionary units counts as market rate. The permit number is the first permit in the project and can be looked up on PortlandMaps. Expired or cancelled projects are listed but are not counted in the site's totals of permitted homes.</p>
<footer>&copy; 2026 Old i, LLC &middot; Data through __ASOF__ &middot; Source: City of Portland permit records via PortlandMaps</footer>
</main>
<script>
const R=__ROWS__;
const $=i=>document.getElementById(i),f=n=>n.toLocaleString('en-US');
const SZ=['1 to 4','5 to 74','75 or more'],SC=['var(--s14)','var(--s574)','var(--s75)'],FU=['','Market rate','Subsidized'],OC=['Completed','Permit issued','In review','Expired or cancelled'];
const size=r=>r[4]<=4?0:r[4]<=74?1:2;
const COLS=[['Address',r=>r[0],0],['Neighborhood',r=>r[1],0],['LU approved',r=>r[11],1],['Permit issued',r=>r[3],1],['Size class',r=>size(r),0],['New homes',r=>r[4],1],['Approval Time',r=>r[12],1],['Net new',r=>r[6],1],['Funding',r=>r[7],0],['Status',r=>r[8],0],['First permit',r=>r[9],0]];
let sortC=5,sortD=-1,page=0,view=[];const PER=50;
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function head(){$('hd').innerHTML=COLS.map((c,i)=>`<th class="${c[2]?'n':''}" ${i==sortC?`aria-sort="${sortD>0?'ascending':'descending'}"`:''}><button type="button" data-i="${i}">${c[0]}${i==sortC?(sortD>0?' ▲':' ▼'):''}</button></th>`).join('')}
function apply(){
  const q=$('q').value.trim().toLowerCase(),fs=$('fs').value,ff=$('ff').value,fo=$('fo').value,y0=+$('y0').value||2000,y1=+$('y1').value||2026;
  view=R.filter(r=>(!q||(r[0]+' '+r[1]+' '+r[9]).toLowerCase().includes(q))&&(fs===''||size(r)==fs)&&(ff===''||r[7]==ff)&&(fo===''||r[8]==fo)&&r[2]>=y0&&r[2]<=y1);
  const g=COLS[sortC][1];view.sort((a,b)=>{const x=g(a),y=g(b);return (x<y?-1:x>y?1:0)*sortD||b[4]-a[4]});
  page=0;draw()}
function draw(){
  const n=view.length,pages=Math.max(1,Math.ceil(n/PER));page=Math.min(page,pages-1);
  const gross=view.reduce((s,r)=>s+r[4],0),net=view.reduce((s,r)=>s+r[6],0);
  $('sum').innerHTML=n?`<b>${f(n)}</b> project${n==1?'':'s'} &middot; <b>${f(gross)}</b> new homes &middot; <b>${f(net)}</b> net new`:'No projects match. Try a shorter search or clear a filter.';
  $('tb').innerHTML=view.slice(page*PER,page*PER+PER).map(r=>{const s=size(r);return `<tr><td>${esc(r[0])||'<span class="sub">No address on permit</span>'}${r[10]>1?`<div class="sub">${r[10]} permits</div>`:''}</td><td>${esc(r[1])}</td><td class="n">${r[11]||''}</td><td class="n">${r[3]||'<span class="sub">none</span>'}</td><td><i class="dot" style="background:${SC[s]}"></i>${SZ[s]}</td><td class="n">${f(r[4])}</td><td class="n">${r[12]?r[12].toFixed(1)+' yr':''}</td><td class="n">${f(r[6])}</td><td>${FU[r[7]]}</td><td>${OC[r[8]]}</td><td>${esc(r[9])}</td></tr>`}).join('');
  $('pos').textContent=n?`Page ${page+1} of ${f(pages)}`:'';$('prev').disabled=page==0;$('next').disabled=page>=pages-1;head()}
$('hd').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;const i=+b.dataset.i;if(i==sortC)sortD=-sortD;else{sortC=i;sortD=COLS[i][2]?-1:1}apply()});
['q','fs','ff','fo','y0','y1'].forEach(i=>$(i).addEventListener('input',apply));
$('prev').onclick=()=>{page--;draw();scrollTo(0,$('sum').offsetTop-10)};$('next').onclick=()=>{page++;draw();scrollTo(0,$('sum').offsetTop-10)};
apply();
</script></body></html>'''
html = html.replace('__ROWS__', json.dumps(rows, separators=(',', ':'))).replace('__ASOF__', asof)
open(os.path.join(HERE, '..', 'projects.html'), 'w').write(html)
print('projects.html written', len(rows), 'projects', len(html))
