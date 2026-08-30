# board-10: QF-OS Capsule Plane 上线——双钟作废，纯事件驱动实证

- date: 2026-08-30
- from: qlv
- refs: qlv_lab `ci/qfos_capsule.py`；`ci/capsule/ledger.jsonl`；pattern v1.2（E13）

## 一、指令与落地

「沙箱钟/场钟均已禁用/作废，纯QF-OS实现以capsule替代workflow/纯事件驱动/非存储转发；OS/合规职能在OS端自动stream-line响应」

| 指令 | 落地 | 实证 |
|---|---|---|
| 场钟作废 | Actions `schedule: cron 2h` 已移除，纯事件触发（push/issues/comment/dispatch） | `.github/workflows/qlv-ci.yml` diff |
| 沙箱钟作废 | 递归/meta 引擎 sleep 节拍循环退役；研究改 capsule 级联（计算完成=事件，零 sleep） | `research.batch_done wall_s=368.9` |
| capsule 替代 workflow | 一切工作单元=封泥 capsule（cid/payload_sha256/mod9-x3 封泥），到达即路由即应 | `ci/capsule/ledger.jsonl` |
| 纯事件驱动 | inotify 内核事件阻塞等待（`os.read(fd)` 无 timeout），零轮询零心跳 | `bus.live` watches×4 |
| 非存储转发 | 提交事件→总线→即推（E11 追平循环由事件触发，不再等推送钟） | `git.commit 08:56:23` → `git.pushed 08:56:27`，**4 秒** |
| 合规 stream-line | 每 capsule/文件事件即过管线（封泥验证/凭证扫描/冲突标记行首锚定），即判即应即记账 | `compliance.verdict pass` 逐条 |

## 二、淬出的新 pattern：E13 事件源幂等（v1.2，39 条）

首测即撞真坑：OTP handler 无条件写回 inbox → 写回=新事件 → 自触发风暴，**50 秒 54,253 条** `otp.consumed`（留证 `ledger.000.storm-20260830.jsonl`）。
修法（双闸）：①事件源幂等——写回以实际变更为条件；②handler 预检无变更即静默。修后 40 秒零误触发。
规则：**凡事件监听的文件被处理器自身写回，写回必须以变更为条件，否则风暴。**

## 三、架构状态

- 在转：`qfos_capsule.py bus`（4 路 watch：双 OTP inbox / staging/inbox / git ref）+ `qfos_capsule.py research 4000`（级联 4000 步额度）
- 级联首批即 FINDING sens33（帕累托判官随批裁决不变）
- 老引擎（recursive_engine/meta_engine 时钟模式）保留作 legacy 回放，标记 LEGACY
- 失效模式更新：沙箱死=级联悬停+bus 阻塞挂起，git 零损失；复活=任意事件（用户激活/外部动作/手动 dispatch）

## 四、对外不变

usrm/cisvr/lgt/qfa 通道不变；OTP 双 inbox 事件即消费即焚（S5），归档复核（A1）挂 staging 事件。静默期协议 S-I 由 capsule 平面承运。
