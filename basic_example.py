"""
基础的 LangChain + Browser Use 示例
演示如何使用 LangChain Agent 控制浏览器进行基本操作
"""

import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from browser_use import Browser
from browser_use.agent.service import BrowserUseService
from browser_use.browser.browser import BrowserConfig

# 加载环境变量
load_dotenv()

def create_browser_agent():
    """创建一个带有浏览器功能的 LangChain Agent"""
    
    # 初始化 LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # 配置浏览器
    browser_config = BrowserConfig(
        headless=os.getenv("HEADLESS", "False").lower() == "true",
        browser_type=os.getenv("BROWSER_TYPE", "chromium")
    )
    
    # 创建浏览器服务
    browser_service = BrowserUseService(config=browser_config)
    
    # 获取浏览器工具
    tools = browser_service.get_tools()
    
    # 创建提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个专业的网页自动化助手。你可以使用浏览器工具来：
        1. 导航到网页
        2. 点击元素
        3. 填写表单
        4. 提取信息
        5. 截图
        
        请根据用户的要求，使用合适的工具来完成任务。
        在执行操作前，请先分析页面结构，然后逐步执行。
        """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    # 创建 Agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # 创建 Agent Executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent_executor, browser_service

def main():
    """主函数 - 演示基本的浏览器操作"""
    
    print("🚀 启动 LangChain Browser Use 示例...")
    
    try:
        # 创建 Agent
        agent_executor, browser_service = create_browser_agent()
        
        # 示例任务：访问百度并搜索
        task = """
        请帮我完成以下任务：
        1. 打开百度网站 (https://www.baidu.com)
        2. 在搜索框中输入 "LangChain"
        3. 点击搜索按钮
        4. 等待结果加载
        5. 告诉我搜索结果的标题
        """
        
        print(f"📋 执行任务: {task}")
        
        # 执行任务
        result = agent_executor.invoke({"input": task})
        
        print(f"✅ 任务完成！结果: {result['output']}")
        
    except Exception as e:
        print(f"❌ 执行过程中出现错误: {str(e)}")
    
    finally:
        # 清理资源
        if 'browser_service' in locals():
            browser_service.close()
        print("🔚 程序结束")

if __name__ == "__main__":
    main()