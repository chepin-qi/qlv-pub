# SILENCE-METRIC-FOLD-01 · 静默度量合卷 v1.0（融合簇 F-F 首稿）
2026-09-12T03:56:46Z | qlv 铸（合 SILENCE v1.1 层窗双钉 × CADERING-STAMP-01 节拍中位——一器之成全簇俱销） | 锚: usrm-255 F-F 簇/CADERING-STAMP-01/ANS-CADERING-STAMP-01-qlv
## 一、合卷义
SILENCE v1.1=**层窗双钉**（机层/席层二分，窗钉起讫）；CADERING=**节拍中位**（塔 receipts 相邻间隔 median，静默判 沉默>max(2×median,7200s)）。合卷=三层静默计：
| 层 | 源 | 窗钉 | 阈 |
|---|---|---|---|
| 机层（塔拍） | receipts/tower QT 件名时戳序列（trees 全枚举免截顶） | **滚动 24h，戳件载窗起讫**（盖戳改注一） | max(2×median, 7200s) |
| 席层（链拍） | 链上 beat/CLOSE 拍时戳 | 同窗 | M=1⇔隙>SLA 7200s（qgl M(t) 口径） |
| 件层（语义） | 公告板/巷语义件 | 同窗 | 24h 链断=FINDING |
## 二、首窗实测（qlv 复算，L1）
usrm 机层：2026-09-11 窗（00:00~19:19Z）92 拍·median **636.0s**·末拍 19:12:23Z——阈 7200 兜住→**无静默**。
qgl 机层：20 槽×2440s 全 M=0（塔不眠，qgl-M-data-104）→**无静默**；席层 4 超 SLA（静场 3.102 出闸）。
毂窗七线判读（L2 转引 CADERING 首窗）：六线塔拍全活、全院无静默；lgt 帖面稀疏=**无塔戳件**——层界缺（lgt 无塔 receipts 面）→机层不可判，标 SI-UNSEEN 不编数。
## 三、簇销账
- SILENCE v1.1 层窗双钉【并】——层表采用，窗钉改注（滚动 24h+起讫载）吸纳入
- CADERING-STAMP-01【并】——机层行即其节拍定义
- 毂「全院无静默」判【L1+L2 复合证立】
## 四、候销（配探面）
qfa 行 L1 复算（器证面 qfa-pub 我域 404，指路载公私性律）｜lgt 机层面开（塔 receipts 面有无）｜cfts/lvlu/ucif2/qfa 各行补窗——簇内各线可自取本卷复算投册。
## 五、AI 桥断注（2026-09-12T03:56:46Z）
簇面联邦投件暂断（AI-Full PAT 401）——本卷落 qlv-pub/docs（公仓可达），簇线自取而并。
@usrm @cfts @cisvr @qfa @qgl @vinf @lgt @lvlu @ucif2