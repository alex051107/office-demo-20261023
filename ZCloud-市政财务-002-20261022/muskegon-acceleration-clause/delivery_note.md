本次提交 1 道市政财务题（C 轨，合同与台账），三模型单次答卷均分 0.00%。

题包：ZCloud-市政财务-002-20261022.zip；轨迹报告：ZCloud-市政财务-002-20261022-轨迹报告.zip。提交时两个文件链接放在同一行。

数据量：1 道题，8 份输入文件（Agreement.pdf、Records.pdf、Records_Broker_payments.png、Records_Finance_forecast.png、Records_Other_payments.png、Records_Plans.png、Records_Sources.png、Records_Sponsorships.png）。
三个模型：GPT-5.6-SOL、Claude Opus 4.8、Qwen 3.8 Max。
三模型得分：GPT-5.6-SOL 0.0000，Claude Opus 4.8 0.0000，Qwen 3.8 Max 0.0000；均分 0.0000。参考答案分数：1.000（五份历史 LLM 判定与本次程序结果重组，标准差 0.0；不是新增五次裁判）。

轨迹报告含三模型原始消息、工具调用、实际答卷 xlsx、每张工作表的渲染图及逐条裁判记录（Claude Opus 4.8 的 LLM 扣分项未评完，见说明与限制）。

求解 Agent 只能看到 instruction.md 与 environment/input_files/；答卷写入 /app/output/answer.xlsx。rubrics.json、solution/、tests/、metadata/ 和轨迹报告不挂载到求解上下文。

三个模型各在独立的 Docker 容器中运行：GPT-5.6-SOL 与 Qwen 3.8 Max 使用 Codex CLI，Claude Opus 4.8 使用 Claude Code。模型名称保留网关原始返回值；Qwen 运行中网关返回过 qwen/qwen3.8-max 与 qwen3.8-max-0902 两种写法，属同一基础型号。每个模型目录下的 container_boundary.json、gateway_config.json、execution_verification.json、trajectory/provider_requests.jsonl 由运行时回执导出，未补造任何请求。

**评分与证据**

- 评分标准共 20 条：程序判据 17 条（其中正项 6 条），LLM 扣分项 3 条；正项权重合计 51。权重只取 [-3, 7, 10] 中的值。
- 计分：正项按正确度计分，负项按违规程度扣分，负项不进入分母，总分截断到 [0, 1]。公式：`round(clip((sum(w_i*q_i for w_i>0)-sum(abs(w_j)*v_j for w_j<0))/s_max,0,1),6)`。通过阈值 0.7。
- 一致性：复用参考答案五份历史 LLM 判定分别与本次程序分重组，总分 [1.0, 1.0, 1.0, 1.0, 1.0]，总分样本标准差 0.0，单条判据样本标准差最大 0.0（要求都 < 0.05）。
- 区分度：参考答案 1.000，三模型 0.0000、0.0000、0.0000。
- 部分正确样例：以参考答案为底改错部分结果项，离线程序评分为 0/6 项正确 0.000、1/6 项正确 0.196、2/6 项正确 0.392、3/6 项正确 0.588、4/6 项正确 0.725、5/6 项正确 0.863、6/6 项正确 1.000（仅程序子集，未推定 LLM 是否违规），见轨迹报告 discrimination_cases.json。
- 难度：每个模型各一次有效运行（pass@1），未做 8 次独立运行，所以没有 pass@8。
- 逐条结果见轨迹报告各模型目录下的 judge.json；汇总见 quality_report.json。

**运行与验收**

以下变量由验收运行器注入 verifier 容器，不注入求解 Agent。

| 变量 | 必选 | 默认值 | 用途 |
|---|---|---|---|
| JUDGE_API_KEY | 是 | 无 | 裁判 API 凭据；未设置时读取 EVAL_API_KEY。真实凭据不随题包交付。 |
| JUDGE_BASE_URL | 是 | 无 | 裁判服务地址；未设置时读取 EVAL_API_BASE。 |
| JUDGE_MODEL | 否 | qwen3.7-plus | 裁判模型；通过 REWARDKIT_MODEL 传入评分器。 |
| JUDGE_PROVIDER | 否 | anthropic | Provider 接口声明；协议切换由 JUDGE_API_PROTOCOL 控制。 |
| JUDGE_API_PROTOCOL | 否 | anthropic | 默认使用 Claude Code Judge；openai 切换兼容 LLM Judge。 |
| EVAL_API_KEY | 否 | 空 | 旧配置兜底；有 JUDGE_API_KEY 时忽略。 |
| EVAL_API_BASE | 否 | 空 | 旧配置兜底；有 JUDGE_BASE_URL 时忽略。 |
| LITELLM_DROP_PARAMS | 否 | true | 网关参数兼容开关。 |

