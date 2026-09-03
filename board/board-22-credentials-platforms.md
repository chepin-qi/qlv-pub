# board-22 · root 凭证下放：11 平台入 vault + 真机面纪律入典

**日期**：2026-09-04 ｜ **线**：qlv ｜ **类型**：资源台账（零密钥值）

---

## 一、凭证下放事件
root 直投 11 平台凭证/账号线索，全部入 `.vault/quantum/`（11 件），**铁律执行**：键值永不入仓/链/帖；真值探针 12 枚扫三仓 → **CLEAN 零泄漏**。
台账：`qlv_lab/registry/platforms.json`（PLATFORMS-REGISTRY-01，只记指针与状态）。

## 二、平台状态总览（零值）
| 平台 | 状态 | 角色 |
|---|---|---|
| 本源 originqc ×3+1 | U95099 机时尽 / foxmail 新键 / thai68 透支14.334s+60s / 1 键归属待定 | **最后手段**（一次性机时，单账号≤120s） |
| quafu 夸父 | root 重铸新键在 qlv vault，候验活；qfa 侧须 root 直投 | p=3 提交线（rm01 已 MATCH） |
| 天衍 tianyan | VALID（qfa rm02 实测） | **真机主路**：176/24 free/calibration 先行，paid 候 root 钱类闸 |
| quantumrings | 下放未验（128bit-30天/64bit，64 两键同值在案） | 模拟器主用 |
| openquantum / 腾讯 / IBM | 下放未验 | 备用面 |
| fieldqkit | 统一接口包（7 家） | 候选集成层 |
| 国盾 / Bluequbit | 仅链接无键 | 候补 |

## 三、root 纪律入典（真机面五律）
1. 本源机时极紧缺：他平台尽量完成实验与预研，非用不可才用本源
2. 使用前充分准备：了解参数与规则，充分规划设计
3. 实验电路均经仿真预验；单次提交、零重试，绝不浪耗资台机时
4. 真机/钱类一律 root 闸，提交令须 root 明示
5. 密钥永不跨线；线路跨线（QASM sha256 锚定互验）

## 四、当前真机面就绪度
- 线路：qfa p=3 12q（qaoa_p3.qasm）双线验真（qfa 天衍云 12000 shots ALL PASS + qlv QASM 直执 P_opt 差 1.67e-16）
- 独立闸：qlv `qasm_xexec.py` 就绪（提交前最后一道独立验）
- 路径：天衍 free/calibration 机 → 候 root 提交令
- 通报：qfa inbox CRED-01 卡已投（qfa 主线 d78e6c2）
