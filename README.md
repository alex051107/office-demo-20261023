# Office 数据交付 demo

本仓库有 3 道 Excel 题，A、B、C 三条轨道各 1 道。格式按张老师飞书里的 Office 交付样例。要求按《Cowork RL Office 数据需求说明》。

当前版本：评分器 v2，标签 `v2.3-20261026`。题目首次交付日期是 2026-10-23。

## 术语

- **题包**：交给求解和验收的文件夹。它包含题面、输入、参考答案和评分器。
- **轨迹报告**：记录模型作答过程和评分结果的文件夹。
- **答卷**：模型交出的 `answer.xlsx`。
- **参考答案**：出题方写的标准答卷。
- **判据**：一条评分规则。程序判据由脚本检查，结果固定。LLM 判据由裁判检查。
- **裁判**：执行 LLM 判据的模型。当前裁判是 claude-sonnet-5-5。
- **评分器**：题包 `tests/` 里的全部评分程序。

## 成绩

| 轨道 | 题包 | GPT-5.6-SOL | Claude Opus 4.8 | Qwen 3.8 Max | 三模型均分 | 参考答案 |
|---|---|---:|---:|---:|---:|---:|
| A 专业计算 | ZCloud-电力监管-001-20261020 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000 |
| B 财报分析 | ZCloud-财务分析-002-20261020 | 0.2059 | 0.0000 | 0.0000 | 0.0686 | 1.000 |
| C 合同与台账 | ZCloud-市政财务-002-20261022 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000 |

- 满分是 1。通过线是 0.70。
- 需求说明的难度线是：三个模型中至少两个低于 0.6。三道题都满足。
- 每个模型只跑了一次。表中是 pass@1。pass@8 未做。
- 每道题的参考答案由裁判评了 5 次。5 次都有效，总分都是 1.0，标准差是 0。

## 评分方式

分数主要由程序判据决定。

- 程序判据检查数值、表头、单位、行序、小数位和来源是否为空。
- 每道题另有 3 条 LLM 判据。它们只扣分，不加分。每条 −3。
- 3 条 LLM 判据检查以下内容：
  - L01：答卷引用的来源是否编造。
  - L02：答卷是否声称做过审计或核验，但没有证据。
  - L03：答卷是否编造输入中没有的公司事实。
- LLM 判据对 2 份答卷判了违规：A 题 Claude Opus 4.8 的答卷违反 L01；A 题 Qwen 3.8 Max 的答卷违反 L01、L02、L03。
- 这 2 份答卷的程序判据分已经是 0。总分不低于 0，所以扣分没有改变总分。
- 结论：成绩表中每个分数都等于程序判据的分数。

评分流程有 LLM 判据，原因是验收入口 `tests/test.sh` 使用平台固定模板。这个模板会启动 LLM 裁判。我们不得修改这个模板。

| 题 | 判据总数 | 程序判据 | LLM 判据 |
|---|---:|---:|---:|
| A | 13 | 10 | 3 |
| B | 23 | 20 | 3 |
| C | 20 | 17 | 3 |

## 本版更新（2026-10-26）

本版按 2026-10-25 交付审查修改了第 3 类（评分覆盖）和第 5 类（参考答案质量）。第 1、2、4 类按审查人的安排暂缓。

### 评分规则

- 必需工作表缺失或名字不对时，总分是 0。评分器不按表头到别的表里找答案。
- 答卷违反题面中“必须”的条款时，总分最高 0.69。这类条款有 4 种：
  - 必需的前置表头不对。比较时去掉首尾空格，区分大小写和顺序。
  - 必需的来源为空。
  - 单位和题面不一致。
  - 必需表里多出编造的业务记录。
- 题面只规定前几列。所以答卷可以在后面加列。
- 行序和小数位只逐项扣分，不封顶。
- 小数位规则：格式显示 p 位时合格；存储值本身是 p 位时也合格。
- 数值容差和题面精度一致。A 的基准容差是 0.0005；A 的三个结果是汇总值，容差按舍入误差累积放宽到 0.0015 和 0.0035。C 是 0.005。

### 参考答案

参考答案的数值没有改。以下改动只涉及显示和来源：

