#!/usr/bin/env python3
"""qlv-lib 侧工单轮询执行器（在 chepin-ai/qlv-lib Actions 内运行，持 AI_FULL_* secrets）"""
import json, os, subprocess, sys, hashlib, time, base64, urllib.request

PUB_REPO = "https://raw.githubusercontent.com/chepin-qi/qlv-pub/main"
ALLOWED = {"cred_selftest", "repo_mirror", "dispatch", "fetch_publish", "sealed_exec"}

def fetch(path):
    with urllib.request.urlopen(f"{PUB_REPO}/{path}", timeout=30) as r:
        return r.read()

def verify_sig(doc_bytes, sig_b64):
    # 验签：公钥取自 CAP-QLV-PK-0001.json（同仓公开件）
    cap = json.loads(fetch("CAP-QLV-PK-0001.json"))
    pub_line = cap["identity"]["ed25519_pub"]
    with open("/tmp/qlv_allowed", "w") as f:
        f.write(f"qlv-line@chepin-qi ssh-ed25519 {pub_line.split()[1]}\n")
    open("/tmp/wo_msg", "wb").write(doc_bytes)
    open("/tmp/wo_sig", "wb").write(base64.b64decode(sig_b64))
    r = subprocess.run(["ssh-keygen", "-Y", "verify", "-f", "/tmp/qlv_allowed",
                        "-I", "qlv-line@chepin-qi", "-n", "qlv-chain",
                        "-s", "/tmp/wo_sig"], stdin=open("/tmp/wo_msg", "rb"),
                       capture_output=True)
    return r.returncode == 0

def exec_wo(wo):
    t = wo["type"]
    if t == "cred_selftest":
        names = ["AI_FULL_PAT", "AI_FULL_APP_ID", "AI_FULL_APP_KEY",
                 "OTP_PHONE", "OTP_EMAIL1", "OTP_EMAIL2"]
        return {n: ("present" if os.environ.get(n) else "MISSING") for n in names}
    return {"status": "skipped", "reason": f"type {t} 未在本版实现"}

def main():
    idx = json.loads(fetch("workorders/index.json"))
    for woid in idx["open"]:
        raw = fetch(f"workorders/{woid}.json")
        wo = json.loads(raw)
        assert wo["type"] in ALLOWED, "类型不在白名单"
        body = {k: v for k, v in wo.items() if k != "sig_b64"}
        canon = json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        if not verify_sig(canon.encode(), wo["sig_b64"]):
            print(f"{woid}: 验签失败，拒执"); continue
        result = exec_wo(wo)
        receipt = {"wo_id": woid, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   "result": result, "artifact_sha256": hashlib.sha256(
                       json.dumps(result, sort_keys=True).encode()).hexdigest()[:16]}
        print(json.dumps(receipt, ensure_ascii=False))
        # 回执写入（由调用方 workflow 负责 git push 到 receipts/）

if __name__ == "__main__":
    main()
