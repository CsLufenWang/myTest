"""
搜索示例 - 使用 LangChain + Browser Use 进行智能搜索
演示如何自动搜索信息并提取结果
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

def create_search_agent():
    """创建专门用于搜索的 Agent"""
    
    # 初始化 LLM
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.1,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # 配置浏览器
    browser_config = BrowserConfig(
        headless=False,  # 显示浏览器窗口以便观察
        browser_type="chromium"
    )
    
    # 创建浏览器服务
    browser_service = BrowserUseService(config=browser_config)
    tools = browser_service.get_tools()
    
    # 创建搜索专用提示模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个专业的信息搜索助手。你的任务是：

        1. 理解用户的搜索需求
        2. 选择合适的搜索引擎
        3. 构造有效的搜索查询
        4. 提取和整理搜索结果
        5. 提供准确、有用的信息摘要

        搜索策略：
        - 对于中文内容，优先使用百度
        - 对于英文内容，优先使用Google
        - 对于技术问题，可以搜索Stack Overflow
        - 对于学术内容，可以搜索Google Scholar

        请确保：
        - 等待页面完全加载
        - 准确识别搜索结果
        - 提取关键信息
        - 避免点击广告链接
        """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    # 创建 Agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10
    )
    
    return agent_executor, browser_service

def search_and_summarize(query, search_engine="baidu"):
    """执行搜索并总结结果"""
    
    print(f"🔍 开始搜索: {query}")
    
    agent_executor, browser_service = create_search_agent()
    
    try:
        if search_engine.lower() == "baidu":
            search_url = "https://www.baidu.com"
        elif search_engine.lower() == "google":
            search_url = "https://www.google.com"
        else:
            search_url = "https://www.baidu.com"
        
        task = f"""
        请帮我搜索关于 "{query}" 的信息：
        
        1. 打开 {search_url}
        2. 在搜索框中输入查询词: {query}
        3. 点击搜索按钮
        4. 等待搜索结果加载
        5. 提取前5个搜索结果的标题和简介
        6. 总结这些信息，提供一个简洁的答案
        
        请确保提取的信息准确且有用。
        """
        
        result = agent_executor.invoke({"input": task})
        return result['output']
        
    except Exception as e:
        print(f"❌ 搜索过程中出现错误: {str(e)}")
        return None
    
    finally:
        browser_service.close()

def main():
    """主函数 - 演示多个搜索示例"""
    
    print("🔍 LangChain Browser Use 搜索示例")
    print("=" * 50)
    
    # 搜索示例列表
    search_queries = [
        ("Python LangChain 教程", "baidu"),
        ("机器学习最新发展", "baidu"),
        ("Browser automation best practices", "google")
    ]
    
    for query, engine in search_queries:
        print(f"\n📋 搜索任务: {query} (使用 {engine})")
        print("-" * 30)
        
        result = search_and_summarize(query, engine)
        
        if result:
            print(f"✅ 搜索结果:\n{result}")
        else:
            print("❌ 搜索失败")
        
        print("\n" + "="*50)

def interactive_search():
    """交互式搜索模式"""
    
    print("🔍 进入交互式搜索模式")
    print("输入 'quit' 退出程序")
    
    agent_executor, browser_service = create_search_agent()
    
    try:
        while True:
            query = input("\n请输入搜索内容: ").strip()
            
            if query.lower() in ['quit', 'exit', '退出']:
                break
            
            if not query:
                continue
            
            engine = input("选择搜索引擎 (baidu/google) [默认: baidu]: ").strip() or "baidu"
            
            print(f"🔍 搜索: {query}")
            
            try:
                if engine.lower() == "baidu":
                    search_url = "https://www.baidu.com"
                else:
                    search_url = "https://www.google.com"
                
                task = f"""
                搜索 "{query}":
                1. 打开 {search_url}
                2. 搜索 "{query}"
                3. 提取并总结前3个结果
                """
                
                result = agent_executor.invoke({"input": task})
                print(f"✅ 结果:\n{result['output']}")
                
            except Exception as e:
                print(f"❌ 搜索出错: {str(e)}")
    
    finally:
        browser_service.close()
        print("👋 再见！")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_search()
    else:
        main()