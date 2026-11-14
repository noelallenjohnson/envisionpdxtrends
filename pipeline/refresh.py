"""Envision Portland Trends: data refresh.

Pulls City of Portland permit records, applies the reviewed rules, and writes
the site data file. Run:  python pipeline/refresh.py            (live pull)
                          python pipeline/refresh.py --cache DIR (reuse bp.json, demo.json, lu.json in DIR)

Rules (agreed in the November 2026 review):
  * Units: new construction, conversions of non-residential buildings and units added inside
    existing buildings count. Remodels, hotels, replacements and moves do not.
  * Projects: permits within 40 m and 270 days are one project (two 5+ unit permits only if same tax lot).
  * Net new: gross units minus homes demolished on the same site.
  * Subsidy (5+ units): subsidized means state, local bond or tax-credit money, or university housing.
    Inclusionary housing alone is market rate. No evidence means market rate.
  * frozen/reviewed_projects.csv holds every individually reviewed call and always wins.
"""
import argparse, datetime, json, os, re, sys, time
import numpy as np, pandas as pd, requests
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
FROZEN = os.path.join(HERE, 'frozen')
OUT = os.path.join(HERE, 'out')
FEED = 'https://www.portlandmaps.com/arcgis/rest/services/Public/BDS_Permit/MapServer/22/query'
DEAD = ['Expired', 'Cancelled', 'Void', 'Withdrawn']
APPROVED = ['Approved', 'Recorded', 'Decision Rendered', 'Appeal Decision Rendered', 'City Approved', 'LUBA Decision Rendered']
XY = lambda lo, la: ((lo + 122.68) * np.cos(np.radians(45.52)) * 111320, (la - 45.52) * 110574)


# ---------------------------------------------------------------- pull
def pull(where, label):
    out, off = [], 0
    while True:
        p = dict(where=where, outFields='*', returnGeometry='true', outSR=4326, f='json',
                 orderByFields='OBJECTID', resultOffset=off, resultRecordCount=2000)
        j = None
        for attempt in range(8):
            try:
                j = requests.post(FEED, data=p, timeout=180).json()
                if 'error' not in j:
                    break
            except Exception as e:  # network hiccup: wait and retry
                j = {'error': str(e)}
            time.sleep(5 + attempt * 5)
        if j is None or 'error' in j:
            sys.exit(f'City feed failed for {label}: {j}')
        fs = j.get('features', [])
        for f in fs:
            a = f['attributes']; g = f.get('geometry') or {}
            a['LONGITUDE'] = g.get('x'); a['LATITUDE'] = g.get('y'); out.append(a)
        off += len(fs)
        if len(fs) < 2000 and not j.get('exceededTransferLimit'):
            break
    print(label, len(out), flush=True)
    return out


def get_raw(cache):
    q = {'bp': "NUMNEWUNITS>0 AND PERMIT IN ('Residential 1 & 2 Family Permit','Commercial Building Permit','Major Project Groups','Manufactured Home on Indiv. Lot Permit','Manufactured Home in Park Permit','Site Development Permit')",
         'demo': "WORK_DESCRIPTION LIKE '%Demol%' OR PERMIT LIKE '%Demo%'",
         'lu': "PERMIT='Land Use Review'"}
    raw = {}
    for k, where in q.items():
        f = os.path.join(cache, k + '.json') if cache else None
        if f and os.path.exists(f):
            raw[k] = json.load(open(f))
        else:
            raw[k] = pull(where, k)
            if f:
                json.dump(raw[k], open(f, 'w'))
    return raw


def load(rows):
    d = pd.DataFrame(rows)
    for c in ['ISSUED', 'FINALED', 'INTAKECOMPLETEDATE', 'CREATEDATE']:
        d[c] = pd.to_datetime(d[c], unit='ms', utc=True).dt.tz_convert('America/Los_Angeles').dt.tz_localize(None)
    d['ADDR'] = (d.HOUSE.fillna('').astype(str).str.strip() + ' ' + d.DIRECTION.fillna('').str.strip() + ' ' + d.PROPSTREET.fillna('').str.strip() + ' ' + d.STREETTYPE.fillna('').str.strip()).str.replace(r'\s+', ' ', regex=True).str.strip()
    d['DESC'] = d.DESCRIPTION.fillna('').str.replace(r'\s+', ' ', regex=True)
    d['X'], d['Y'] = XY(d.LONGITUDE, d.LATITUDE)
    return d


# ---------------------------------------------------------------- 1. what each permit does to the housing count
CREATE = re.compile(r'\bADU\b|ACCESSORY DWELLING|CONVER|CHANGE OF OCCUPANCY|CHANGE OCCUPANCY|LEGALIZ|\bCREAT\w* .{0,60}(UNIT|DWELLING|APARTMENT|DUPLEX|TRIPLEX|FOURPLEX|RESIDENCE)|NEW .{0,25}(DWELLING UNIT|LIVING UNIT|APARTMENT|RESIDENTIAL UNIT)|ADD\w* .{0,40}(DWELLING UNIT|LIVING UNIT|APARTMENT|UNITS?\b)|\bDUPLEX|TRIPLEX|FOURPLEX|4-PLEX|TWO[- ]FAMILY|SECOND (DWELLING|UNIT)|ADDITIONAL (DWELLING|UNIT)|\d+ (NEW )?(RESIDENTIAL |DWELLING |APARTMENT |LIVING )UNITS?|\bSRO\b|LIVE[/-]WORK|TO (APARTMENT|RESIDENTIAL|HOUSING)')
NONRES = re.compile(r'(OFFICE|HOTEL|MOTEL|COMMERCIAL|RETAIL|WAREHOUSE|CHURCH|SCHOOL|\bB OCC|\bR-1\b|\bM OCC|STORAGE|RESTAURANT|BANK|INDUSTRIAL|NURSING|CLINIC|HOSPITAL|DORM)')
RESTYPE = ['Single Family Dwelling', 'Apartments/Condos (3 or more units)', 'Accessory Dwelling Unit', 'Townhouse (3 or more units)', 'Duplex/Two Family Dwelling', 'Rowhouse (2 units)', 'Rowhouse (3 or more units)', 'Townhouse (2 Units)', 'Floating Home', 'Special Residential', 'Row House', 'Residential', 'Garage/Carport', 'Accessory Structure']
COUNT = ['New construction', 'Conversion of non-residential building to housing', 'New unit created within/added to existing building', 'New construction in non-residential permit type - check', 'Manufactured home placed in park']


