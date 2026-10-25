## 评分器 v2（2026-10-26）

本次仅修复第3类评分覆盖和第5类参考答案质量；版本日期沿用修复总则，实际离线检查于2026-10-25完成。未修改instruction.md、四份输入或任何模型答卷，未执行新求解、新rollout或网络裁判。

- 必需表名、首行表头文字、列序和列数必须精确匹配；任一失败整卷0分，不再按表头回退找表。额外支持表允许存在且不受业务检查约束。
- 共23条有效判据：20条程序项、3条原有文字项；正项仍为10、10、7、7，分母34。新增7个独立−3扣分项：Results来源存在性S01、定位S02、Analysis定位SP1、行序O01、单位U01、金额精度DP1、百分比精度DP2；额外业务记录X2改为独立−3二元扣分。负项不进入分母，保留原有计分和0.7通过阈值。
- 数值容差与显示分开：金额0.05、百分比0.005；金额显示一位、百分比两位。允许相应的已舍入存储值或明确number_format。原有3条文字判据的文本、权重和保存判定均不变。
- 已保存的11组程序/文字混合评分均离线重组，调用既有finalize.py；不是11次新裁判。原评分文件均以相邻.v1文件保留。参考答案重组分1.000000，GPT-5.6-SOL 0.205882，Claude Opus4.8 0.000000，Qwen3.8 Max 0.000000；与旧分相同。五份历史参考答案文字判定分别复用后均为1分，不能当作修订版五次独立混合验收。

| 答卷 | v1总分 | v2离线重组总分 |
|---|---:|---:|
| 参考答案 | 1.000000 | 1.000000 |
| GPT-5.6-SOL | 0.205882 | 0.205882 |
| Claude Opus4.8 | 0.000000 | 0.000000 |
| Qwen3.8 Max | 0.000000 | 0.000000 |

参考答案五份副本同步更新。Results B2固定0.0、B3固定0.00；Analysis和Summary金额也固定一位。Results D2与D3各自完整列出：CNO_2024-12-31_10K.xlsx的T050!G15、CNO_2024-09-30_10Q.xlsx的T010!S19、CNO_2025-03-31_10Q.xlsx的T010!G19，以及CNO_2025-06-30_10Q.xlsx的T016!N14、T016!N24、Text!A131。

21.6与31.7是两个时点的累计嵌入衍生工具误差；本季费用调整为−(31.7−21.6)=−10.1。修订Q4=(2471.9−21.6)−(1926.4+15.6)=508.3，修订Q1=580.1−10.1=570.0；差额61.7，变化率12.1385008853…%，显示12.14。保留静态值，题面未要求必须新增公式。三表均已换行、调整列宽和行高；LibreOffice/Poppler重新生成3份PDF与3张PNG并逐张查看，未见内容截断。

回归：51个负例均低于1分，其中19个接口负例均为0；4个合法控制均为1，正确金标为1。逐项旧程序分/新程序分见validation/negative_cases/cases.json；11组离线重组见validation/rescore_summary.json（位于题包）。

待确认：题面尚未明示“最新修订口径＋累计误差差分”基准；依修复总则不改instruction.md，已在参考解与此说明补足。修订后金标文字未重新送裁判；本次不补pass@8，也不处理第1、2、4类或重建外层压缩包。

---

## 初次交付记录

以下保留原运行条件及历史结果；当前评分结构、参考答案与离线证据以v2节为准。

本次提交 1 道财务分析题（B 轨，财报分析），三模型单次答卷均分 6.86%。

题包：ZCloud-财务分析-002-20261020.zip；轨迹报告：ZCloud-财务分析-002-20261020-轨迹报告.zip。提交时两个文件链接放在同一行。

数据量：1 道题，4 份输入文件（CNO_2024-09-30_10Q.xlsx、CNO_2024-12-31_10K.xlsx、CNO_2025-03-31_10Q.xlsx、CNO_2025-06-30_10Q.xlsx）。
三个模型：GPT-5.6-SOL、Claude Opus 4.8、Qwen 3.8 Max。
三模型得分：GPT-5.6-SOL 0.2059，Claude Opus 4.8 0.0000，Qwen 3.8 Max 0.0000；均分 0.0686。参考答案分数：1.000（同一答卷重复评分 5 次，标准差 0.0）。

轨迹报告含三模型原始消息、工具调用、实际答卷 xlsx、每张工作表的渲染图及逐条裁判记录。

求解 Agent 只能看到 instruction.md 与 environment/input_files/；答卷写入 /app/output/answer.xlsx。rubrics.json、solution/、tests/、metadata/ 和轨迹报告不挂载到求解上下文。

三个模型各在独立的 Docker 容器中运行：GPT-5.6-SOL 与 Qwen 3.8 Max 使用 Codex CLI，Claude Opus 4.8 使用 Claude Code。模型名称保留网关原始返回值；Qwen 运行中网关返回过 qwen/qwen3.8-max 与 qwen3.8-max-0902 两种写法，属同一基础型号。每个模型目录下的 container_boundary.json、gateway_config.json、execution_verification.json、trajectory/provider_requests.jsonl 由运行时回执导出，未补造任何请求。

**评分与证据**

- 评分标准共 16 条：程序判据 13 条（其中正项 4 条），LLM 扣分项 3 条；正项权重合计 34。权重只取 [-7, -3, 7, 10] 中的值。
- 计分：正项按正确度计分，负项按违规程度扣分，负项不进入分母，总分截断到 [0, 1]。公式：`round(clip((sum(w_i*q_i for w_i>0)-sum(abs(w_j)*v_j for w_j<0))/s_max,0,1),6)`。通过阈值 0.7。
- 一致性：参考答案重复评分 5 次，总分 [1.0, 1.0, 1.0, 1.0, 1.0]，总分样本标准差 0.0，单条判据样本标准差最大 0.0（要求都 < 0.05）。
- 区分度：参考答案 1.000，三模型 0.2059、0.0000、0.0000。
- 部分正确样例：以参考答案为底改错部分结果项，离线程序评分为 0/4 项正确 0.000、1/4 项正确 0.206、2/4 项正确 0.500、3/4 项正确 0.794、4/4 项正确 1.000（LLM 扣分项按未违规处理），见轨迹报告 discrimination_cases.json。
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
- 题面差异：题面正文与模型运行时一致；末尾的运行说明把输入目录从 /app/input 改为题包镜像里的 /app/input_files/。数值、判据和输出格式要求相同。
- environment/Dockerfile 只用公开源构建（python:3.12-slim-bookworm、Debian、npm、PyPI）。模型运行时用的是开发环境镜像；用本 Dockerfile 在断网容器里重算程序判据，参考答案 1 分，三份模型答卷的程序分与本文成绩一致。
- Qwen 3.8 Max 答卷用公式给出结果；用 LibreOffice 重算公式后离线程序分仍为 0，失分来自数值本身。
- 开发阶段的另一套评分规则含部分分，给 Qwen 3.8 Max 0.16 分；本包统一使用 Office 裁判分。