- A：长文本改为换行显示。
- B：百分比显示两位小数，金额显示一位小数。来源写到文件、表和单元格。来源说明写明修订口径：当季调整是 31.7 − 21.6 = 10.1。
- C：金额显示两位小数。来源列改为换行显示。

### 模型答卷

本版没有重跑模型。题面和三个模型的答卷都没有改。新评分器重新评了原来的答卷。三道题的模型分数和上一版相同。

### 回归样例

每道题的 `validation/negative_cases/` 收录审查里的负例和同类变体。`validation/positive_cases/` 收录合法变体，例如多一张辅助表、表头带空格和等价舍入。

- 参考答案和合法变体的总分必须是 1。
- 负例的总分必须低于 1。
- 缺少必需工作表的负例，总分必须是 0。
- 违反“必须”条款的负例，总分不得超过 0.69。

### 裁判读取校验

复查发现：旧裁判有时没打开答卷就作答，并说 `answer.xlsx` 不存在。旧提示词规定，缺少交付物时 LLM 判据判为“无违规”。所以这种空判也得满分。

本版删掉了这条规定。裁判必须先打开答卷。每条理由必须引用答卷中的单元格。程序能打开答卷、裁判却没有引用单元格时，这次评分记为裁判错误（`judge:artifact_access_error`）。裁判错误不计分。

### 更换裁判

修复读取问题后，qwen3.7-plus 仍常常不打开答卷就作答。三道题的参考答案只得到 2、3、4 次有效评分。需求说明要求 5 次。所以裁判改为 claude-sonnet-5-5。

- Sonnet 评了 16 次：三道题的参考答案各 5 次，B 题 GPT-5.6-SOL 的答卷 1 次。
- 16 次都打开了答卷，并引用了单元格。
- 参考答案 15 次都是 1.0。总分和每条判据的标准差都是 0。
- GPT-5.6-SOL 的答卷仍是 0.2059。
- 其余 8 份模型答卷没有重评。它们的程序判据分都是 0。LLM 判据只扣分。所以换任何裁判，总分都是 0。

旧评分文件、中间结果和无效的裁判尝试都在各包的 `history/` 中。修改经过见 `history/CHANGELOG.md`。

## 三道题

### A 轨：ZCloud-电力监管-001-20261020

- 任务：计算 2020 年三项净资本支出差额（实际减预测）。三项是网络类、非网络类和合计。
- 依据：澳大利亚能源监管机构的配电网资产滚动模型手册，以及 Powercor 的输入表。
- 输入 2 份：`Distribution_handbook.pdf`、`Powercor_RFM_inputs.xlsx`。
- 判据 13 条（v1 是 9 条）。其中 LLM 判据 3 条。

### B 轨：ZCloud-财务分析-002-20261020

- 任务：推出 CNO Financial 2024 年第四季度的保险赔付（全年减前三季度）。然后和 2025 年第一季度比较，给出变化额和变化率，并整理季度汇总。
- 依据：CNO Financial 的 10-Q 和 10-K 表格。
- 输入 4 份：`CNO_2024-09-30_10Q.xlsx`、`CNO_2024-12-31_10K.xlsx`、`CNO_2025-03-31_10Q.xlsx`、`CNO_2025-06-30_10Q.xlsx`。
- 判据 23 条（v1 是 16 条）。其中 LLM 判据 3 条。

### C 轨：ZCloud-市政财务-002-20261022

- 任务：计算三种终止方案下，截至 2007 年 12 月 31 日应付给 SFMG 的本金余额。
- 依据：Muskegon 体育馆冠名合同的提前终止条款，以及付款台账。台账同时以 PDF 和图片提供。
- 输入 8 份：`Agreement.pdf`、`Records.pdf`、`Records_Broker_payments.png`、`Records_Finance_forecast.png`、`Records_Other_payments.png`、`Records_Plans.png`、`Records_Sources.png`、`Records_Sponsorships.png`。
- 判据 20 条（v1 是 17 条）。其中 LLM 判据 3 条。

## 目录结构

每道题有两个并列的文件夹。这和样例相同。

