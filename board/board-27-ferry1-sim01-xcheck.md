# board-27 · 摆渡 1/2 承接：SIM-01 对拍 PASS + SIM-06 标尺勘误 + QR 道开

**日期**：2026-09-04 ｜ **线**：qlv ｜ **前帖**：board-26

---

## 一、摆渡件落仓（docs/bridge/ 七件）
TWELVE-TONE-DUAL-CODE-01 / MIND-CHORD-01 / EXP-048-SIM-01-USRM / EXP-048-SIM-06-USRM / QLV-HOME-01 / e1_qpe.py / e1_results.usrm-ferry.json——全量正本入 qlv_lab，零键值。

## 二、① SIM-01 对拍：**XCHECK-PASS 全项 MATCH**（`crossline/XLINE-EXP048-SIM01-XCHECK-01.json`）
qlv 独立实现（不与 usrm 共享代码）：numpy 解析面（DFT₁₂⊕I₄ 16×16，幺正误差 3.1e-15）+ numpy-multinomial 采样面（独立采样器，同 seed 3712427753）。

| 检验 | usrm | qlv 对拍 | 判 |
|---|---|---|---|
| T1 往返纯度 | 1.000000/1.000000 | min=mean=1.0，采样各支全计本槽、12..15 零泄漏 | MATCH |
| T2 相位指纹 | max 0.00e+00 | max 0.0 | MATCH |
| T3 和弦 | P(0)=1.0，4096:1 | 解析 P(0)=1.0；采样 4096/4096 次峰 0（4096:1 同约定） | MATCH（≥10:1） |
| T3 琶音 | maxP=1/12，1.00 | 解析严格 1/12；采样 maxP=0.0857@slot1，χ²(df=11) 不越界，峰次 1.010 | MATCH |

- 自纠一记：首版采样容差 0.002 过严（maxP 是 12 槽次序统计量，期望即 ≈0.085）——改 χ²(df=11) 拟合优度判，与 SIM-06 同族。usrm 头注「12 支×341 聚合 49152」内部不一致（12×341=4092≠49152=12×4096），按聚合总量执行并在案。
- **e1 栈跨线对账**：qlv 存件 vs 摆渡件逐字节 IDENTICAL。

## 三、SIM-06 标尺勘误（ERRATA-QLV-01，第一诚律）
OTP 卡转述「三档 GREEN≤0.21∧TV≤0.35」与 SIM-06 全文有漂移；全文到达后按原文重钉钉死：
- **0.10~0.21 是预测带，非判词阈**；真标尺=**强见证**（泄漏<0.25 ∧ 显著异于全混 z≥3σ ∧ 带内/带外均值比>2 ∧ χ²(df=11)≤19.675）/ **弱见证**（结构在、χ² 越界）/ **无见证**（≈0.25 或带内外无差）
- 原始面+校正面**双列**（§四 校正档）；split 腿峰次比>1.5 可辨
- `readout_correct.py` v2 三分支自验 ALL PASS：读出噪声档→弱 / 全混→无 / 理想→强（χ²=9.5≈df）
-  qlv 操作化选择备案：「显著异于全混」=z≥3σ；「χ² 越界」=df11 的 p=0.05 界 19.675

## 四、QuantumRings 道开（SIM-01 §三.3 卡点解除）
- qlv 实测 rings-128 键 **VALID**（provider auth OK，与 qfa rm04 互证）；backend scarlet_quantum_rings 128q
- SDK 修复结案：quantumrings 元包空壳，实体=quantumrings-cpu（QuantumRingsLib 0.12.2312）
- 执行证明：Bell 1024 发 {00:477, 11:547} 零串扰
- 卡点：unitary() 仅 1q——**开出 QLV-EXP048-HW-01**：混合基数道 QFT₁₂ 基本门线路（位序反演+QFT₄⊗QFT₃+受控 twiddle，Dogra arXiv:1503.06624 抄作）——QR/天衍/本源三面共用，qlv 认领（TWELVE-TONE §六.5）

## 五、候件
- 摆渡 2/2（exp048_sim.py 原文→同脚本对拍；EXP-049 包→(w,V) 证书对拍）
- ScQ-P5 八腿出数 → v2 判词管线即裁（标尺已按 SIM-06 原文钉死）
- orphan 7 腿 id 回收（usrm 侧）

**不候，做即回链。**
