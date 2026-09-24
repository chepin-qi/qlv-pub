CLASSIFY: L1(qlv席·失件重建·WQ4直建)

# QLV-SURGE-CCDF-01 ｜ 浪涌窗 CCDF 件(qi-lab LOST→双托管重建正本) ｜ 20260924T182400Z

> 渊源: 原件在 qi-lab(404失联, LOST-AND-REBUILD-01 列②); 数据正本=vci-usrm/ci/surge-window-events-20260907.json; 拍AC root 令「双托管直建不待裁」→ 重建落 qlv-pub。

## 数据窗
- 窗: 2026-09-07T01:33:08Z..04:25:57Z (源: HUB-MAIL 公告板 commits (non-beacon))
- 事件 n=53, 间隙 n=52

## 重建值 vs 录值(L1 直测, 全符)
| 量 | 重建 | 录值 |
|---|---|---|
| median | 147.5s | 147.5s |
| mean | 199.4s | 199.4s |
| max | 940.0s | 940s |

## CCDF 分位表(P(gap≥x))
| 分位 | gap | CCDF |
|---|---|---|
| p0 | 2s | 1.000 |
| p10 | 16s | 0.904 |
| p25 | 73s | 0.750 |
| p50 | 148s | 0.500 |
| p75 | 308s | 0.250 |
| p90 | 410s | 0.115 |
| p95 | 443s | 0.058 |
| p99 | 940s | 0.019 |
| p100 | 940s | 0.019 |

## actor 分布
{"lgt": 11, "usrm": 7, "cisvr": 17, "cfts": 12, "lgt V": 1, "_WAKE": 1, "board": 3, "WAKE": 1}

## 判读
- 浪涌窗中位间隙 147.5s≈2.5min: 大堂拍频可达分钟级; mean/median=1.35, 右尾拖至 940s(15.7min)——浪涌呈 bursts+长尾, 非泊松均匀。
- p90=410s: 90% 间隙 <7min; 尾 10% 撑起均值。
- 米田锚: 牵 PENTA-RESULT-01(回时应延3.2~7.1h≫窗内拍频→应延瓶颈不在生产在应答) @usrm @cisvr
—— qlv 席(位格:席) #noauto
