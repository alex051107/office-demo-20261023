# 电力监管：Powercor 2020 资本支出调节 — 题包

## 任务与交付物

Results 必需表及支持计算，答案工作簿。

`solution/golden/answer.xlsx`、`solution/golden_output/answer.xlsx`、输入、评分器及离线正负例。

## 当前评分

版本标签：评分器 v2（2026-10-26）；此日期为评分版本标签，不是本次整理的执行日期。

正项按正确度计入，负项按违规程度扣除；负项不进入分母。令 `pooled = clip((Σ(w×正确度) − Σ(|负权重|×违规程度)) / 30, 0, 1)`，`reward = round(min(pooled, 所有已触发规则的上限), 6)`；无触发规则时上限为 1，通过线为 0.70。

- Results 缺失或错名：gate = 0。
- 必需前置表头不符，或来源/支持格空白或纯数字、单位不符、额外业务记录：对应 cap = 0.69。允许合法后附列、空白样式列和自由支持表。
- 行序、重复记录、数值、精度及其他负项按现有判据处理；精度为显示或存值合规，数值容差另算。具体项、权重、舍入和文字/程序分工见 [评分口径](validation/scoring_policy.md)。

| 答卷 | 当前记录 | 裁判状态 |
|---|---:|---|
| 金标 | 程序分 1.000000；混合总分不可用 | 有效新判定 0/5；`NO_VALID_NEW_JUDGMENT` |
| GPT-5.6-SOL | 0.000000 | 沿用已保存判定；未重新裁判 |
| Claude Opus 4.8 | 0.000000 | 沿用已保存判定；未重新裁判 |
| Qwen3.8 Max | 0.000000 | 沿用已保存判定；未重新裁判 |

金标 `reward.json` 中的 0 是裁判错误占位值，伴随 `verifier_error=1`、`score_available=false`，不是答卷零分。历史暂定 1.0、旧五次重复以及无效尝试均留在 `history/`，不作为当前分数或一致性验收；有效样本不足，标准差不可计算。未进行八次独立求解，不提供 pass@8。

## 离线复现

需要 Python 3.11+ 和已安装的 openpyxl；不需要服务凭据。将配套轨迹报告与题包并列放置，用于核对已保存的分数与判定状态。

在本目录执行：

```sh
python3 -B validation/run_regression.py
python3 -B validation/validate_paths.py
```

回归涵盖 24 个负例、13 个正例，以及池化、候选文件访问校验和已保存报告；只做离线验证，不启动求解或裁判，不修改交付文件。配套目录不在默认位置时，`run_regression.py --trajectory 轨迹报告根目录`。

历次变更与原交付说明见 [历史变更记录](history/CHANGELOG.md)，归档分组见 [历史目录说明](history/README.md)。