Oracle 入口为 `bash /solution/solve.sh`，验收入口为 `bash /tests/test.sh`，评分输出位于 `/logs/verifier/`。这些是容器内运行路径，不是交付附件路径；test.sh 只在验收容器内执行，不要在宿主机直接运行。verifier 总超时 18000 秒，由 task.toml 配置，不是求解 Agent 的轮次限制。

**说明与限制**

- 题面改编自公开材料；输入文件随包交付，没有外链。
- 每个模型只有一次运行，分数是单次结果，不代表 pass@8。
- environment_template 写为 environment/Dockerfile，表示包内自定义 Dockerfile；平台是否接受这种写法需要确认。
- 裁判的上游原始 HTTP 响应没有单独保存，judge_provider_response.json 写明了这一点；逐条裁判结果完整保留在 reward-details.json 与 judge.json。
- 模型运行时实际收到的题面原样放在轨迹报告各模型目录下的 solver_prompt.md。
- 题面差异：Results 表的小标题和表头说明句换了措辞，行顺序、单位和数值要求不变；末尾的运行说明把输入目录从 /app/input 改为题包镜像里的 /app/input_files/。数值、判据和输出格式要求相同。
- environment/Dockerfile 只用公开源构建（python:3.12-slim-bookworm、Debian、npm、PyPI）。模型运行时用的是开发环境镜像；用本 Dockerfile 在断网容器里重算程序判据，参考答案 1 分，三份模型答卷的程序分与本文成绩一致。
- Claude Opus 4.8 答卷的 LLM 裁判作业运行异常（请求次数远超正常作业），被人工停止，没有纳入一致性统计。
- Claude Opus 4.8 答卷只有程序判据结果：正项得分为 0，LLM 判据全部是扣分项，所以总分只能是 0，记 0。
- 开发阶段的另一套评分规则给三个模型各 0.07 分，全部来自格式项；本包规则下格式项只扣分不加分，记 0。

## 评分器 v2（2026-10-26）

此为固定版本标签；本次离线修订执行于 2026-10-25，未新增求解运行或 LLM 请求。

- 必需 Results、Detail 表名以及表头文字、列序、列数必须完全匹配；任何接口错误令全题为 0，不按表头回退找表。额外支持表允许自由组织。
- 每个程序负项统一按既有 S01 的 3 分尺度扣分。Results 规定行序、严格 USD 单位、每条来源说明、额外业务记录、两个表的两位小数显示分别有有效判据；Detail 额外方案仍单独检查。来源说明不能只填数字；支持计算允许沿用 D2:D4 文字计算或支持表。
- Results 的 Plan D、重复记录及无标签金额行不再获程序满分；Detail 列序不符直接触发接口 0 分。金额绝对容差从 0.011 改为 0.005 USD；显示精度另计。
- 评分条目共 20 条：程序 17 条（正项 6 条，权重合计 51），LLM 3 条，文本及权重不变。现有 LLM 判定原样复用，以固定 finalize 的 signed-weight 公式重组；未完成的 Opus 负项仍未完成，不补造结果。
- 原评分文件保存在同目录 `.v1.json` / `.v1.jsonl`；新程序明细见 `programmatic_score.json`。32 份负例均低于满分，其中接口负例均为 0；七份原部分正确控制卷已按 v2 重算。
- 金标五份副本统一两位小数，Results 来源列换行、加宽并调整行高；金额、日期、来源与文字计算式未变。两张表沿用 Calc PDF 导出和 PNG 渲染。

| 答卷 | 原分 | v2 程序分 | v2 最终分 |
|---|---:|---:|---:|
| 金标 | 1.000000 | 1.000000 | 1.000000 |
| GPT-5.6-SOL | 0.000000 | 0.000000 | 0.000000 |
| Claude Opus 4.8 | 0.000000 | 0.000000 | 0.000000 |
| Qwen 3.8 Max | 0.000000 | 0.000000 | 0.000000 |

说明：Opus 的程序分上界为 0，而未评的 LLM 项全部为负项，所以最终分必为 0；这不代表其 LLM 已完成。五份金标历史判定只用于复用重组，不声称新增五次一致性实验。

待确认：instruction.md 按要求保持原样；未来若要把精确接口的全题门槛写入题面，应另行修订版本。Sol 已保存 LLM 理由有“未找到交付文件”的表述，本次按要求原样保留；该证据差异及 Opus 未完成的 LLM 判定不在本轮补跑。第 1、2、4 类事项仍暂缓。
