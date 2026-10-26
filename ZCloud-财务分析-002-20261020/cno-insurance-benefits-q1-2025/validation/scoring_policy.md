# 评分口径

版本标签：评分器 v2（2026-10-26）。23 条判据保持现有权重：20 条程序项、3 条文字负项，正项权重合计 34。

## 门槛、封顶与扣分

- 必需 Results、Analysis 或 Summary 缺失或错名：整卷 0 分，不通过表头搜索补救。
- 必需表头去首尾空格后按大小写、文字和顺序比较；不符时 required_header_cap 将总分封顶 0.69。题面仅规定前置列，允许后附列、空白样式列和自由结构支持表。
- 来源/支持格空白或纯数字、单位不符、未知标签携带业务值：instruction_must_clause_cap 将总分封顶 0.69。
- 行序、重复记录、精度、来源定位等仍按对应程序负项扣分；不增加权重模拟封顶。正负权重池化后执行门槛与封顶，规则和原因写入 reward-details.json。

## 精度与容差

要求 p 位小数时，number_format 显示 p 位，或存值等于 round(value,p)，任一满足即可；百分比格式按百分点比较。通用的“至少 p 位”规则也接受存值精度不少于 p；本题没有此要求。数值容差独立：金额为 0.05 百万美元，百分比为 0.005 个百分点。输入与累计调整为十分位，季度加减没有额外合法中间舍入误差，不放宽容差。

## LLM 与程序归属

程序独占标准来源字段的文件、表格和单元格真实性（SD1、SD2、S02、SP1），以及来源存在性（S01）、数值、记录、顺序、单位与格式。L01 只看这些字段之外新增的虚构来源断言；L02 检查无证据的完成性声明；L03 检查新增公司经营事实。三条文字判据的文本和权重不变，不比较金标文本相似性。历史模型保存的判定不代表重新验证了全部候选上的归属行为。

## 程序负项

- `P1`（-3）：缺失或错误时扣分；正确不加分：Pivot: Summary fourth-quarter benefits equal the Analysis record
- `P2`（-3）：缺失或错误时扣分；正确不加分：Pivot: Summary first quarter less fourth quarter equals the Results change row
- `SD1`（-3）：缺失或错误时扣分；正确不加分：Analysis fourth-quarter record names a supplied file
- `SD2`（-3）：缺失或错误时扣分；正确不加分：Analysis first-quarter record names a supplied file
- `F1`（-3）：Required sheet header prefix matches exact case-sensitive text and order after trimming; trailing columns allowed.
- `F2`（-3）：Required sheet header prefix matches exact case-sensitive text and order after trimming; trailing columns allowed.
- `F3`（-3）：Required sheet header prefix matches exact case-sensitive text and order after trimming; trailing columns allowed.
- `X1`（-3）：Deduct 3 when any cell of the workbook holds an Excel error value
- `X2`（-3）：任一必需表出现额外业务记录、空键非空记录或重复记录时扣3分。
- `S01`（-3）：A required Results source_note or Analysis source_document/source_page is empty or numeric-only.
- `S02`（-3）：Results来源须指向实际随包文件和存在的worksheet/table；明确给出单元格时须在该表范围内，允许明确引用第2行来源；任一违规扣3分。
- `SP1`（-3）：Analysis每行source_page须给实际随包文件中的worksheet/table；任一缺失或不存在扣3分。
- `O01`（-3）：Results、Analysis、Summary的必需记录须按题面顺序出现且各一次；任一缺失、逆序或重复扣3分。
- `U01`（-3）：Results两行unit分别严格为USD millions、percent，Analysis两行严格为USD millions；任一违规扣3分。
- `DP1`（-3）：Results金额变动的number_format显示一位小数，或存储值等于舍入到一位小数的值，即满足要求；后者不限于General格式。否则扣3分。
- `DP2`（-3）：Results百分比的number_format显示两位小数，或存储值等于舍入到两位小数的值，即满足要求；后者不限于General格式。否则扣3分。

## 候选文件访问校验

内容判定必须建立在实际读取候选工作簿的证据上，每条理由须引用候选中存在的工作表与单元格。程序已成功读取候选，但理由宣称候选缺失/不可读，或缺少有效候选单元格引用时，finalize 记录 verifier_error=1、judge:artifact_access_error；该记录不是答卷得分，不计入一致性样本。来源文件缺失与候选无法读取分开处理，避免把正常来源负项误判为裁判错误。

## 复现与证据边界

运行 `python3 -B validation/run_regression.py` 检查正负例、池化规则、候选访问证据与保存判定；不调用求解器或裁判。LLM 裁判为 claude-sonnet-5-5。参考答案的 5 次评分（`judge_runs/golden_r1` 到 `golden_r5`）都来自它，总分和每条判据的标准差都是 0。除 B 的 GPT-5.6-SOL 外，模型答卷没有重评：它们程序分为 0，LLM 判据只扣分，任何裁判下都是 0 分。旧的 qwen 判定保留在 `history/`，不参与统计。