def event(w, t, permit, u):
    if w == 'New Construction':
        if t in ('Hotel/Motel',): return 'Not housing (hotel/motel)'
        if t not in RESTYPE: return 'New construction in non-residential permit type - check'
        return 'New construction'
    if w in ('Alteration', 'Addition'):
        if CREATE.search(u):
            if permit == 'Commercial Building Permit' and NONRES.search(u) and re.search(r'CONVER|CHANGE OF OCC|CHANGE OCC|TO (APARTMENT|RESIDENTIAL|HOUSING)', u): return 'Conversion of non-residential building to housing'
            return 'New unit created within/added to existing building'
        return 'Remodel of existing unit - no new housing'
    if w in ('Replacement', 'Move', 'Repair Fire Damage'): return 'Replacement or move - no net new'
    if w == 'First': return 'Manufactured home placed in park'
    return 'Other - check'


def dunits(t, d):
    t = t or ''
    if t in ('Single Family Dwelling', 'Accessory Dwelling Unit', 'Floating Home', 'Row House'): return 1
    if 'Duplex' in t or '2 units' in t.lower() or '2 Units' in t: return 2
    if t.startswith(('Apartments', 'Townhouse (3', 'Rowhouse (3', 'Special Residential', 'Residential')) or re.search(r'APARTMENT|DWELLING|RESIDEN|HOUSE\b|TRIPLEX|FOURPLEX|PLEX', d.upper()):
        if t in ('Accessory Structure', 'Garage/Carport'): return 0
        m = re.search(r'(\d{1,3})[- ]?(UNIT|PLEX|APARTMENT|DWELLING)', d.upper())
        if m: return int(m.group(1))
        if 'TRIPLEX' in d.upper(): return 3
        if 'FOURPLEX' in d.upper(): return 4
        if t.startswith(('Apartments', 'Townhouse (3', 'Rowhouse (3')): return np.nan
        if re.search(r'\b(SFR|SINGLE FAMILY|HOUSE|RESIDENCE|DWELLING)\b', d.upper()) and not re.search(r'GARAGE ONLY|SHED|CARPORT ONLY', d.upper()): return 1 if t not in ('Accessory Structure', 'Garage/Carport') and not NONRES.search(t.upper()) else 0
    return 0