```text
office-demo-20261023/
├── ZCloud-电力监管-001-20261020/            # 题包
│   ├── README.md、manifest.json、交付文档.md
│   └── powercor-2020-capex-reconciliation/
│       ├── environment/、solution/、tests/、targets/
│       ├── metadata/、validation/、history/
│       └── task.toml、instruction.md、rubrics.json、records.jsonl、delivery_note.md
├── ZCloud-电力监管-001-20261020-轨迹报告/
│   ├── README.md、manifest.json、交付文档.md
│   └── powercor-2020-capex-reconciliation/
│       ├── golden/、rollouts/、judge_runs/、metadata/、validation/、history/
│       └── quality_report.json、consistency.json、records.jsonl、delivery_note.md
├── ZCloud-财务分析-002-20261020/ 与 -轨迹报告/    # 结构同上
├── ZCloud-市政财务-002-20261022/ 与 -轨迹报告/    # 结构同上
└── zips/                                  # 6 个压缩包与 SHA256SUMS.txt
```

## 下载

- `zips/` 里有 6 个压缩包。每道题有 1 个题包和 1 个轨迹报告。
- `zips/SHA256SUMS.txt` 是压缩包的校验值。
- 仓库根目录有同样内容的文件夹，可以在线浏览。

## 题包内容

| 路径 | 内容 |
|---|---|
| `instruction.md` | 给求解模型的题面：角色、任务、输出文件和表头要求。 |
| `task.toml` | 元数据、环境资源、验收超时和 `JUDGE_*` 环境变量。元数据包括行业、职业、领域分级、难度、估时、多模态标记和联网标记。 |
| `rubrics.json` | 全部判据，使用统一 schema。每条判据有 id、描述、权重、类型、维度和评分方法。权重只有 10、7、−3 三种。 |
| `environment/` | `Dockerfile`、`requirements.txt` 和 `input_files/`。`input_files/` 有全部输入原件，没有外链。 |
| `solution/` | `solve.sh` 和参考答案 `golden_output/answer.xlsx`。求解模型看不到这个目录。 |
| `tests/` | 评分器。`test.sh` 和样例逐字一致。`finalize.py` 在样例基础上增加了整卷 0 分、封顶和裁判读取校验。其余文件是程序判据和 LLM 判据的提示词。 |
| `targets/` | 交付文件的形态（`answer.xlsx`）。 |
| `metadata/task_metadata.json` | 题目来源、真实性说明、能力标签和三模型分数。 |
| `records.jsonl`、`manifest.json` | 本题的索引记录和文件清单。 |
| `validation/` | 回归检查 `run_regression.py`、正负例、路径检查 `validate_paths.py`、评分说明 `scoring_policy.md`、包审计结果、原件哈希比对、Sonnet 重评汇总和运行日志。 |
| `delivery_note.md` | 本题的交付说明：交付物、评分方式、复现方法和裁判情况。 |
| `history/` | 旧版本、中间结果和无效的裁判尝试。只供追溯。 |

## 轨迹报告内容

| 路径 | 内容 |
|---|---|
| `rollouts/<模型>/candidate.xlsx` | 该模型的答卷。`solver_output/` 是原样副本。 |
| `rollouts/<模型>/solver_prompt.md` | 该模型运行时实际收到的题面。 |
| `rollouts/<模型>/trajectory/` | 原始事件流 `events.jsonl`、逐条模型请求 `provider_requests.jsonl` 和分段记录 `segments.json`。 |
| `rollouts/<模型>/judge.json` | 每条判据的得分和理由。`reward.json` 和 `reward-details.json` 是评分器的原始输出。 |
| `rollouts/<模型>/renders/`、`visual_review.json` | 答卷每张工作表的 PDF 和 PNG 渲染图，以及查看记录。 |
| `rollouts/<模型>/structural_checks.json`、`extracted_text.md` | 工作簿结构检查结果和全部单元格文本。 |
| `rollouts/<模型>/` 下的运行记录 | `container_boundary.json`、`gateway_config.json`、`execution_verification.json`、`run_metadata.json`、`usage.json`。内容是运行环境、模型网关、返回型号核验、起止时间、请求数和用量。 |
| `golden/` | 参考答案的同一套文件。 |
| `judge_runs/` | 全部裁判结果：参考答案 5 次，每个模型 1 次。 |
| `discrimination_cases.json` | 部分正确样例。参考答案改错 k 项后，记录程序判据的分数。这些样例证明评分器能区分部分正确和完全正确。 |
| `consistency.json` | 参考答案 5 次评分的一致性统计，包括总分和每条判据。 |
| `quality_report.json` | 汇总：三模型分数、均分、区分度、一致性、来源核验和限制。 |

