# Office 数据交付 demo（2026-10-23）

A、B、C 三条轨道各做了一道完整的题，格式照张老师飞书里的 Office 交付样例，要求照《Cowork RL Office 数据需求说明》。每道题分两个文件夹：**题包**交给求解与验收使用，**轨迹报告**记录三个模型实际怎么做、怎么被评分。

## 成绩

| 轨道 | 题包 | GPT-5.6-SOL | Claude Opus 4.8 | Qwen 3.8 Max | 三模型均分 | 参考答案（5 次，标准差） |
|---|---|---:|---:|---:|---:|---:|
| A 专业计算 | ZCloud-电力监管-001-20261020 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000（0.0） |
| B 财报分析 | ZCloud-财务分析-002-20261020 | 0.2059 | 0.0000 | 0.0000 | 0.0686 | 1.000（0.0） |
| C 合同与台账 | ZCloud-市政财务-002-20261022 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.000（0.0） |

分数是 Office 裁判（qwen3.7-plus，harbor-rewardkit 0.1.7）对每份答卷的第一次评分，满分 1。需求说明的难度线是三个模型里至少两个低于 0.6，三道题都满足。每个模型只跑了一次，所以表里是 pass@1，没有 pass@8。

## 三道题

- **A 轨 · ZCloud-电力监管-001-20261020**：根据澳大利亚能源监管机构的配电网资产滚动模型手册和 Powercor 的输入表，算 2020 年网络类、非网络类和合计三项净资本支出差额（实际减预测）。输入 2 份（Distribution_handbook.pdf、Powercor_RFM_inputs.xlsx），评分标准 9 条，其中 LLM 扣分项 3 条。
- **B 轨 · ZCloud-财务分析-002-20261020**：从 CNO Financial 的 10-Q 与 10-K 表格推出 2024 年第四季度保险赔付（全年减前三季度），与 2025 年第一季度比较，给出变化额和变化率，并整理季度汇总。输入 4 份（CNO_2024-09-30_10Q.xlsx、CNO_2024-12-31_10K.xlsx、CNO_2025-03-31_10Q.xlsx、CNO_2025-06-30_10Q.xlsx），评分标准 16 条，其中 LLM 扣分项 3 条。
- **C 轨 · ZCloud-市政财务-002-20261022**：按 Muskegon 体育馆冠名合同的提前终止条款和付款台账，算三种终止方案下截至 2007 年 12 月 31 日应付的 SFMG 本金余额。台账同时给 PDF 与图片。输入 8 份（Agreement.pdf、Records.pdf、Records_Broker_payments.png、Records_Finance_forecast.png、Records_Other_payments.png、Records_Plans.png、Records_Sources.png、Records_Sponsorships.png），评分标准 17 条，其中 LLM 扣分项 3 条。

## 下载

`zips/` 里有 6 个压缩包，每道题一个题包、一个轨迹报告，和样例一样可以直接转发。`zips/SHA256SUMS.txt` 是校验值。同样的内容也以文件夹形式放在仓库根目录，方便在线浏览。

## 题包里有什么

| 路径 | 作用 |
|---|---|
| `instruction.md` | 给求解 Agent 的完整题面：角色、任务、输出文件与表头要求。 |
| `task.toml` | 元数据（行业、职业、领域分级、难度、估时、多模态与联网标记）、环境资源、验收超时和 `JUDGE_*` 环境变量。 |
| `rubrics.json` | 评分标准，统一 schema。每条有 id、描述、权重、类型、维度和评分方法；权重只用 10、7、-3、-7。 |
| `environment/` | `Dockerfile`、`requirements.txt` 和 `input_files/`（全部输入原件，没有外链）。 |
| `solution/` | `solve.sh` 与参考答案 `golden_output/answer.xlsx`。求解 Agent 看不到。 |
| `tests/` | 验收入口 `test.sh` 和 `finalize.py`（与样例逐字一致），以及程序判据的实现与 LLM 判据提示词。 |
| `targets/` | 要求交付的文件形态（answer.xlsx）。 |
| `metadata/task_metadata.json` | 题目来源、真实性说明、能力标签、三模型分数。 |
| `records.jsonl`、`manifest.json` | 本题的索引记录与文件清单。 |
| `validation/` | 路径检查脚本、包审计结果、原件与随包文件的哈希比对。 |
| `delivery_note.md` | 本题的交付说明：可见范围、运行方式、评分证据和限制。 |

## 轨迹报告里有什么