def build_projects(bp, demo_rows):
    U = bp.DESC.str.upper()
    bp['UNIT_EVENT'] = [event(w, t, p, u) for w, t, p, u in zip(bp.WORK_DESCRIPTION, bp.TYPE, bp.PERMIT, U)]
    bp['GROSS_NEW_UNITS'] = np.where(bp.UNIT_EVENT.isin(COUNT), bp.NUMNEWUNITS, 0)
    dead = bp.STATUS.isin(DEAD)
    # ---- 2. group permits into projects
    c = bp[(bp.GROSS_NEW_UNITS > 0) & bp.X.notna()].copy(); idx = c.index.to_numpy()
    tree = cKDTree(c[['X', 'Y']].to_numpy()); pairs = tree.query_pairs(40.0, output_type='ndarray')
    t = c.CREATEDATE.to_numpy().astype('datetime64[D]').astype(int); u_ = c.GROSS_NEW_UNITS.to_numpy(); lot = c.STATEIDKEY.fillna('').str.replace(' ', '').to_numpy()
    ok = (np.abs(t[pairs[:, 0]] - t[pairs[:, 1]]) <= 270) & ~((u_[pairs[:, 0]] >= 5) & (u_[pairs[:, 1]] >= 5) & (lot[pairs[:, 0]] != lot[pairs[:, 1]]))
    par = np.arange(len(c))
    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    for a, b in pairs[ok]:
        ra, rb = find(a), find(b)
        if ra != rb: par[rb] = ra
    root = np.array([find(i) for i in range(len(c))])
    bp['PG'] = -1; bp.loc[idx, 'PG'] = root
    nog = bp.PG == -1; bp.loc[nog, 'PG'] = -np.arange(2, nog.sum() + 2)
    g = bp[bp.GROSS_NEW_UNITS > 0].sort_values('CREATEDATE').groupby('PG')
    first = g.first()
    proj = pd.DataFrame({'FIRST_APPLICATION': first.APPLICATION, 'PROJECT_ADDRESS': first.ADDR, 'PERMITS': g.size(), 'GROSS_NEW_UNITS': g.GROSS_NEW_UNITS.sum(),
                         'FIRST_SET_UP': g.CREATEDATE.min(), 'FIRST_ISSUED': g.ISSUED.min(), 'LAST_FINAL': g.FINALED.max(),
                         'PERMITS_ISSUED': g.ISSUED.count(), 'PERMITS_FINAL': g.FINALED.count(),
                         'TYPES': g.TYPE.agg(lambda s: '; '.join(f'{k} x{v}' for k, v in s.value_counts().items())),
                         'UNIT_EVENTS': g.UNIT_EVENT.agg(lambda s: '; '.join(sorted(set(s)))),
                         'NEIGHBORHOOD': first.NEIGHBORHOOD, 'LATITUDE': g.LATITUDE.mean(), 'LONGITUDE': g.LONGITUDE.mean(), 'X': g.X.mean(), 'Y': g.Y.mean(), 'DESC': first.DESC})
    proj = proj.sort_values('FIRST_SET_UP'); proj['PROJECT_ID'] = ['P%05d' % i for i in range(1, len(proj) + 1)]
    bp['PROJECT_ID'] = bp.PG.map(proj.PROJECT_ID)
    proj['ALL_DEAD'] = bp[bp.GROSS_NEW_UNITS > 0].assign(d=dead).groupby('PG').d.all()
    # ---- 3. demolitions -> net new
    dm = load(demo_rows)
    dm = dm[dm.PERMIT.isin(['Residential 1 & 2 Family Permit', 'Commercial Building Permit', 'Major Project Groups']) & ~dm.STATUS.isin(DEAD + ['Application'])].copy()
    dm['DEMO_UNITS'] = [dunits(t, d) for t, d in zip(dm.TYPE, dm.DESC)]
    dr = dm[(dm.DEMO_UNITS != 0) & dm.X.notna()].copy()
    cp = bp[(bp.GROSS_NEW_UNITS > 0) & bp.X.notna()]; ct = cKDTree(cp[['X', 'Y']].to_numpy()); cpid = cp.PROJECT_ID.to_numpy(); clot = cp.STATEIDKEY.fillna('').str.replace(' ', '').to_numpy()
    cx = cp.X.to_numpy(); cy = cp.Y.to_numpy()
    psetup = proj.set_index('PROJECT_ID').FIRST_SET_UP
    assign = []
    for x, y, d, lt in zip(dr.X, dr.Y, dr.CREATEDATE, dr.STATEIDKEY.fillna('').str.replace(' ', '')):
        best = None
        for j in ct.query_ball_point([x, y], 30.0):
            dd = (psetup[cpid[j]] - d).days
            if -730 <= dd <= 1825:
                sc = (0 if clot[j] == lt and lt else 1, abs(dd), np.hypot(cx[j] - x, cy[j] - y))
                if best is None or sc < best[0]: best = (sc, cpid[j])
        assign.append(best[1] if best else None)
    dr['PROJECT_ID'] = assign
    ds = dr[dr.PROJECT_ID.notna()].groupby('PROJECT_ID').agg(DEMOLISHED_UNITS=('DEMO_UNITS', lambda s: s.fillna(0).sum()))
    proj = proj.merge(ds, left_on='PROJECT_ID', right_index=True, how='left'); proj['DEMOLISHED_UNITS'] = proj.DEMOLISHED_UNITS.fillna(0)
    proj['OUTCOME'] = np.select([proj.ALL_DEAD, proj.PERMITS_FINAL == proj.PERMITS, proj.PERMITS_ISSUED > 0], ['Expired or cancelled - never realized', 'Completed (all permits final)', 'Issued / under construction'], 'In review - not yet issued')
    return bp, proj


# ---------------------------------------------------------------- 4. subsidy records at the site
def match_subsidy(bp, proj):
    ref = pd.read_csv(os.path.join(FROZEN, 'subsidy_records.csv'))
    ref['X'], ref['Y'] = XY(ref.LON, ref.LAT); ref['HN'] = ref.ADDR.fillna('').str.extract(r'^\s*(\d+)')[0]
    rt = cKDTree(ref[['X', 'Y']].to_numpy())
    big = proj[(proj.GROSS_NEW_UNITS >= 5) & proj.X.notna()]
    pts = bp[(bp.GROSS_NEW_UNITS > 0) & bp.X.notna()].groupby('PROJECT_ID')[['X', 'Y']].apply(lambda d: d.to_numpy())
    rows = []
    for r in big.itertuples():
        hn = re.match(r'\d+', r.PROJECT_ADDRESS or ''); hn = hn.group(0) if hn else None
        cand = {}
        for (x, y) in pts[r.PROJECT_ID][:60]:
            for j in rt.query_ball_point([x, y], 90.0):
                d = np.hypot(ref.X[j] - x, ref.Y[j] - y); cand[j] = min(cand.get(j, 1e9), d)
        best = None
        for j, d in cand.items():
            q = ref.loc[j]; yr = r.FIRST_SET_UP.year
            if pd.notna(q.YEAR) and not (yr - 2 <= q.YEAR <= yr + 9): continue
            ur = (q.UNITS / r.GROSS_NEW_UNITS) if pd.notna(q.UNITS) and q.UNITS > 0 else np.nan
            same_hn = hn is not None and q.HN == hn
            if not (same_hn or d <= 40 or (pd.notna(ur) and 0.75 <= ur <= 1.33)): continue
            sc = (0 if same_hn else 1, 0 if (pd.notna(ur) and 0.75 <= ur <= 1.33) else 1, d)
            if best is None or sc < best[0]: best = (sc, j)
        if best:
            q = ref.loc[best[1]]
            rows.append(dict(PROJECT_ID=r.PROJECT_ID, MATCH_NAME=q.NAME, MATCH_TOTAL_UNITS=q.UNITS, MATCH_REGULATED_UNITS=q.REG))
    mt = pd.DataFrame(rows, columns=['PROJECT_ID', 'MATCH_NAME', 'MATCH_TOTAL_UNITS', 'MATCH_REGULATED_UNITS'])
    return proj.merge(mt, on='PROJECT_ID', how='left')


