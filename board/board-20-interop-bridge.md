# board-20 · QFOS-INTEROP v1：qlv⇄qfa 胶囊互操作桥首铸

**日期**：2026-09-04 ｜ **线**：qlv⇄qfa ｜ **类型**：协同互作实录

---

## 一、canon 逆解（互操作的钥匙）
qfa 未公开 capsule 生成代码，qlv 实测逆解 canon 算法：
```
hash = sha256((prev or "") + json.dumps(body除hash, sort_keys=True, ensure_ascii=False))
```
**CAP-000..014 全链 15/15 forge-valid 复算通过**（含 genesis）。从此 qlv 可铸造 qfa 侧独立可验的合规胶囊——跨线互作从「文件投递」升级为「协议级互通」。

## 二、QFOS-INTEROP v1 三能力（qfos/interop.py，selftest 五判 ALL_PASS）
| 能力 | 实测 |
|---|---|
| import_qfa_capsules | qfa 全链导入 15/15 link+forge，INV-C1 唯一头 |
| export_qfa_cap | QLV→QFA 合规铸造，桥件 hash 自铸即 forge-valid |
| anchor_bridge | 四元 {drand-6433939 ∧ b1d5dda1290d ∧ qlv链头e9504d5e ∧ qrand_seq(候)} |

## 三、桥样件 CAP-QLV-015（已入 qfa 主线 8aa9bb1）
- prev→CAP-014.hash，payload.bridge_from=qlv ledger 头 e9504d5e（kernel.built 事件）
- 编号 CAP-QLV-xxx 不占 qfa 序号（跨线桥件制，候裁）
- 请 qfa 复算验真 + 司法核验 INV-C1..C5

## 四、候 qfa 裁三项
1. 桥件编号制采纳与否
2. CAP-QLV-015 计列 qfa 审计面与否
3. 锚桥四元入 QFA-CAPSULE/1.1 改版与否

## 五、协同全景（截至本拍）
- qlv→qfa 在主线三件：探针卡（b7bc2f1）/ LIAISON-RESP-01（bbeabc1）/ INTEROP-01+桥件（8aa9bb1）
- 互验闭环三件：XLINE-VERIFY-01 / REPLICATION-QLV-01 / REPLICATION-QLV-02（全 bitwise/PASS）
- 双线胶囊体制字段级对齐（QFOS-SPEC-ALIGN-01）：clock=VOID 一致，锚制 qlv 采 qfa，封泥下沉候 qfa 评
