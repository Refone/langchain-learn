# LangChain 中, 如何让大模型更加准确地判断是否需要调用工具?

## 1. 写好工具描述（最重要）

模型判断"是否调用工具"主要依据工具的 `name` 和 `description`，描述要具体说明**何时用、何时不用**：

```python
from langchain_core.tools import tool
@tool
def search_weather(city: str) -> str:
    """查询指定城市的实时天气。

    仅当用户明确询问天气、气温、降水时使用本工具。
    不要用于回答常识性气候问题或历史天气咨询。
    """
    ...
```

要点：

- 描述中给出**正反例**（何时调用 / 何时直接回答）
- 参数也要有清晰的描述（通过 Pydantic 的 `Field(description=...)`）
- 避免多个工具职责重叠，职责越清晰越不容易误选

## 2. 优化系统提示词

在 System Prompt 中明确工具的边界：

```python
system = """你可以调用以下工具。
规则：
1. 能凭已有知识回答的问题，直接回答，不要调用工具。
2. 涉及实时数据（股价、天气、新闻）必须调用工具。
3. 不确定时优先直接回答，避免无意义的工具调用。"""
```

## 3. 用 Few-shot 示例引导

在消息历史中插入工具调用的示例对话，模型对齐效果显著：

```python
from langchain_core.messages import HumanMessage, AIMessage

examples = [
    HumanMessage("北京今天天气怎么样？"),
    AIMessage("", tool_calls=[{"name": "search_weather", "args": {"city": "北京"}, "id": "1"}]),
    # 反例：不需要工具的情况
    HumanMessage("什么是光合作用？"),
    AIMessage("光合作用是植物利用光能……"),
]
```

## 4. 控制工具数量与参数结构

- **工具数量别太多**：10 个以上时误调/漏调率明显上升。工具多时可先做一层"工具路由"（先用 embedding 或一个小模型筛选相关工具，再交给主模型）
- **参数尽量简单**：减少必填参数数量，给参数设置合理默认值，降低模型构造错误参数的概率
- 用 Pydantic 定义参数 schema 并加校验，让模型有明确的结构参照

## 5. 选择 / 调整模型与绑定方式

```python
llm_with_tools = llm.bind_tools(
    tools,
    tool_choice="auto",   # auto / required / none / 指定工具名
)
```

- 用原生支持 function calling 的模型（GPT-4o、Claude、Qwen 等），比靠 prompt 解析的 ReAct 模式可靠得多
- `tool_choice="required"` 可强制调用，`"none"` 可禁用——根据场景动态切换比完全交给模型判断更可控
- 适当降低 temperature

## 6. 加一层校验与兜底

- **调用前校验**：用 `with_fallbacks` 或在工具内部校验参数合法性，不合法时返回错误信息让模型重试（LangChain 默认会把工具异常回传给模型自我修正）
- **结构化输出 + 人工确认**：高风险操作先用结构化输出让模型说明"为什么要调用"，再决定是否执行
- **评估驱动**：收集误调/漏调的 bad case，加入 few-shot 示例或改进描述，这是最有效的迭代方式

## 7. 复杂场景：显式规划代替隐式判断

如果靠模型自主判断始终不稳定，可以改成显式流程（LangGraph）：

```text
分类节点（是否需要工具？哪个工具？）→ 工具节点 → 汇总节点
```

用一个小模型或分类器专门做"是否需要工具"的判断，主模型只负责生成和总结，准确率通常比让主模型"边想边决定"更高。

**一句话总结**：优先级是 ① 工具描述写清楚 → ② 系统提示词定边界 → ③ few-shot 示例 → ④ 减少工具数量/简化参数 → ⑤ 用 LangGraph 显式路由兜底。