S2 = re.compile(r'SUPPORTIVE HOUSING|PERMANENT SUPPORTIVE|LOW[- ]INCOME|HOME FORWARD|TAX CREDIT|LIHTC|REGULATED AFFORDABLE|100% (OF THE UNITS )?(WILL BE )?AFFORDABLE|INCOME[- ]RESTRICTED|HOUSING AUTHORITY|TRANSITIONAL HOUSING|PUBLIC HOUSING|HABITAT FOR HUMANITY|CENTRAL CITY CONCERN|REACH (CDC|COMMUNITY)|HACIENDA|INNOVATIVE HOUSING|NORTHWEST HOUSING ALTERNATIVES|CATHOLIC CHARITIES|BRIDGE HOUSING|PROUD GROUND|\bPCRI\b|OUR JUST FUTURE|HUMAN SOLUTIONS|COMMUNITY PARTNERS FOR AFFORDABLE|SELF ENHANCEMENT|METRO (HOUSING )?BOND|AFFORDABLE (APARTMENT|SENIOR|FAMILY)|ALL AFFORDABLE|ALL (OF THE )?UNITS (WILL BE |ARE )?(AFFORDABLE|OFFERED AT)|\d+% (OF )?(AREA |AVERAGE )?(MEDIAN|AMI|MFI)|DORM|RESIDENCE HALL|STUDENT HOUSING')


def baseline(bp, proj):
    # townhouse permits that each carry the whole project count ("1 of 9" showing 9 units): one unit per permit
    m = bp.DESC.str.upper().str.extract(r'\b(\d{1,3})\s+OF\s+(\d{1,3})\b'); B = pd.to_numeric(m[1])
    fix = (bp.GROSS_NEW_UNITS > 2) & (B == bp.GROSS_NEW_UNITS) & bp.APPLICATION.str.endswith('RS')
    bp['U'] = np.where(fix, 1, bp.GROSS_NEW_UNITS)
    for r in pd.read_csv(os.path.join(FROZEN, 'unit_overrides.csv')).itertuples():
        bp.loc[bp.APPLICATION == r.APPLICATION, 'U'] = r.UNITS
    proj['GROSS'] = proj.PROJECT_ID.map(bp.groupby('PROJECT_ID').U.sum())
    share = proj.MATCH_REGULATED_UNITS / proj.MATCH_TOTAL_UNITS
    txt = bp[bp.GROSS_NEW_UNITS > 0].groupby('PROJECT_ID').DESC.agg(lambda s: bool(S2.search(' '.join(s).upper())))
    proj['TXT'] = proj.PROJECT_ID.map(txt).fillna(False).astype(bool)
    rec = proj.MATCH_NAME.notna() & ~(share < 0.5)
    proj['SUBSIDY'] = np.select([proj.GROSS < 5, rec, proj.TXT], ['Not applicable (1-4 units)', 'Subsidized', 'Subsidized'], 'Market rate')
    proj['SUBSIDY_BASIS'] = np.select([proj.GROSS < 5, rec, proj.TXT, proj.MATCH_NAME.notna()], ['', 'Affordable-housing record at the site', 'Permit text names subsidy, sponsor or student housing', 'Record has under half its units regulated: inclusionary, market rate'], 'No subsidy evidence found')
    proj['NET'] = proj.GROSS - proj.DEMOLISHED_UNITS
    proj['DEVELOPER'] = ''; proj['REVIEW_STATUS'] = 'Rule-based, not individually reviewed'
    # reviewed calls always win; a reviewed call follows its permit into whichever project now holds it
    rv = pd.read_csv(os.path.join(FROZEN, 'reviewed_projects.csv'))
    app2pid = dict(zip(bp.APPLICATION, bp.PROJECT_ID)); pos = {p: i for i, p in zip(proj.index, proj.PROJECT_ID)}
    missing = 0
    for r in rv.itertuples():
        i = pos.get(app2pid.get(r.FIRST_APPLICATION))
        if i is None:
            missing += 1; continue
        proj.at[i, 'SUBSIDY'] = r.SUBSIDY; proj.at[i, 'SUBSIDY_BASIS'] = r.SUBSIDY_BASIS if isinstance(r.SUBSIDY_BASIS, str) else ''
        proj.at[i, 'DEVELOPER'] = r.DEVELOPER if isinstance(r.DEVELOPER, str) else ''; proj.at[i, 'REVIEW_STATUS'] = r.REVIEW_STATUS
        if pd.notna(r.NET_NEW_OVERRIDE): proj.at[i, 'NET'] = r.NET_NEW_OVERRIDE
    print('reviewed calls applied:', len(rv) - missing, 'not found in feed:', missing)
    proj['CLASS'] = np.select([proj.GROSS <= 4, proj.GROSS <= 74], ['1-4 units: local household wealth', '5-74 units: local/regional developer'], '75+ units: institutional scale')
    proj = proj[proj.GROSS > 0].copy()
    proj['YEAR'] = proj.FIRST_SET_UP.dt.year; proj['YEAR_ISSUED'] = proj.FIRST_ISSUED.dt.year
    return proj


