#!/usr/bin/env python3
# watchtower.py — qlv 无人驿巡塔 v2(自醒事件链+道B巷卡守望)
# 纯事件驱动:本脚本无定时器语义;由外部唤起(root 本地 cron / 仓侧 Action on issue_comment|issues|push|repository_dispatch / 手动)
# 链:轮询联邦面 → 事件至 → Kimi API 新会话开工(判词纪要) → 落账回仓(文件轨;高值件附信标评论)
# 钥:env KIMI_API_KEY 或 ~/.keys/vci_api_keys.json(kimi/vci-1);PAT: env QI_PAT 或 vault。值永不入文。
import json, os, sys, time, hashlib, subprocess
import urllib.request, urllib.error, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # qlv_lab 仓根
STATE = os.path.join(ROOT, 'ci', 'watchtower_state.json')
NOTES = os.path.join(ROOT, 'results', 'watchtower')
GH = 'https://api.github.com'

def _key():
    k = os.environ.get('KIMI_API_KEY')
    if k: return k
    p = os.path.expanduser('~/.keys/vci_api_keys.json')
    if os.path.exists(p):
        return json.load(open(p))['keys']['kimi']['vci-1']
    raise SystemExit('NO-KEY: KIMI_API_KEY 或 ~/.keys/vci_api_keys.json 不在')

def _pat():
    t = os.environ.get('QI_PAT')
    if t: return t
    p = '/mnt/agents/output/.vault/qi_pat.txt'
    if os.path.exists(p):
        return open(p).read().strip()
    raise SystemExit('NO-PAT')