| 路径 | 作用 |
|---|---|
| `rollouts/<模型>/candidate.xlsx` | 该模型交出的答卷，`solver_output/` 是原样副本。 |
| `rollouts/<模型>/solver_prompt.md` | 该模型运行时实际收到的题面，原样保存。 |
| `rollouts/<模型>/trajectory/` | 原始事件流 `events.jsonl`（消息、工具调用、结束状态），逐条模型请求 `provider_requests.jsonl`，分段记录 `segments.json`。 |
| `rollouts/<模型>/judge.json` | 逐条评分：每条判据的得分、程序或 LLM 给出的理由。`reward.json` 与 `reward-details.json` 是评分器原始输出。 |
| `rollouts/<模型>/renders/`、`visual_review.json` | 答卷每张工作表渲染成的 PDF 和 PNG，以及查看记录。 |
| `rollouts/<模型>/structural_checks.json`、`extracted_text.md` | 工作簿结构检查和全部单元格文本。 |
| `rollouts/<模型>/container_boundary.json`、`gateway_config.json`、`execution_verification.json`、`run_metadata.json`、`usage.json` | 运行环境、模型网关、返回型号核验、起止时间、请求数和用量，均从运行回执导出。 |
| `golden/` | 参考答案的同一套文件。 |
| `judge_runs/` | 参考答案 5 次、各模型 1 次的全部裁判结果。 |
| `consistency.json` | 参考答案重复评分 5 次的一致性统计（总分和逐条）。 |
| `quality_report.json` | 汇总：三模型分数、均分、区分度、一致性、来源核验和限制。 |

## 复现评分

1. 在题包目录构建镜像：`docker build -t office-demo environment/`。镜像只用公开源（python:3.12-slim-bookworm、Debian、npm、PyPI），国内网络可加 `--build-arg DEBIAN_MIRROR=https://mirrors.tuna.tsinghua.edu.cn`。
2. 设置裁判凭据：`JUDGE_API_KEY` 和 `JUDGE_BASE_URL` 必填，`JUDGE_MODEL` 默认 `qwen3.7-plus`。完整变量表见各题 `delivery_note.md`。
3. 把答卷挂到 `/app/output/answer.xlsx`，在容器里执行 `bash /tests/test.sh`，结果写入 `/logs/verifier/`。
4. 只想看程序判据、不调用 LLM，可以在宿主机运行 `python3 tests/offline_score.py --candidate <答卷> --out <目录>`。

## 和样例不同的地方

- 样例交付的是 PPT，这三道题交付 Excel。样例按页渲染幻灯片，这里按工作表渲染。
- 样例的题面和评分标准是中文。这三道题的原始材料是英文的监管手册、财报和合同，所以题面和程序判据的名称用英文，LLM 扣分项、元数据和说明文档用中文。模型和裁判都是按这份文本运行和评分的。
- 题面在模型运行后改过措辞：Powercor 题补了一句角色说明，Powercor 和 Muskegon 两题的 Results 小标题与表头说明句换了说法，三题末尾的运行说明把输入目录改成题包镜像里的 `/app/input_files/`。数值、判据和输出格式要求没有变。模型实际收到的题面见各模型目录下的 `solver_prompt.md`。
- 三个模型各跑了一次。需求说明要求的多次 rollout 和 pass@8 还没有做。
- 模型运行时用的是开发环境的镜像，题包里的 Dockerfile 是交付时重新写的公开版本。我们用它在断网容器里重新跑了程序判据：三道题的参考答案都是 1 分，九份模型答卷的程序分和表里的成绩一致。
- 运行环境：GPT-5.6-SOL 与 Qwen 3.8 Max 用 Codex CLI，Claude Opus 4.8 用 Claude Code，都在隔离的 Docker 容器里运行。样例三个模型都用 Claude Code。
- 裁判的上游原始 HTTP 响应没有单独保存。逐条评分结果完整保存在 `reward-details.json` 和 `judge.json` 里，`judge_provider_response.json` 如实写明了这一点。
- `task.toml` 的 `environment_template` 写的是包内的 `environment/Dockerfile`，平台是否接受这种写法需要确认。
- Qwen 运行中网关返回的型号名有 `qwen/qwen3.8-max` 和 `qwen3.8-max-0902` 两种写法，属于同一基础型号，原值保留。

## 题目来源

三道题的题面和输入都改编自公开材料，计算规则全部来自原件。

- Powercor：澳大利亚能源监管机构公开的配电网资产滚动模型手册（原文件），加上从公开模型整理出的输入表；输入表里部分数值做过调整，调整有登记记录。
- CNO：四份 Excel 由 CNO Financial 向美国证监会提交的季度和年度报告转录。
- Muskegon：体育馆冠名合同的公开节选，付款记录是依据合同编制的案例数据，以 PDF 和图片两种形式给出。

这些都不是客户的原始委托。