# ---------------------------------------------------------------- 5. land use approvals -> permits
W = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12}
P1 = re.compile(r'(\d{1,4}|' + '|'.join(W) + r')[\s-]*(?:new |residential |dwelling |affordable |market[- ]rate |apartment |housing |living |studio |total |rental |condo(?:minium)? |townho\w+ |micro[- ]?|sro |attached |senior |student |loft )*(units?|dwellings?|apartments?|townho\w+|condo\w*|rowhouses?|lofts)', re.I)


def ext(t):
    """Largest plausible unit count named in a city case description."""
    if not isinstance(t, str): return np.nan
    t = re.sub(r'(?i)(roof ?top|mechanical|hvac|condens\w+|a/c|ac|air[- ]handling|storage|retail|commercial|parking|antenna|rtu)[\s-]*units?', '', t)
    v = [int(a) if a.isdigit() else W[a.lower()] for a, b in P1.findall(t)]; v = [x for x in v if 2 < x < 1500]
    return max(v) if v else np.nan


def land_use(lu_rows, bp, P):
    S = pd.read_csv(os.path.join(FROZEN, 'land_use_series.csv'), parse_dates=['INTAKE_COMPLETE', 'ISSUE_DATE'])
    lu = pd.DataFrame(lu_rows)
    for c in ['ISSUED', 'FINALED', 'INTAKECOMPLETEDATE', 'CREATEDATE']: lu[c] = pd.to_datetime(lu[c], unit='ms')
    code = lu.WORK_DESCRIPTION.fillna('').str.split(' - ').str[0].str.strip()
    # (a) cases that were still undecided when the series was frozen: pick up their decision from the feed
    live = lu.set_index('APPLICATION'); undecided = S.SOURCE.str.startswith('2020') & (S.ISSUE_DATE.isna() | ~S.STATUS.isin(APPROVED))
    upd = 0
    for i in S.index[undecided]:
        a = S.at[i, 'APPLICATION_NUMBER']
        if a in live.index:
            q = live.loc[a]
            if isinstance(q, pd.DataFrame): q = q.iloc[0]
            if q.STATUS != S.at[i, 'STATUS'] or (pd.isna(S.at[i, 'ISSUE_DATE']) and pd.notna(q.ISSUED)):
                S.at[i, 'STATUS'] = q.STATUS
                if pd.isna(S.at[i, 'ISSUE_DATE']) and pd.notna(q.ISSUED): S.at[i, 'ISSUE_DATE'] = q.ISSUED
                upd += 1
    # (b) design and historic review cases filed after the series was frozen: unit count from the city description (provisional)
    cutoff = pd.Timestamp('2026-11-06 23:59:59')
    new = lu[(lu.CREATEDATE > cutoff) & code.str.match(r'^(DZM|DZ|HDZM|HDZ|HRM|HR)$') & ~lu.APPLICATION.isin(S.APPLICATION_NUMBER)].copy()
    new['U'] = new.DESCRIPTION.map(ext); new = new[new.U.notna()]
    if len(new):
        S = pd.concat([S, pd.DataFrame({'APPLICATION_NUMBER': new.APPLICATION, 'SOURCE': 'After Nov 2026: city description only (provisional)', 'WORK': new.WORK_DESCRIPTION,
                                        'SERIES_ROLE': 'New units approved (design or historic review)', 'UNITS_APPROVED': new.U, 'STATUS': new.STATUS,
                                        'INTAKE_COMPLETE': new.INTAKECOMPLETEDATE.fillna(new.CREATEDATE), 'ISSUE_DATE': new.ISSUED, 'LATITUDE': new.LATITUDE, 'LONGITUDE': new.LONGITUDE})], ignore_index=True)
    print('land use: decisions picked up', upd, '| new cases added', len(new))
    S['X'], S['Y'] = XY(S.LONGITUDE, S.LATITUDE)
    per = bp[(bp.GROSS_NEW_UNITS > 0) & bp.X.notna() & bp.PROJECT_ID.isin(P.PROJECT_ID)]
    t = cKDTree(per[['X', 'Y']].to_numpy()); ppid = per.PROJECT_ID.to_numpy(); px = per.X.to_numpy(); py = per.Y.to_numpy()
    pinfo = P.set_index('PROJECT_ID'); k11 = dict(zip(bp.APPLICATION.str[:11], bp.PROJECT_ID))
    rows = []; lk = {}  # lk: project -> land use cases (first seen, approved, case number), design and historic reviews only
    for r in S.itertuples():
        cand = {}; how = ''
        c = r.BUILDING_PERMITS_CITED
        if isinstance(c, str) and c:
            for x in c.split('; '):
                pid = k11.get('20' + x)
                if pid in pinfo.index: cand[pid] = 0; how = 'cited'
        if not cand and r.X == r.X and pd.notna(r.INTAKE_COMPLETE):
            for j in t.query_ball_point([r.X, r.Y], 60.0):
                pid = ppid[j]; d = np.hypot(px[j] - r.X, py[j] - r.Y); dd = (pinfo.FIRST_SET_UP[pid] - r.INTAKE_COMPLETE).days
                if -365 <= dd <= 365 * 7: cand[pid] = min(cand.get(pid, 1e9), d)
            how = 'site' if cand else ''
        if not cand:
            rows.append((pd.NaT, '')); continue
        sub = pinfo.loc[list(cand)]
        if r.SERIES_ROLE.startswith('New units') and pd.notna(r.UNITS_APPROVED) and r.UNITS_APPROVED > 0 and how == 'site':
            sub = sub.assign(rat=(sub.GROSS / r.UNITS_APPROVED)); ok = sub[sub.rat.between(0.5, 2.0)]
            if not len(ok):
                rows.append((pd.NaT, '')); continue
            sub = ok.iloc[[(ok.rat - 1).abs().argmin()]]
        out = ('Completed' if (sub.OUTCOME.str.startswith('Completed')).all() else ('Permit issued' if sub.FIRST_ISSUED.notna().any() else ('Permit expired or cancelled' if sub.OUTCOME.str.startswith('Expired').all() else 'Permit in review')))
        rows.append((sub.FIRST_ISSUED.min(), out))
        if r.SERIES_ROLE.startswith('New units') and pd.notna(r.INTAKE_COMPLETE):
            for pid in sub.index: lk.setdefault(pid, []).append((r.INTAKE_COMPLETE, r.ISSUE_DATE if r.STATUS in APPROVED else pd.NaT, r.APPLICATION_NUMBER))
    S['PERMIT_FIRST_ISSUED'] = pd.to_datetime([a for a, b in rows]); S['PERMIT_OUTCOME'] = [b for a, b in rows]
    S['MO'] = ((S.PERMIT_FIRST_ISSUED - S.ISSUE_DATE).dt.days / 30.44).round(1)
    global LINKED; LINKED = S  # the series with each case's permit outcome, kept for the vesting-rush analysis
    U = S[S.SERIES_ROLE.str.startswith('New units') & (S.UNITS_APPROVED > 0) & S.ISSUE_DATE.notna() & S.STATUS.isin(APPROVED)]
    Bn = pd.DataFrame({'DECISION_YEAR': U.ISSUE_DATE.dt.year.astype(int), 'UNITS_APPROVED': U.UNITS_APPROVED, 'REAL': U.PERMIT_OUTCOME.isin(['Completed', 'Permit issued']), 'MO': U.MO})
    # 2000-2009: read by script from the city description (provisional)
    old = lu[(lu.CREATEDATE < '2010-01-01') & code.str.match(r'^(DZM|DZ|HDZM|HDZ|HRM|HR|\(Old\) DR|DR)$') & lu.STATUS.isin(APPROVED)].copy()
    old['U'] = old.DESCRIPTION.map(ext); old = old[old.U.notna() & old.ISSUED.notna()]
    old['X'], old['Y'] = XY(old.LONGITUDE, old.LATITUDE)
    ar = []
    for r in old.itertuples():
        best = None
        if r.X == r.X:
            for j in t.query_ball_point([r.X, r.Y], 60.0):
                q = pinfo.loc[ppid[j]]; dd = (q.FIRST_SET_UP - r.CREATEDATE).days; rat = q.GROSS / r.U
                if -365 <= dd <= 365 * 7 and 0.5 <= rat <= 2 and (best is None or abs(rat - 1) < best[0]): best = (abs(rat - 1), ppid[j])
        fi = pinfo.FIRST_ISSUED[best[1]] if best else pd.NaT
        if best: lk.setdefault(best[1], []).append((r.CREATEDATE, r.ISSUED, r.APPLICATION))
        ar.append(dict(DECISION_YEAR=r.ISSUED.year, UNITS_APPROVED=r.U, REAL=bool(best) and pd.notna(fi), MO=((fi - r.ISSUED).days / 30.44) if pd.notna(fi) else np.nan))
    A = pd.DataFrame(ar)
    C = pd.concat([A[A.DECISION_YEAR < 2010], Bn[Bn.DECISION_YEAR >= 2010]], ignore_index=True)
    out = []
    for y, d in C.groupby('DECISION_YEAR'):
        if y < 2002: continue
        mo = d.loc[d.REAL & (d.MO > -6), 'MO'].median()
        out.append({'y': int(y), 'units': int(d.UNITS_APPROVED.sum()), 'perm': int(d.loc[d.REAL, 'UNITS_APPROVED'].sum()), 'cases': int(len(d)), 'cp': int(d.REAL.sum()), 'mo': (None if pd.isna(mo) else round(float(mo), 1))})
    return out, lk