## 复现评分

1. 在题包目录构建镜像：`docker build -t office-demo environment/`。
   镜像只用公开源：python:3.12-slim-bookworm、Debian、npm 和 PyPI。国内网络可以加参数 `--build-arg DEBIAN_MIRROR=https://mirrors.tuna.tsinghua.edu.cn`。
2. 设置 `JUDGE_API_KEY` 和 `JUDGE_BASE_URL`。这两个变量必须设置。
3. 设置 `JUDGE_MODEL=claude-sonnet-5-5`。
   `task.toml` 的默认值是 claude-sonnet-5-5。不设这个变量、直接运行 `test.sh` 时，平台模板会改用 qwen3.7-plus。
4. 把答卷挂载到 `/app/output/answer.xlsx`。
5. 在容器里运行 `bash /tests/test.sh`。
   结果写入 `/logs/verifier/`。

只检查程序判据、不调用裁判时，在宿主机运行：

```sh
python3 tests/offline_score.py --candidate <答卷> --out <目录>
```

`JUDGE_PROVIDER` 和 `JUDGE_API_PROTOCOL` 的默认值也在各题 `task.toml` 中。

## 和样例的差异

- 交付格式：样例交付 PPT，本仓库交付 Excel。样例按页渲染幻灯片，本仓库按工作表渲染。
- 语言：样例的题面和判据是中文。本仓库的原始材料是英文的监管手册、财报和合同。所以题面和程序判据的名称用英文。LLM 判据、元数据和说明文档用中文。
- 题面措辞：模型运行后，题面改过措辞。数值、判据和输出格式要求没有改。改动如下：
  - Powercor 题增加了一句角色说明。
  - Powercor 和 Muskegon 两题改写了 Results 小标题和表头说明句。
  - 三题末尾的运行说明把输入目录改为 `/app/input_files/`。
  - 模型实际收到的题面在各模型目录的 `solver_prompt.md` 中。
- 运行次数：三个模型各跑了一次。需求说明要求的多次 rollout 和 pass@8 未做。
- 镜像：模型运行时用开发环境的镜像。题包里的 Dockerfile 是交付时重新写的公开版本。我们在断网容器里用这个 Dockerfile 重跑了程序判据。三道题的参考答案都是 1 分。九份模型答卷的程序判据分和成绩表一致。
- 运行环境：GPT-5.6-SOL 和 Qwen 3.8 Max 用 Codex CLI。Claude Opus 4.8 用 Claude Code。三个模型都在隔离的 Docker 容器里运行。样例的三个模型都用 Claude Code。
- 裁判原始响应：裁判的上游 HTTP 原始响应没有单独保存。每条判据的评分结果保存在 `reward-details.json` 和 `judge.json` 中。`judge_provider_response.json` 记录了这一点。
- 环境模板：`task.toml` 的 `environment_template` 指向包内的 `environment/Dockerfile`。平台是否接受这种写法：未确认。确认方法是询问平台方。
- 型号名：Qwen 运行时，网关返回两种型号名：`qwen/qwen3.8-max` 和 `qwen3.8-max-0902`。两者是同一基础型号。记录保留原值。

## 题目来源

三道题的题面和输入都改编自公开材料。计算规则全部来自原件。这些材料都不是客户的原始委托。

- Powercor：手册是澳大利亚能源监管机构公开的配电网资产滚动模型手册，使用原文件。输入表从公开模型整理。输入表中部分数值做过调整。每处调整都有登记记录。
- CNO：四份 Excel 由 CNO Financial 向美国证监会提交的季度报告和年度报告转录。
- Muskegon：体育馆冠名合同的公开节选。付款记录是按合同编制的案例数据，以 PDF 和图片两种形式提供。