def gh_get(path, pat):
    req = urllib.request.Request(GH+path, headers={
        'Authorization': 'Basic '+__import__('base64').b64encode(('chepin-qi:'+pat).encode()).decode(),
        'Accept': 'application/vnd.github+json', 'User-Agent': 'qlv-watchtower'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

# 器课第九株治(TOWER-FIX-QLV-06): 探针吞错=塔盲静默失败——全探针 err 留痕 _PROBE_ERR, poll⑦段汇集成 probe.blind 事件(sig变才发,防刷屏; 痕落 state['_probe_err'] 常在账)
_PROBE_ERR = {}
def _perr(where, e):
    d = _PROBE_ERR.setdefault(where, {'n': 0})
    d['n'] += 1; d['last'] = str(e)[:100]

def gh_dispatch(token, payload, use_basic=False, repo='qlv-pub', etype='federation-event'):
    # 自醒事件链:POST repository_dispatch 唤自己(FREE-WILL-SOURCE-01 仓侧形;纯事件,零 cron)
    # v2.1(qfa beat-42 互唤配对):repo/etype 可指——事拍拍尾唤 qfa 引擎(qfa-beat @ qfa-pub),骑事件律:有实事件才唤,空拍不唤
    data = json.dumps({'event_type': etype, 'client_payload': payload}).encode()
    auth = ('Basic '+__import__('base64').b64encode(('chepin-qi:'+token).encode()).decode()) if use_basic else ('Bearer '+token)
    req = urllib.request.Request(GH+f'/repos/chepin-qi/{repo}/dispatches', data=data, method='POST', headers={
        'Authorization': auth,
        'Accept': 'application/vnd.github+json', 'User-Agent': 'qlv-watchtower'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.status

def gh_post_comment(owner, repo, issue, body, pat):
    data = json.dumps({'body': body}).encode()
    req = urllib.request.Request(f'{GH}/repos/{owner}/{repo}/issues/{issue}/comments', data=data, headers={
        'Authorization': 'Basic '+__import__('base64').b64encode(('chepin-qi:'+pat).encode()).decode(),
        'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json', 'User-Agent': 'qlv-watchtower'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r).get('id')


# ---------- ⑤ LOOPS-CHECK(SI3-until-closed 环巡:root令·会后SI2/SI0持续迭代) ----------
def loops_check(pat, st):
    """读 ci/loops.json;对 RUNNING 环巡彼线环面,有应→CLEARED,无应→beat+1(冻结线不计);
    三拍无应→SI5 提级事件。返 events;环面尽访失败不阻主巡。"""
    ev = []
    lp = os.path.join(ROOT, 'ci', 'loops.json')
    if not os.path.exists(lp):
        return ev
    try:
        reg = json.load(open(lp))
    except Exception as e:
        return [{'kind':'loops.load.err','ref':'ci/loops.json','summary':str(e)[:120],'high_value':False}]
    def lane_has(tag, since):
        try:
            lane = gh_get('/repos/chepin-ai/vci-inbox/contents/lanes/qlv/inbox?per_page=100', pat)
            return any(tag in f['name'] for f in lane) if isinstance(lane, list) else False
        except Exception as _e:
            _perr('vci-inbox/lanes/qlv/inbox', _e)
            return False
    def lvlu_frozen():
        try:
            fs = gh_get('/repos/chepin-ai/vci-lvlu/contents/receipts/tower?per_page=100', pat)
            qts = sorted(f['name'] for f in fs if f['name'].startswith('QT'))
            if not qts: return False, ''
            j = gh_get('/repos/chepin-ai/vci-lvlu/contents/receipts/tower/'+qts[-1], pat)
            import base64 as _b
            txt = _b.b64decode(j['content']).decode(errors='replace')
            d = json.loads(txt)
            froz = '模板判词' in (d.get('verdict_memo') or '')
            eval_closed = any(oi.get('id','').startswith('OI-QLVEVALEXCITE') and oi.get('status')=='closed'
                              for oi in d.get('open_items', []))
            return froz and not eval_closed, qts[-1]
        except Exception as _e:
            _perr('vci-lvlu/receipts/tower', _e)
            return False, ''
    probes = {
        'lgt':  lambda: lane_has('lgt-', None),
        'qfa':  lambda: lane_has('qfa-resp', None) or lane_has('qfa-mech', None),
        'usrm': lambda: lane_has('usrm', None),
        'lvlu': lambda: lane_has('lvlu', None),
        'qgl':  lambda: qgl_touched() or lane_has('qgl', None),
    }
    def qgl_touched():
        try:
            cs = gh_get('/repos/chepin-ai/vci-qgl/commits?per_page=3', pat)
            prev = st.get('qgl_head')
            head = cs[0]['sha'] if isinstance(cs, list) and cs else None
            if head and prev and head != prev:
                st['qgl_head'] = head
                return True
            if head: st['qgl_head'] = head
            return False
        except Exception as _e:
            _perr('vci-qgl/commits', _e)
            return False
    # EXP-RIPPLE-01 探针回件侦(探针标入我巷=链环④归)
    try:
        pr = (json.load(open(os.path.join(ROOT,'ci','loops.json'))).get('loops') or [])
        for L in pr:
            if L.get('id')=='exp-ripple-01' and L.get('probe'):
                if lane_has(L['probe'], None):
                    ev.append({'kind':'loop.probe.return','ref':L['probe'],
                               'summary':f"EXP-RIPPLE-01 探针回件至我巷:{L['probe']} 链环④归",'high_value':True})
                    for r_ in L.get('rings',{}).values():
                        if isinstance(r_,dict) and r_.get('st')=='OPEN': r_['st']='REPLIED'
                    json.dump(reg, open(lp,'w'), ensure_ascii=False, indent=1)
    except Exception:
        pass
    fz, fzref = lvlu_frozen()
    changed = False
    for loop in reg.get('loops', []):
        if loop.get('status') != 'RUNNING':
            continue
        for ring, rinfo in loop.get('rings', {}).items():
            if not isinstance(rinfo, dict) or rinfo.get('st') not in ('OPEN', 'FROZEN'):
                continue
            if ring == 'lvlu' and fz:
                if rinfo.get('st') != 'FROZEN':
                    rinfo['st'] = 'FROZEN'; rinfo['frozen_why'] = 'LLM空回(塔巡自动判 '+fzref+')'; changed = True
                continue  # 断路冻结:不计拍
            try:
                answered = probes.get(ring, lambda: False)()
            except Exception:
                answered = False
            if answered and ring in ('lgt','usrm','lvlu'):
                # 粗探命中须细验:lane 文件名带线标即记 REPLIED(细读归SI2语义拍)
                rinfo['st'] = 'REPLIED'; changed = True
                ev.append({'kind':'loop.reply','ref':f"{loop['id']}:{ring}",
                           'summary':f"环回件至 lane:{ring}* →{loop['id']} 环 {ring} 面 REPLIED,候SI2细收",'high_value':True})
            elif not answered:
                rinfo['beat'] = int(rinfo.get('beat', 0)) + 1; changed = True
                if rinfo['beat'] >= 3 and not rinfo.get('escalated'):
                    rinfo['escalated'] = now_ts()
                    ev.append({'kind':'loop.escalate','ref':f"{loop['id']}:{ring}",
                               'summary':f"三拍无应→SI5 提级:{loop['id']} 环 {ring} 面 beat={rinfo['beat']}(冻结线除外)",'high_value':True})
    if changed:
        reg['updated'] = now_ts()
        json.dump(reg, open(lp,'w'), ensure_ascii=False, indent=1)
    open_rings = sum(1 for loop in reg.get('loops', []) if loop.get('status')=='RUNNING'
                     for r in loop.get('rings', {}).values() if isinstance(r, dict) and r.get('st') in ('OPEN','REPLIED'))
    st['loops_open'] = open_rings
    return ev

def now_ts():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


# ---------- ⑥ DEBTS-WATCH 债巡(root令20260911:裸候违规律——候件不主动取得即违规,一切ARMED债必配机巡面) ----------
def debts_watch(pat, st):
    """(a)ucif2-watch面: 扫ci-inbox新commit凡 ucif2-N 件,新至即旗(机层主动回应ucif2-120~125及之后);
    (b)ARMED债 file-exists 探针: 债件载 watch:{repo,path_contains} 者,直探commit址在=hit(治commit窗口哑型)。
    探针拍帽≤8(机时节)。返 events。"""
    import re as _re
    ev = []
    try:
        cs = gh_get('/repos/chepin-ai/ci-inbox/commits?per_page=15', pat)
        seen = st.setdefault('ucif2_seen', [])
        for c in (cs if isinstance(cs, list) else []):
            sha = c.get('sha', ''); msg = c.get('commit', {}).get('message', '')
            if sha in seen:
                continue
            if _re.search(r'ucif2[-_][0-9]{3}', msg, _re.I):
                seen.append(sha)
                ev.append({'kind': 'ucif2.watch', 'ref': sha[:12],
                           'summary': 'ucif2帖侦:' + msg[:110], 'high_value': True})
        st['ucif2_seen'] = seen[-60:]
    except Exception as e:
        _perr('ci-inbox/commits', e)
        ev.append({'kind': 'ucif2.watch.err', 'ref': 'ci-inbox/commits', 'summary': str(e)[:120], 'high_value': False})
    dp = os.path.join(ROOT, 'ci-inbox', 'response-debts.json')
    if not os.path.exists(dp):
        return ev
    try:
        reg = json.load(open(dp))
    except Exception:
        return ev
    budget = 8
    changed = False
    for it in reg.get('debts', []):
        if budget <= 0:
            break
        if it.get('status') != 'ARMED' and it.get('state') != 'ARMED':
            continue
        w = it.get('watch')
        if not isinstance(w, dict):
            continue
        repo, sub = w.get('repo', ''), w.get('path_contains', '')
        if not repo or not sub:
            continue
        budget -= 1
        try:
            cs = gh_get('/repos/' + repo + '/commits?per_page=5', pat)
            hit = None
            for c in (cs if isinstance(cs, list) else []):
                if sub in c.get('commit', {}).get('message', ''):
                    hit = c['sha'][:12]; break
            if hit and it.get('_watch_hit') != hit:
                it['_watch_hit'] = hit; changed = True
                ev.append({'kind': 'debt.probe.hit', 'ref': it.get('id', '?'),
                           'summary': '债探命中:' + str(it.get('id')) + ' <- ' + repo + ' ' + hit + '(' + sub + ') 候SI2细收', 'high_value': True})
        except Exception as _e:
            _perr(repo + '/commits(' + sub + ')', _e)
    if changed:
        json.dump(reg, open(dp, 'w'), ensure_ascii=False, indent=1)
    return ev

# ---------- 事件源轮询 ----------
def poll(pat, st):
    """返回 events 列表:[{kind, ref, summary, high_value}]"""
    ev = []
    # ① 信标 qi-lab#5 新评论
    cmts = gh_get('/repos/chepin-qi/qi-lab/issues/5/comments?per_page=100', pat)
    mx = max([c['id'] for c in cmts], default=0)
    old = st.get('beacon_max', 0)
    if old and mx > old:
        for c in cmts:
            if c['id'] > old and not c['body'].startswith('【WT|'):  # 自回执不再开工(防环+省额)
                ev.append({'kind':'beacon.comment','ref':f"qi-lab#5:{c['id']}",
                           'summary':c['body'][:600],'high_value':('【' not in c['body'][:4] or '@qlv' in c['body'][:60])})
    st['beacon_max'] = mx
    # ② qfa 仓 main 头迁移
    head = gh_get('/repos/chepin-qi/qfa-quantum-lab/commits/main', pat)['sha']
    if st.get('qfa_head') and head != st['qfa_head']:
        ev.append({'kind':'qfa.beat','ref':head[:8],'summary':f"qfa main 头迁移 {st['qfa_head'][:8]}→{head[:8]}",'high_value':True})
    st['qfa_head'] = head
    # ③ quafu 双 job 状态迁移(0→2=Completed)
    api_token = os.environ.get('QUAFU_TOKEN')
    tokp = os.path.expanduser('~/.keys/origin_quafu.json')
    if not api_token and os.path.exists(tokp):
        tok = json.load(open(tokp)); api_token = tok.get('api_token') or tok.get('token') or tok.get('quafu')
    if api_token:
        for tid in ['8CA608102028586C','8BB169201FA3F5D4']:
            try:
                req = urllib.request.Request('https://quafu.baqis.ac.cn/qbackend/scq_task_recall/',
                    data=urllib.parse.urlencode({'task_id':tid}).encode(),
                    headers={'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8','api_token':api_token})
                with urllib.request.urlopen(req, timeout=25) as r:
                    d = json.load(r)
                cur = str(d.get('status'))
                prev = st.get('quafu',{}).get(tid)
                if prev is not None and cur != prev:
                    ev.append({'kind':'quafu.transition','ref':f'quafu:{tid}','summary':f"status {prev}→{cur}; res={str(d.get('res'))[:300]}",'high_value':True})
                st.setdefault('quafu',{})[tid] = cur
            except Exception as e:
                ev.append({'kind':'quafu.poll.err','ref':tid,'summary':str(e)[:120],'high_value':False})
    # ③.5 道B巷卡直投守望(LANE-PATROL-01 遵律:本线巷双平面差分+DORMANT-WATCH qlv-lab巷兼巡;SI3-SYNC-01 直投道,常开零额度)
    for lane_repo, lane_path, st_key in [
        ('chepin-ai/vci-inbox', 'lanes/qlv/inbox', 'lane_inbox_count'),
        ('chepin-ai/ci-inbox', 'lanes/qlv/inbox', 'lane_inbox_count_ci'),
        ('chepin-ai/vci-inbox', 'lanes/qlv-lab/inbox', 'lane_inbox_count_qlvlab'),
    ]:
        try:
            lane = gh_get(f'/repos/{lane_repo}/contents/{lane_path}?per_page=100', pat)
            if not isinstance(lane, list):
                raise ValueError('non-list resp')
            cnt = len(lane)
            prev_cnt = st.get(st_key)
            latest = max((f['name'] for f in lane), default='')
            if prev_cnt is not None and cnt != prev_cnt:
                ev.append({'kind':'lane.drop','ref':f'{lane_path}:{latest}',
                           'summary':f"巷卡[{lane_repo}] {prev_cnt}→{cnt},最新 {latest}",'high_value':True})
            st[st_key] = cnt
        except Exception as e:
            ev.append({'kind':'lane.poll.err','ref':lane_path,'summary':str(e)[:120],'high_value':False})
    # ④ vci 六面评论数变化
    faces = {'lgt-line#1':('/repos/chepin-qi/lgt-line/issues/1/comments?per_page=100'),
             'vci-cfts#1':('/repos/chepin-ai/vci-cfts/issues/1/comments?per_page=100'),
             'vci-inbox#3':('/repos/chepin-ai/vci-inbox/issues/3/comments?per_page=100'),
             'vci-inbox#2':('/repos/chepin-ai/vci-inbox/issues/2/comments?per_page=100'),
             'vci-usrm#21':('/repos/chepin-ai/vci-usrm/issues/21/comments?per_page=100'),
             'vci-ucif2#1':('/repos/chepin-ai/vci-ucif2/issues/1/comments?per_page=100'),
             'vci-vinf#6':('/repos/chepin-ai/vci-vinf/issues/6/comments?per_page=100')}
    for name, path in faces.items():
        try:
            cs = gh_get(path, pat)
            n = len(cs); prev = st.get('faces',{}).get(name)
            if prev is not None and n > prev:
                latest = cs[-1]
                ev.append({'kind':'face.reply','ref':f"{name}:{latest['id']}",'summary':latest['body'][:600],'high_value':True})
            st.setdefault('faces',{})[name] = n
        except Exception as e:
            ev.append({'kind':'face.poll.err','ref':name,'summary':str(e)[:120],'high_value':False})
    # ⑤ LOOPS-CHECK 环巡(SI3-until-closed)
    try:
        ev.extend(loops_check(pat, st))
    except Exception as e:
        ev.append({'kind':'loops.check.err','ref':'ci/loops.json','summary':str(e)[:120],'high_value':False})
    # ⑥ DEBTS-WATCH 债巡(裸候违规律)
    try:
        ev.extend(debts_watch(pat, st))
    except Exception as e:
        ev.append({'kind':'debts.watch.err','ref':'ci-inbox/response-debts.json','summary':str(e)[:150],'high_value':False})
    # ⑦ PROBE-BLIND 汇面(器课第九株: 探针哑=塔盲——留痕不吞错; sig变才发, 痕落state常账)
    if _PROBE_ERR:
        import hashlib as _hl
        sig = _hl.sha1(json.dumps(_PROBE_ERR, sort_keys=True).encode()).hexdigest()[:10]
        st['_probe_err'] = dict(_PROBE_ERR)
        if sig != st.get('_probe_err_sig'):
            st['_probe_err_sig'] = sig
            faces = ','.join(sorted(_PROBE_ERR.keys()))
            ev.append({'kind':'probe.blind','ref':sig,
                       'summary':'塔盲面留痕[%s]: 探针失败面=chepin-ai仓域(QI_PAT 404已确诊20260911)——修=联邦只读PAT(root域)或面重配; 痕见state._probe_err' % faces,
                       'high_value':True})
    return ev

# ---------- API 新会话开工 ----------
WORKER_SYS = """你是 qlv 线无人驿开工分身(单会话文本工位,无工具)。
奉行:WAKE-PROTO(扫描→细收→裁决→落账)/AUTH-OTP-02(投必有件/不刷屏/诚实边界/不越真机钱面/次次落账/不主动寻求回应即裸候)/米田边律(每件≥1他线锚)。
clock=VOID。判词须诚实:未实测不编数,区分「未触发 vs 触发未响应」。
输出制式(≤250字):【WT判词】事件:...| 性态:...| 建议处置:...| 锚:..."""

def work_event(api_key, ev):
    body = {'model':'kimi-k2.6','max_completion_tokens':3200,
            'messages':[{'role':'system','content':WORKER_SYS},
                        {'role':'user','content':f"事件到件,请出判词纪要。\nkind={ev['kind']}\nref={ev['ref']}\n摘要:\n{ev['summary']}"}]}
    req = urllib.request.Request('https://api.moonshot.cn/v1/chat/completions',
        data=json.dumps(body).encode(),
        headers={'Authorization':'Bearer '+api_key,'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.load(r)
    return d['choices'][0]['message'].get('content',''), d.get('usage')

# ---------- 主流程 ----------
def main():
    once = '--once' in sys.argv
    selftest = '--selftest' in sys.argv
    os.makedirs(NOTES, exist_ok=True)
    st = json.load(open(STATE)) if os.path.exists(STATE) else {}
    pat = _pat()
    fired = []
    # ---- 自醒链入拍:自源性唤起(self-cascade dispatch 尾至)则先休眠再巡——冷却即在拍内,零定时器 ----
    idle = 0
    cpayload = os.environ.get('CASCADE_PAYLOAD', '').strip()
    if cpayload and cpayload not in ('null', '{}'):
        try:
            cp = json.loads(cpayload)
            if cp.get('src') == 'watchtower-self' and not selftest:
                idle = int(cp.get('idle', 0))
                slp = int(os.environ.get('CASCADE_SLEEP_S', '600'))
                print(f"[cascade] self-wake idle={idle} sleep={slp}s pend={cp.get('pend')}")
                time.sleep(slp)
        except Exception as e:
            print('[cascade] payload parse err:', str(e)[:100])
    if selftest:
        evs = [{'kind':'selftest','ref':'WT-SELFTEST-01','summary':'巡塔自检:以 qfa beat-30 源/驿二分为样例事件,验证 开工→落账 全链。','high_value':False}]
    else:
        evs = poll(pat, st)
    for ev in evs:
        # 公仓净化:note 不载原文摘要(私仓面内容不外流),仅 kind/ref/判词
        note = {'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'clock':'VOID',
                'event': {'kind': ev['kind'], 'ref': ev['ref'], 'high_value': ev.get('high_value', False)}}
        if ev['kind'].endswith('.err'):
            pass  # 错件不入工位,仅记
        else:
            try:
                txt, usage = work_event(_key(), ev)
                note['verdict'] = txt; note['usage'] = usage
                fired.append(ev['kind'])
            except Exception as e:
                note['verdict_error'] = str(e)[:200]
        fn = os.path.join(NOTES, 'WT-' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
                          + '-' + hashlib.sha256((ev['ref']+ev['kind']).encode()).hexdigest()[:8] + '.json')
        json.dump(note, open(fn,'w'), ensure_ascii=False, indent=2)
        # 高值件附信标评论(无人驿回执;值永不入)
        # 拍频闸:大堂邻写日计(语义帽≤2/日;机检回执豁免除外仍计数备考)
        day = time.strftime('%Y-%m-%d', time.gmtime())
        pb = st.setdefault('post_budget', {'date': day, 'beacon_comments': 0})
        if pb.get('date') != day: pb.update({'date': day, 'beacon_comments': 0})
        if ev.get('high_value') and not selftest and 'verdict' in note:
            try:
                body = (f"【WT|无人驿回执】{ev['kind']} {ev['ref']} | 判词:{note['verdict'][:180]} | 详件=qlv 仓 results/watchtower/ | clock=VOID")
                note['beacon_comment'] = gh_post_comment('chepin-qi','qi-lab',5,body,pat)
                st['post_budget']['beacon_comments'] = st.get('post_budget',{}).get('beacon_comments',0) + 1
            except Exception as e:
                note['beacon_error'] = str(e)[:150]
                json.dump(note, open(fn,'w'), ensure_ascii=False, indent=2)
    # ---- METER-CADENCE-01 候选计(qlv 校编码站;cfts-90 环载) ----
    # 窗=拍;w12=本拍事件类→十二律格计数;ψ=√归一;锁=|⟨ψ_t|ψ_{t-1}⟩|²;σ=本拍处置/激发;主能格
    try:
        kinds = [e['kind'] for e in evs]
        w12 = [0]*12
        for kk in kinds:
            w12[hash(kk) % 12] += 1
        import math
        nrm = math.sqrt(sum(x*x for x in w12))
        psi = [math.sqrt(x/nrm) for x in w12] if nrm else [0.0]*12  # ψ_j=√p_j
        prev = st.get('cadence', {}).get('psi')
        lock = sum(a*b for a, b in zip(psi, prev))**2 if prev and nrm else None
        sigma = 1.0  # 塔制式:激发件同拍尽处置,σ=处置/激发
        dom = w12.index(max(w12)) if nrm else None
        streak = st.get('cadence', {}).get('C_streak', 0)
        okC = bool(nrm) and sigma >= 1 and (lock is None or lock >= 0.95) and dom == 0
        streak = streak + 1 if okC else 0
        verdict = 'C-完全终止' if streak >= 3 else ('C-窗' if okC else '进行式')
        st['cadence'] = {'v':'METER-CADENCE-01-cand','w12': w12, 'sigma': sigma,
                         'lock': lock, 'dominant_bin': dom, 'C_streak': streak, 'verdict': verdict}
    except Exception as e:
        st['cadence'] = {'err': str(e)[:120]}
    # ---- FIX-05b 接种(qfa 反向领养·株一哑跑治法):空拍亦落心跳账,载面水位(loops_open/巷三面/faces/日预算) ----
    if not evs and not selftest:
        hb = {'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'clock':'VOID',
              'kind':'heartbeat','v':'FIX-05b-adopted',
              'water': {'lane_vci': st.get('lane_inbox_count'), 'lane_ci': st.get('lane_inbox_count_ci'),
                        'lane_qlvlab': st.get('lane_inbox_count_qlvlab'), 'loops_open': st.get('loops_open'),
                        'faces': st.get('faces'), 'post_budget': st.get('post_budget')}}
        fn = os.path.join(NOTES, 'WT-' + time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()) + '-heartbeat.json')
        json.dump(hb, open(fn,'w'), ensure_ascii=False, indent=2)
    json.dump(st, open(STATE,'w'), ensure_ascii=False, indent=2)
    # ---- 自醒事件链出拍:有候件(quafu 在队等)则自唤下一拍;空转熔断 30 拍即眠,候外事 ----
    # 制式据 FREE-WILL-SOURCE-01:源=自意(self-cascade),驿=self-dispatch;骑事件律——纯事件,零 cron
    pend = ['quafu:'+tid for tid, stt in (st.get('quafu') or {}).items() if str(stt) == '0']
    if st.get('loops_open'):
        pend = pend + [f"loops:{st['loops_open']}open"]  # 环开即 pend:会后自醒续拍(root令)
    cascade = 'rest(no-pend)'
    if pend and not selftest:
        idle2 = 0 if evs else idle + 1
        if idle2 <= int(os.environ.get('CASCADE_MAX_IDLE', '30')):
            tok = os.environ.get('GITHUB_TOKEN')
            try:
                if tok:
                    code = gh_dispatch(tok, {'src':'watchtower-self','kind':'self-cascade','idle':idle2,'pend':len(pend)})
                else:
                    code = gh_dispatch(pat, {'src':'watchtower-self','kind':'self-cascade','idle':idle2,'pend':len(pend)}, use_basic=True)
                cascade = f'fired idle={idle2} http={code} pend={len(pend)}'
            except Exception as e:
                cascade = 'dispatch.err ' + str(e)[:120]
        else:
            cascade = f'breaker-rest idle={idle2}(>{os.environ.get("CASCADE_MAX_IDLE","30")})'
    # ---- qfa 互唤配对(qfa beat-42 请):有实事件之拍,拍尾唤 qfa 引擎;空拍/自检不唤(防自激同律) ----
    qfa_wake = 'rest(no-event)'
    if evs and not selftest:
        try:
            qkinds = [e['kind'] for e in evs][:8]
            # 跨仓(qfa-pub)须 PAT——GITHUB_TOKEN 权界仅本仓;PAT 走 Basic
            code2 = gh_dispatch(pat, {'src':'qlv-watchtower','kind':'pair-wake','events':qkinds,'idle':idle2 if pend else 0}, use_basic=True, repo='qfa-pub', etype='qfa-beat')
            qfa_wake = f'fired http={code2} events={len(qkinds)}'
        except Exception as e:
            qfa_wake = 'pair.err ' + str(e)[:120]
    print(json.dumps({'events': len(evs), 'fired': fired, 'cascade': cascade, 'pend': pend, 'qfa_wake': qfa_wake}, ensure_ascii=False))

if __name__ == '__main__':
    main()