# ---------------------------------------------------------------- 6. site data
def near_max(P, metres=800):
    """True for each project within `metres` of a MAX light rail line as it runs today (frozen/geo.json)."""
    geo = json.load(open(os.path.join(FROZEN, 'geo.json'))); X0, X1, Y0, Y1 = -122.84, -122.47, 45.43, 45.66
    pts = []
    for ln in geo['mx']:
        L = ln if isinstance(ln[0], (list, tuple)) else [ln[i:i + 2] for i in range(0, len(ln), 2)]
        for (ax, ay), (bx, by) in zip(L[:-1], L[1:]):
            for t in np.linspace(0, 1, 12): pts.append((ax + (bx - ax) * t, ay + (by - ay) * t))
    pts = np.array(pts); lon = X0 + pts[:, 0] / 1000 * (X1 - X0); lat = Y1 - pts[:, 1] / 1000 * (Y1 - Y0)
    tr = cKDTree(np.c_[XY(lon, lat)]); x, y = XY(P.LONGITUDE.to_numpy(), P.LATITUDE.to_numpy())
    ok = ~np.isnan(x); d = np.full(len(P), np.inf); d[ok] = tr.query(np.c_[x[ok], y[ok]])[0]
    return d <= metres


def lu_waits(P):
    """Large projects (75+ homes) with a matched design or historic review that reached a permit:
    months from land use filing to first building permit, for permits issued 2010-2019 and since March 2020."""
    L = P[(P.GROSS >= 75) & P.LU_FIRST_SEEN.notna() & P.FIRST_ISSUED.notna() & ~P.OUTCOME.str.startswith('Expired')].copy()
    mo = lambda a, b: (b - a).dt.days / 30.44
    L['w'] = mo(L.LU_FIRST_SEEN, L.FIRST_ISSUED); L = L[L.w >= 0]
    L['rev'] = mo(L.LU_FIRST_SEEN, L.LU_APPROVED); L['ap'] = mo(L.LU_APPROVED, L.FIRST_ISSUED); L['bp'] = mo(L.FIRST_SET_UP, L.FIRST_ISSUED)
    r1 = lambda v: None if pd.isna(v) else round(float(v), 1)
    def block(d):
        return {'n': int(len(d)), 'med': r1(d.w.median()), 'q1': r1(d.w.quantile(.25)), 'q3': r1(d.w.quantile(.75)), 'rev': r1(d.rev.median()), 'ap': r1(d.ap.median()), 'bp': r1(d.bp.median())}
    a = L[(L.FIRST_ISSUED >= '2010-01-01') & (L.FIRST_ISSUED < '2020-01-01')]; b = L[L.FIRST_ISSUED >= '2020-03-01']
    pts = [[int(r.FIRST_ISSUED.year), round(float(r.w), 1), 2 if r.SUBSIDY == 'Subsidized' else 1, int(r.GROSS)] for r in L.sort_values('FIRST_ISSUED').itertuples()]  # one row per project: year permitted, months waited, funding, homes
    return {'before': block(a), 'since': block(b), 'sub': block(b[b.SUBSIDY == 'Subsidized']), 'mkt': block(b[b.SUBSIDY == 'Market rate']), 'pts': pts}


