# LangChain Browser Use 示例

这个项目展示了如何使用 LangChain 结合 Browser Use 来自动化浏览器操作。

## 功能特性

- 使用 LangChain 的 Agent 框架
- 集成 Browser Use 进行网页自动化
- 支持多种浏览器操作：搜索、点击、填表等
- 提供多个实用示例

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基础示例
```bash
python basic_example.py
```

### 搜索示例
```bash
python search_example.py
```

### 表单填写示例
```bash
python form_example.py
```

## 配置

在使用前，请确保设置好你的 OpenAI API Key：

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 示例说明

1. `basic_example.py` - 基础的浏览器操作示例
2. `search_example.py` - 自动搜索和信息提取
3. `form_example.py` - 自动填写表单
4. `advanced_example.py` - 复杂的多步骤操作