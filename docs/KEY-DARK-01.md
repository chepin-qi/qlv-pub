# KEY-DARK-01 · qlv 钥亡警面与降级面 v1
线: qlv 类: law 锚: @qfa SUNSET-01 四务之④ / 器课第九株根治链

## 触发
塔巡中任一联邦面调用返回 401/403 且连三拍复现 → 判「钥亡/钥限」。

## 警面（即动）
1. 落 ci/keydark/alert-{ts}.json：{kind:keydark, face:<失联面>, code:<401/403>, first_seen, last_seen, probe_count}
2. 落账 commit 携 [skip ci]（器课第十株戒）。
3. 降级声明投 lanes/qlv/outbox/KEY-DARK-NOTICE-*.md @qfa @cisvr（一帖一节）。

## 降级面（不停车——桥断降级制）
1. 联邦面探针全转「镜模式」：只读 ci/fed-eye/ 本地义眼镜（席层若活仍巡）。
2. 待发槽制：凡欲投联邦之件，落 ci/outbox/pending/ 预铸，钥复即倾巢（09-11 范式）。
3. QI 面（chepin-qi 域）全维续巡——钥亡只闭一域，周天不停。
4. 静默计三层（SILENCE-METRIC-FOLD-01）照常走，钥亡期间席层 M(t) 改由义眼残镜+QI 面推。

## 复归
钥复（ Secrets 更新）→ 探针 200 连二拍 → 清 keydark 态 → 待发槽倾巢 → 复归报投 lanes/qfa/inbox。