def site_data(P, lu, asof):
    nm = near_max(P)
    X0, X1, Y0, Y1 = -122.84, -122.47, 45.43, 45.66
    qx = lambda lo: int(round((lo - X0) / (X1 - X0) * 1000)); qy = lambda la: int(round((Y1 - la) / (Y1 - Y0) * 1000))
    rows = []
    for k, r in enumerate(P.itertuples()):
        x = qx(r.LONGITUDE) if r.LONGITUDE == r.LONGITUDE else -1; y = qy(r.LATITUDE) if r.LATITUDE == r.LATITUDE else -1
        sub = 1 if r.SUBSIDY == 'Market rate' else (2 if r.SUBSIDY == 'Subsidized' else 0)
        yi = int(r.YEAR_ISSUED) if r.YEAR_ISSUED == r.YEAR_ISSUED else 0
        yf = int(r.LAST_FINAL.year) if (r.OUTCOME.startswith('Completed') and pd.notna(r.LAST_FINAL)) else 0
        mo = round(max((r.FIRST_ISSUED - r.FIRST_SET_UP).days / 30.44, 0), 1) if pd.notna(r.FIRST_ISSUED) else -1  # months from permit application to first permit issued
        rows.append([x, y, int(r.YEAR), yi, int(r.GROSS), int(r.NET), sub, 1 if r.OUTCOME.startswith('Expired') else 0, yf, mo, int(nm[k])])
    L = P[(P.GROSS >= 5) & P.FIRST_ISSUED.notna()].copy(); L['m'] = (L.FIRST_ISSUED - L.FIRST_SET_UP).dt.days / 30.44
    g = L.groupby('YEAR_ISSUED').m
    dur = [{'y': int(y), 'm': round(float(g.median()[y]), 1), 'q1': round(float(g.quantile(.25)[y]), 1), 'q3': round(float(g.quantile(.75)[y]), 1)} for y in sorted(g.groups)]
    geo = json.load(open(os.path.join(FROZEN, 'geo.json'))); pop = json.load(open(os.path.join(FROZEN, 'population.json')))
    return {'p': rows, 'b': geo['b'], 'w': geo['w'], 'dur': dur, 'lu': lu, 'asof': asof, 'pop': pop, 'fw': geo['fw'], 'mx': geo['mx']}


