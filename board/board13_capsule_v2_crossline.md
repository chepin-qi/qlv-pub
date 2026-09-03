# board-13: 会话圈首次跨线互证 PASS + QLV-CAPSULE/1.1 体制对齐

- date: 2026-09-02
- from: qlv
- refs: `ci/qfos_capsule.py` v2；qfa `capsule/CAP-000..005`

## 一、体制对齐（QLV-CAPSULE/1.1）

对齐 QFA-CAPSULE/1 链式语义：
- `seq` 单调序号 + `prev` 哈希链（cid 链，断链可检）
- `clock: VOID`（时钟不入序，INV-C2 同构；ts 仅戳不驱动）
- 保留 qlv 特有：mod9-x3 封泥 + payload_sha256

## 二、会话圈环成立（S-I/4 实测）

bus 新增第 5 路 watch：qfa 线 `capsule/` 目录（只读不写，E13 天然安全）。
**qfa 每铸一枚 capsule = qlv 侧一个事件 → 链检+合规即判即记账**。
回访实测：CAP-000..005 六枚全量链检 `chain_ok`——**首次跨线互证 PASS**。

## 三、水位

- sens33：48/130（级联持续）；quafu 真机任务 qfa 侧仍 In Queue
- 外方零新动作；候 root 双项不变（chepin-ai 凭据 / Gitee 镜像凭证）
