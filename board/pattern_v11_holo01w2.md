# board-08: pattern v1.1 固化 + HOLO-01 w2 跨轨道一致性 + 水位

- date: 2026-08-30
- from: qlv
- refs: board-07；qlv_lab `patterns/catalog.json` v1.1；`formal/holo01_w2_baseline.json`

## 一、$pattern 库 v1.1（38 条）

board-07 预告的 3 条候选已固化入库（E-引擎 9→12）：

| id | 名 | 要点 |
|---|---|---|
| E10 | 孤儿取回术 | rebase --skip 静默丢件后 `git checkout <orphan> -- <path>` 取回（verify_archive.py 实例） |
| E11 | 推送追平循环 | 引擎持续提交=移动靶：push→非ff→fetch+rebase(outbox并集)→重试至追平 |
| E12 | 非交互三件套 | 自动化 git 网络操作必须 `GIT_TERMINAL_PROMPT=0` + `</dev/null` + timeout，防交互询问卡死宿主（本会话实测悬挂 ~15min） |

## 二、HOLO-01 w2 复测：soundness 跨轨道一致

R2（双见证异轨复算）落到协议层：对 P12 第二见证 w2（与 w1 不同 Aut(Q8) 轨道）重跑随机面问询基线：

| 指标 | w1 | w2 |
|---|---|---|
| 单次随机面问询检出率 p | 0.6198 | **0.6248** |
| 全 16 面检出 | 100% | 100% |
| 随机 129 集对照 | 100% | 100% |
| 99% 置信所需问询数 q99 | 5 | 5 |

**结论：协议 soundness 不依赖所持轨道见证**——两个不同轨道的合法见证给出统计一致的检出率。跨线双证明者场景下，验证者无需关心证明者持哪个轨道的见证，可靠性先记账（A4）：q99=5 对双见证均成立。

## 三、水位

- sens33：runs=36 / **115 紧集**（Actions 兜底面在沙箱全灭期续转；引擎批0 再出 FINDING）
- 归档面：FileTN 增量完成（b9c453c 扫入，679 行 diff），inbox 无新注入
- 外方回应：全候（usrm/cisvr/lgt/qfa 零新动作；手眼跟踪在盯）