def vesting_rush(S, P):
    """Monthly filings around the 1 Feb 2017 inclusionary housing rule, for projects of 20+ homes (the rule's threshold).
    lu: design/historic review applications by month filed -> [homes that reached a permit, homes with no permit so far, cases, cases that reached a permit]
    bp: building permit applications by month filed -> [homes issued a permit, homes not issued, projects, projects issued]
    iss: building permits by month issued -> [homes, projects]"""
    months = pd.period_range('2011-01', '2019-12', freq='M'); ix = {m: i for i, m in enumerate(months)}
    lu = [[0, 0, 0, 0] for _ in months]; bpm = [[0, 0, 0, 0] for _ in months]; iss = [[0, 0] for _ in months]
    N = S[S.SERIES_ROLE.str.startswith('New units') & (S.UNITS_APPROVED >= 20) & S.INTAKE_COMPLETE.notna()]
    for r in N.itertuples():
        i = ix.get(pd.Period(r.INTAKE_COMPLETE, 'M'))
        if i is None: continue
        real = r.PERMIT_OUTCOME in ('Completed', 'Permit issued'); u = int(r.UNITS_APPROVED)
        lu[i][0 if real else 1] += u; lu[i][2] += 1; lu[i][3] += int(real)
    for r in P[P.GROSS >= 20].itertuples():
        i = ix.get(pd.Period(r.FIRST_SET_UP, 'M')); got = pd.notna(r.FIRST_ISSUED) and not r.OUTCOME.startswith('Expired'); u = int(r.GROSS)
        if i is not None:
            bpm[i][0 if got else 1] += u; bpm[i][2] += 1; bpm[i][3] += int(got)
        if got:
            j = ix.get(pd.Period(r.FIRST_ISSUED, 'M'))
            if j is not None: iss[j][0] += u; iss[j][1] += 1
    return {'start': [2011, 1], 'lu': lu, 'bp': bpm, 'iss': iss}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--cache'); ap.add_argument('--asof'); ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    raw = get_raw(a.cache)
    bp = load(raw['bp'])
    bp, proj = build_projects(bp, raw['demo'])
    proj = match_subsidy(bp, proj)
    P = baseline(bp, proj)
    lu, lk = land_use(raw['lu'], bp, P)
    first = {pid: min(v, key=lambda t: t[0]) for pid, v in lk.items()}  # the earliest land use case tied to each project
    P['LU_CASE'] = P.PROJECT_ID.map(lambda x: first[x][2] if x in first else '')
    P['LU_FIRST_SEEN'] = pd.to_datetime(P.PROJECT_ID.map(lambda x: first[x][0] if x in first else pd.NaT))
    P['LU_APPROVED'] = pd.to_datetime(P.PROJECT_ID.map(lambda x: first[x][1] if x in first else pd.NaT))
    asof = a.asof or max(bp.CREATEDATE.max(), bp.ISSUED.max()).strftime('%B %-d, %Y')
    D = site_data(P, lu, asof)
    D['iz'] = vesting_rush(LINKED, P)
    D['luw'] = lu_waits(P)
    live = P[~P.OUTCOME.str.startswith('Expired')]
    summ = {'asof': asof, 'projects': int(len(P)), 'gross_units_set_up': int(P.GROSS.sum()), 'net_units_set_up': int(P.NET.sum()),
            'gross_units_issued': int(live[live.FIRST_ISSUED.notna()].GROSS.sum()), 'net_units_issued': int(live[live.FIRST_ISSUED.notna()].NET.sum()),
            'subsidy': {k: int(v) for k, v in P.SUBSIDY.value_counts().items()}}
    print(json.dumps(summ, indent=1))
    # ---- safety check: a refresh must not publish a collapsed or wildly different data set
    os.makedirs(OUT, exist_ok=True); sf = os.path.join(OUT, 'summary.json')
    if os.path.exists(sf) and not a.force:
        prev = json.load(open(sf))
        for k in ['projects', 'gross_units_set_up', 'net_units_issued']:
            if summ[k] < prev[k] * 0.98 or summ[k] > prev[k] * 1.10:
                sys.exit(f'STOPPED: {k} moved from {prev[k]:,} to {summ[k]:,}. That is outside the expected range for one quarter, so nothing was published. Check the city feed, then rerun with --force if the change is real.')
    json.dump(summ, open(sf, 'w'), indent=1)
    open(os.path.join(OUT, 'data.json'), 'w').write(json.dumps(D, separators=(',', ':')))
    cols = {'PROJECT_ID': 'PROJECT_ID', 'YEAR': 'YEAR_FIRST_SET_UP', 'YEAR_ISSUED': 'YEAR_FIRST_ISSUED', 'PROJECT_ADDRESS': 'PROJECT_ADDRESS', 'NEIGHBORHOOD': 'NEIGHBORHOOD', 'CLASS': 'CAPITAL_CLASS', 'SUBSIDY': 'SUBSIDY',
            'GROSS': 'GROSS_NEW_UNITS', 'DEMOLISHED_UNITS': 'DEMOLISHED_UNITS', 'NET': 'NET_NEW_UNITS', 'OUTCOME': 'OUTCOME', 'DEVELOPER': 'DEVELOPER', 'SUBSIDY_BASIS': 'SUBSIDY_BASIS', 'REVIEW_STATUS': 'REVIEW_STATUS',
            'PERMITS': 'PERMITS', 'TYPES': 'TYPES', 'UNIT_EVENTS': 'UNIT_EVENTS', 'FIRST_SET_UP': 'FIRST_SET_UP', 'FIRST_ISSUED': 'FIRST_ISSUED', 'LAST_FINAL': 'LAST_FINAL', 'MATCH_NAME': 'SUBSIDY_RECORD_NAME', 'FIRST_APPLICATION': 'FIRST_APPLICATION', 'LU_CASE': 'LAND_USE_CASE', 'LU_FIRST_SEEN': 'LAND_USE_FIRST_SEEN', 'LU_APPROVED': 'LAND_USE_APPROVED', 'LATITUDE': 'LATITUDE', 'LONGITUDE': 'LONGITUDE'}
    T = P[list(cols)].rename(columns=cols)
    T.to_csv(os.path.join(OUT, 'projects.csv'), index=False)
    # projects of 5+ homes first set up after the November 2026 review, tagged by rule only: these need a human look
    nr = T[(T.GROSS_NEW_UNITS >= 5) & (T.FIRST_SET_UP > '2026-11-06') & (T.REVIEW_STATUS == 'Rule-based, not individually reviewed')].sort_values('GROSS_NEW_UNITS', ascending=False)
    nr.to_csv(os.path.join(OUT, 'new_projects_to_review.csv'), index=False)
    print('new 5+ unit projects awaiting review:', len(nr))


if __name__ == '__main__':
    main()
