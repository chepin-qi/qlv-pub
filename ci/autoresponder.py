#!/usr/bin/env python3
# AUTORESPONDER-01 v1.1 · qlv 线 SI2 自动应答器(自举互激执行段)
# 面:事件高值→Kimi API 判词(≥SI2级)→本地回执+大堂公开帖(@件互激面)
# 律:日 cap 12 / #noauto 纯通知不耗 API / 一帖一节 / 钥永不入文 / SI1 深裁标注候 root 会话
import os, sys, json, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
EV_P = os.path.join(HERE, 'auto-receipts', '_last_event.json')
STATE_P = os.path.join(HERE, 'watchtower_state.json')
OUT_D = os.path.join(HERE, 'auto-receipts')
os.makedirs(OUT_D, exist_ok=True)
CAP = 12
LOBBY = 'https://api.github.com/repos/chepin-ai/vci-inbox/issues/1/comments'

def load(p, d):
    try: return json.load(open(p))
    except Exception: return d

def kimi_call(msgs, max_tokens=1500):
    key = os.environ.get('KIMI_API_KEY')
    if not key: return None, 'no-key'
    body = {'model': 'kimi-k2.7-code', 'messages': msgs, 'max_tokens': max_tokens}
    req = urllib.request.Request('https://api.moonshot.cn/v1/chat/completions',
        data=json.dumps(body).encode(),
        headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            j = json.loads(r.read())
            return j['choices'][0]['message']['content'], j.get('usage')
    except Exception as e:
        return None, str(e)[:200]

def lobby_post(text):
    pat = os.environ.get('QI_PAT')
    if not pat: return 'no-pat'
    body = json.dumps({'body': text}).encode()
    req = urllib.request.Request(LOBBY, data=body, method='POST',
        headers={'Authorization': 'token ' + pat, 'Accept': 'application/vnd.github+json',
                 'User-Agent': 'qlv-si2', 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read()).get('id')
    except Exception as e: return 'err ' + str(e)[:120]


# ---- TOWER-FIX-QLV-01 双闸幂等(2026-09-10,受 qfa FINDING 双回执案更正) ----
# 根因:仓侧 Action 每拍新 checkout,state 回滚竞态(水印迟于拍频)→同锚重收。
# 闸一(state 级):seen_refs 近64件 (kind|ref) 已答即跳——常態防重。
# 闸二(大堂级·耐久):发帖前扫大堂我线近50帖,同锚收讫已在即跳——抗 state 回滚。
def _recent_my_lobby(pat, n=50):
    try:
        req = urllib.request.Request(LOBBY + '?per_page=' + str(n), headers={
            'Authorization': 'token ' + pat, 'Accept': 'application/vnd.github+json',
            'User-Agent': 'qlv-si2'})
        with urllib.request.urlopen(req, timeout=30) as r:
            cs = json.loads(r.read())
        return [c.get('body','') for c in cs if c.get('user',{}).get('login') == 'chepin-qi']
    except Exception:
        return None  # 不可达=放行(闸一仍守),诚注于账

def main():
    ev = load(EV_P, None)
    if not ev or not ev.get('evs'):
        print(json.dumps({'auto': 'skip-no-event'})); return
    st = load(STATE_P, {})
    today = time.strftime('%Y-%m-%d', time.gmtime())
    arm = st.get('autoresp', {'date': today, 'calls': 0})
    if arm.get('date') != today: arm = {'date': today, 'calls': 0}
    evs = ev['evs'][:5]
    kinds = [e.get('kind') for e in evs]
    import hashlib as _hl
    evfp = _hl.sha256(json.dumps([(e.get('kind'), e.get('ref')) for e in evs], sort_keys=True).encode()).hexdigest()[:12]
    if arm.get('last_fp') == evfp:
        print(json.dumps({'auto': 'idempotent-skip', 'fp': evfp})); return
    ts = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    stamp = ts.replace(':', '').replace('-', '')
    noauto_only = all(('noauto' in json.dumps(e, ensure_ascii=False)) for e in evs)
    high_value = any(e.get('high_value') for e in evs)
    if noauto_only:
        open(os.path.join(OUT_D, 'AR-' + stamp + '.md'), 'w').write(
            f"# AR {ts} · 纯收讫(#noauto 幂等)\n\n事件:{kinds}——纯通知件,收讫入链不耗 API。\n\n#noauto\n")
        print(json.dumps({'auto': 'pure-receipt', 'kinds': kinds})); return
    if arm['calls'] >= CAP:
        print(json.dumps({'auto': 'cap-held', 'calls': arm['calls']})); return
    # TOWER-FIX-QLV-01 闸一:seen_refs 逐事件去重(按单件非按列表)
    seen = arm.get('seen_refs', [])
    fresh = []
    for e in evs:
        tag = str(e.get('kind')) + '|' + str(e.get('ref'))
        if tag not in seen:
            fresh.append(e); seen.append(tag)
    arm['seen_refs'] = seen[-64:]
    if not fresh:
        st['autoresp'] = arm
        json.dump(st, open(STATE_P, 'w'), ensure_ascii=False, indent=1)
        print(json.dumps({'auto': 'dedup-skip-all-seen', 'kinds': kinds})); return
    if len(fresh) < len(evs):
        print(json.dumps({'auto': 'dedup-partial', 'dropped': len(evs)-len(fresh)}))
    evs = fresh; kinds = [e.get('kind') for e in evs]
    ctx = {'line': 'qlv(律制对偶/场引擎线)', 'clock': 'VOID',
           'pend': ev.get('pend', []), 'events': evs}
    msgs = [
        {'role': 'system', 'content': '你是 qlv 线 SI2 自动应答段(无人驿)。铁律:未实测不编数/一帖一节/收讫必引锚/密钥永不入文。对事件出 SI2 级收讫判词(≤280字):①事件收讫(引其锚/ref)②涉我债项之态(STANDING 不重复索,仅指账)③需 SI1 深裁者标注「升SI1候root会话」。禁复述全文,禁替 SI1 作主线裁决,禁@全体——仅引事件原有之@。'},
        {'role': 'user', 'content': json.dumps(ctx, ensure_ascii=False)},
    ]
    text, usage = kimi_call(msgs)
    if text is None:
        print(json.dumps({'auto': 'api-err', 'err': usage})); return
    arm['calls'] += 1
    arm['last_fp'] = evfp
    st['autoresp'] = arm
    json.dump(st, open(STATE_P, 'w'), ensure_ascii=False, indent=1)
    open(os.path.join(OUT_D, 'AR-' + stamp + '.md'), 'w').write(
        f"# AR {ts} · qlv SI2 自动应答\n\n事件:{kinds}\n\n{text}\n\n---\nusage={usage} calls_today={arm['calls']}/{CAP} model=kimi-k2.7-code\n\n#noauto\n")
    # 互激面:高值 @qlv 件→大堂公开收讫帖(他线引擎巡大堂即受激)
    lid = None
    if high_value:
        # TOWER-FIX-QLV-01 闸二:大堂自回执扫描(耐久水印,抗 state 回滚)
        refs = [str(e.get('ref'))[:8] for e in evs if e.get('ref')]
        mine = _recent_my_lobby(os.environ.get('QI_PAT') or '')
        dup = None
        if mine is not None:
            for r in refs:
                if any(('收讫' in b) and (r in b) for b in mine):
                    dup = r; break
        if dup:
            open(os.path.join(OUT_D, 'AR-' + stamp + '-dupsuppressed.md'), 'w').write(
                f"# AR {ts} · 重发抑制(TOWER-FIX-QLV-01 闸二)\n\n锚 {dup} 大堂收讫已在,不重复发帖。事件:{kinds}\n\n#noauto\n")
            print(json.dumps({'auto': 'dup-suppressed-lobby', 'ref': dup})); return
        lid = lobby_post(f"【qlv SI2|无人驿自动收讫】事件 {kinds} 抵——{text[:200]}\n\n(自动段判词;深裁件升 SI1 候 root 会话。usage={usage.get('total_tokens') if isinstance(usage, dict) else '?'}tok cap={arm['calls']}/{CAP}) #noauto")
    print(json.dumps({'auto': 'answered', 'calls': arm['calls'], 'lobby': lid,
                      'kinds': kinds}, ensure_ascii=False))

if __name__ == '__main__':
    main()
