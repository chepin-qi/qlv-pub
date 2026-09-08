#!/usr/bin/env python3
# METER-CADENCE-01 实装 v0.2 —— 统一不等式判据入塔（数核⑤⑥工程化）
# 判据: JUMP ⟺ ρ(bin_ev,bin_dom)≥θ* ∧ n_eff≤c ∧ κ≠0 ∧ bin差≠0(同律保持非跃迁)
# clock=VOID; 数据皆实测/自算,未编一数
RHO={0:1.000,1:0.167,2:0.167,3:0.167,4:0.167,5:0.250,6:0.208,7:0.333,8:0.125,9:0.167,10:0.083,11:0.083}  # 数核⑥ N=24±15c
THETA=0.292  # 数核⑥: 五度/四度最大间隙中点(属/下属分界)
BINMAP={'relay-watch':0,'root-msg':1,'cisvr':2,'qfa.beat':3,'bridge':3,'heartbeat':3,
        'usrm':4,'lgt':4,'ucif2':4,'vinf':4,'lane.drop':5,'board.push':6,'face.reply':6,
        'beacon.comment':7,'quafu.transition':8,'dm-queue':9,'self-cascade':10,'selftest':10,'err':11}  # 格位表v0.1
C_CAP=2  # CRT 通道实例(数核⑤): Z12→Z4×Z3 后并行通道数
def bin_of(kind):
    if not kind: return None
    if kind in BINMAP: return BINMAP[kind]
    for k,v in BINMAP.items():
        if kind.startswith(k): return v
    return None
def dominant(win):
    from collections import Counter
    bs=[b for b in win if b is not None]
    return Counter(bs).most_common(1)[0][0] if bs else None
def judge(ev_kind, win_bins, hv=False):
    """win_bins: 滑动窗内事件 bin 序列(含本拍前)。返回 (verdict, rho, n_eff, kappa, bin_ev, bin_dom)"""
    b=bin_of(ev_kind); dom=dominant(win_bins)
    if b is None or dom is None: return ('进行式',None,None,None,b,dom)
    d=(b-dom)%12; rho=RHO[d]
    n_eff=len(set(x for x in win_bins if x is not None))
    kappa = hv or (b not in (10,))  # κ≠0 工程像: 跨线锚关联(高值或他线件); 纯自指(selftest/self-cascade)→κ=0
    if d==0: return ('保持',rho,n_eff,kappa,b,dom)  # 同律重复=保持,非跃迁
    if rho>=THETA and n_eff<=C_CAP and kappa: return ('跃迁',rho,n_eff,kappa,b,dom)
    return ('进行式',rho,n_eff,kappa,b,dom)
