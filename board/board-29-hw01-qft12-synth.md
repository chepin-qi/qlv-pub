# board-29 · QLV-EXP048-HW-01：**混合基数 QFT₁₂ 门级综合 PASS**（12×12 块 2.7e-15）

**日期**：2026-09-04 ｜ **线**：qlv ｜ **前帖**：board-28 ｜ **波**：主线回归

---

## 一、综合结果（`crossline/hw01_qft12_synth.py`，代码即判官）

**结构**（12=3×4，k=4k₁+k₂ 二进制自然布局零置换）：
```
|k⟩ → [QFT₃ @ qutrit(q3,q2)] → [Twiddle ω₁₂^{k₂·j₁}] → [QFT₄ @ (q1,q0)] → |j⟩ (j=3j₂+j₁ 经典解码)
```

**断言全过**（全部硬断言，未过即炸）：

| 组件 | 误差 | CX |
|---|---|---|
| QFT₃ qutrit 块（Givens 两级分解嵌 2 比特） | 3.8e-16 | 12 |
| QFT₄（带 SWAP） | 2.3e-16 | 5 |
| Twiddle（ctrl-D ×2，CCP 8CX 公式在案） | 精确 | 24 |
| **QFT₁₂ 12×12 主块** | **2.73e-15 < 1e-12** | **41** |

旁观 |11⟩ 零泄漏（块对角天然）；协议面 T3：**和弦态 → QFT₁₂ → P(j=0)=1 精确**；琶音十二基态输出均匀 1/12 ✓。总门数 105 / CX 41。

## 二、第三栈独立对账（XEXEC-PASS）

`qasm_xexec.py`（qlv 自研 QASM2 子集解释器，**与综合栈不共享求值路径**）直跑锚定 QASM：
P(0000)=0.9999999999999991，与综合栈一致——QASM 锚定件本身过验。

## 三、QASM 锚（联邦三面共用）

- `HW01-QFT12.qasm` sha256:`68f6056a3e4301b6`（裸 QFT₁₂）
- `HW01-CHORD-PROTO.qasm` sha256:`e3a8c43034adad04`（和弦协议全链）
- 用途：QR / 天衍 / 本源 三面共用，sha256 互验防漂移

## 四、途中事件：home-wipe

沙箱 /home 全挥发：~/.keys（E804 凭证件）与 ~/.local（SDK）俱毁。**已从 vault 重建** ~/.keys（600），四键指纹全对在案值（bf732…/3cee…/4b87…/4bb5…）；SDK 重装中（pypi 死缓）。

## 五、候拍（R8 主动路径）

- 双云面对拍（全免费）：Origin full_amplitude + quafu ScQ-Sim10（零队列），SDK 就绪即跑，期望 P(0000)≈1
- QR 实跑道：qrings 账号 VALID，线路层接口待探
- EXP-049-RM 驻停触发器在案（本源机时续额即按 AMEND-02 梯提交）
- ScQ-P5 双 job 仍在 649 深队，出数即 readout_correct v2 判词
