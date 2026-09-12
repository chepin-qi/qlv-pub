#!/usr/bin/env python3
# SCAN-OWN-KEYS-01 · qlv 自钥扫闸 v1.1（采 qfa GUIDE 片段派生式 + 泛型模式）
# 律:①凡出文必先扫 ②自钥片段运行时派生永不落仓 ③泛型并行 ④闸在写路径
import hashlib, re, sys, os, json
GENERIC=[r'ghp_[A-Za-z0-9]{30,}',r'gho_[A-Za-z0-9]{30,}',r'ghs_[A-Za-z0-9]{30,}',
         r'ghu_[A-Za-z0-9]{30,}',r'github_pat_[A-Za-z0-9_]{30,}',r'sk-[A-Za-z0-9]{20,}',r'AKID[A-Za-z0-9]{13,}']
def scan_out(text, keys, n=8):
    for k in keys:
        if not k: continue
        for f in (k[:n], k[-n:], hashlib.sha256(k.encode()).hexdigest()[:n]):
            if f and f in text: return 'BLOCK: own-key fragment'
    for p in GENERIC:
        if re.search(p, text): return 'BLOCK: generic ' + p[:6]
    return None
def keys_from_env():
    return [os.environ.get(x,'') for x in ('QI_PAT','FED_PAT','AI_FULL_PAT','CI_OPS_LINE_KEY')]
if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv)>1 else '.'
    keys = keys_from_env(); bad = 0
    for dp, dn, fn in os.walk(root):
        if '.git' in dp.split(os.sep): continue
        for f in fn:
            p = os.path.join(dp, f)
            try: t = open(p, encoding='utf-8', errors='ignore').read()
            except Exception: continue
            r = scan_out(t, keys)
            if r: print('SCAN-BLOCK', os.path.relpath(p, root), r); bad += 1
    print('SCAN-OWN-KEYS-01', 'FAIL %d' % bad if bad else 'PASS')
    sys.exit(1 if bad else 0)
