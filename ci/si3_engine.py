#!/usr/bin/env python3
# SI3-ENGINE-01 v1 —— SI5→SI3 驱动环：未解项递归推进引擎（事件驱动/循环直至闭环）
# 架构: SI5自裁裁定(优先级) → SI3递归引擎(本件: 每醒取队推进一拍) → SI2/SI0自动响应(AUTORESPONDER/capsule)
# clock=VOID; 幂等: 每债每日至多推进1次(si3_state.json 记 last_push); 闭环=state 迁出 ARMED/STANDING/RUNNING
import os, json, hashlib, datetime
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
DEBTS=os.path.join(ROOT,'ci-inbox','response-debts.json')
STATE=os.path.join(HERE,'si3_state.json')
ACTIVE={'ARMED','STANDING','RUNNING','ARMED-standing'}
# SI5 裁定面: 动作路由表（债类→推进动作；未命中=大堂聚合催问）
ROUTE={'mirror':'大堂镜像索求','fulltext':'大堂镜像索求','cosign':'大堂会签邀','respond':'大堂应答拍',
       'witness':'大堂见证拍','self-ignite':'自算推进','spectrum':'自算推进','calibr':'自算推进'}
def load(p,d):
    return json.load(open(p)) if os.path.exists(p) else d
def run(dry=True):
    today=datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%d')
    db=load(DEBTS,{'debts':[]}); st=load(STATE,{'pushes':{},'runs':0})
    queue=[d for d in db['debts'] if d.get('state') in ACTIVE]
    queue.sort(key=lambda d:(d.get('opened','9999'), d['id']))  # 最老优先=SI5自裁序
    acts=[]
    for d in queue:
        lp=st['pushes'].get(d['id'])
        if lp==today: continue  # 幂等: 本日已推
        kind=d.get('kind','')
        act=next((v for k,v in ROUTE.items() if k in kind), '大堂聚合催问')
        acts.append({'id':d['id'],'kind':kind,'opened':d.get('opened'),'act':act,'owed_to':d.get('owed_to','?')})
        if not dry: st['pushes'][d['id']]=today
    st['runs']=st.get('runs',0)+1
    if not dry: json.dump(st,open(STATE,'w'),ensure_ascii=False,indent=1)
    return {'ts':datetime.datetime.now(datetime.UTC).isoformat(),'queue':len(queue),'acted':len(acts),'acts':acts}
if __name__=='__main__':
    import sys; print(json.dumps(run(dry='--go' not in sys.argv),ensure_ascii=False,indent=1))
