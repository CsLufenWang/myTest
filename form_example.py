"""
表单填写示例 - 使用 LangChain + Browser Use 自动填写表单
演示如何智能识别和填写各种类型的表单
"""

import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from browser_use.agent.service import BrowserUseService
from browser_use.browser.browser import BrowserConfig

# 加载环境变量
load_dotenv()

def create_form_agent():
    """创建专门用于表单操作的 Agent"""
    
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    browser_config = BrowserConfig(
        headless=False,
        browser_type="chromium"
    )
    
    browser_service = BrowserUseService(config=browser_config)
    tools = browser_service.get_tools()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个专业的表单填写助手。你的能力包括：

        表单识别：
        - 识别各种输入字段类型（文本、邮箱、密码、数字等）
        - 识别下拉菜单、复选框、单选按钮
        - 识别必填字段和可选字段

        智能填写：
        - 根据字段标签和类型选择合适的内容
        - 处理验证规则（邮箱格式、密码强度等）
        - 处理动态表单（AJAX加载的字段）

        操作策略：
        1. 先分析整个表单结构
        2. 识别所有字段和要求
        3. 按逻辑顺序填写
        4. 处理验证错误
        5. 提交表单

        注意事项：
        - 等待页面和字段完全加载
        - 检查字段是否可见和可编辑
        - 处理弹出窗口和确认对话框
        - 避免提交敏感的真实信息
        """),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=15
    )
    
    return agent_executor, browser_service

def create_test_form_page():
    """创建一个测试表单页面"""
    
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>测试表单</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
            button { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background-color: #0056b3; }
            .required { color: red; }
            .success { color: green; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>用户注册表单</h1>
        <form id="registrationForm">
            <div class="form-group">
                <label for="firstName">姓名 <span class="required">*</span></label>
                <input type="text" id="firstName" name="firstName" required>
            </div>
            
            <div class="form-group">
                <label for="email">邮箱地址 <span class="required">*</span></label>
                <input type="email" id="email" name="email" required>
            </div>
            
            <div class="form-group">
                <label for="phone">电话号码</label>
                <input type="tel" id="phone" name="phone">
            </div>
            
            <div class="form-group">
                <label for="age">年龄</label>
                <input type="number" id="age" name="age" min="18" max="100">
            </div>
            
            <div class="form-group">
                <label for="gender">性别</label>
                <select id="gender" name="gender">
                    <option value="">请选择</option>
                    <option value="male">男</option>
                    <option value="female">女</option>
                    <option value="other">其他</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="interests">兴趣爱好</label>
                <div>
                    <input type="checkbox" id="reading" name="interests" value="reading">
                    <label for="reading" style="display: inline; margin-left: 5px;">阅读</label>
                </div>
                <div>
                    <input type="checkbox" id="sports" name="interests" value="sports">
                    <label for="sports" style="display: inline; margin-left: 5px;">运动</label>
                </div>
                <div>
                    <input type="checkbox" id="music" name="interests" value="music">
                    <label for="music" style="display: inline; margin-left: 5px;">音乐</label>
                </div>
            </div>
            
            <div class="form-group">
                <label for="bio">个人简介</label>
                <textarea id="bio" name="bio" rows="4" placeholder="请简单介绍一下自己..."></textarea>
            </div>
            
            <div class="form-group">
                <input type="checkbox" id="terms" name="terms" required>
                <label for="terms" style="display: inline; margin-left: 5px;">
                    我同意 <span class="required">*</span> <a href="#" onclick="alert('这是条款内容'); return false;">用户协议</a>
                </label>
            </div>
            
            <button type="submit">提交注册</button>
        </form>
        
        <div id="result"></div>
        
        <script>
            document.getElementById('registrationForm').addEventListener('submit', function(e) {
                e.preventDefault();
                
                const formData = new FormData(this);
                const data = {};
                
                for (let [key, value] of formData.entries()) {
                    if (data[key]) {
                        if (Array.isArray(data[key])) {
                            data[key].push(value);
                        } else {
                            data[key] = [data[key], value];
                        }
                    } else {
                        data[key] = value;
                    }
                }
                
                document.getElementById('result').innerHTML = 
                    '<div class="success">✅ 表单提交成功！<br>提交的数据：<pre>' + 
                    JSON.stringify(data, null, 2) + '</pre></div>';
            });
        </script>
    </body>
    </html>
    """
    
    # 保存测试页面
    with open('/workspace/myTest/test_form.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return os.path.abspath('/workspace/myTest/test_form.html')

def fill_registration_form():
    """填写注册表单示例"""
    
    print("📝 创建测试表单...")
    form_path = create_test_form_page()
    form_url = f"file://{form_path}"
    
    print(f"📄 表单路径: {form_url}")
    
    agent_executor, browser_service = create_form_agent()
    
    try:
        # 定义要填写的用户信息
        user_info = {
            "姓名": "张三",
            "邮箱": "zhangsan@example.com",
            "电话": "13800138000",
            "年龄": "25",
            "性别": "男",
            "兴趣": ["阅读", "运动"],
            "简介": "我是一个热爱学习的程序员，喜欢探索新技术。"
        }
        
        task = f"""
        请帮我填写注册表单，用户信息如下：
        {user_info}
        
        具体步骤：
        1. 打开表单页面: {form_url}
        2. 分析表单结构，识别所有字段
        3. 根据提供的用户信息填写表单：
           - 姓名: {user_info['姓名']}
           - 邮箱: {user_info['邮箱']}
           - 电话: {user_info['电话']}
           - 年龄: {user_info['年龄']}
           - 性别: 选择 "{user_info['性别']}"
           - 兴趣爱好: 勾选 {user_info['兴趣']}
           - 个人简介: {user_info['简介']}
           - 同意用户协议: 勾选
        4. 检查所有必填字段是否已填写
        5. 提交表单
        6. 确认提交结果
        
        请确保每个步骤都正确执行，并报告填写过程中的任何问题。
        """
        
        print("🤖 开始自动填写表单...")
        result = agent_executor.invoke({"input": task})
        
        print(f"✅ 表单填写完成！\n结果: {result['output']}")
        
    except Exception as e:
        print(f"❌ 填写表单时出现错误: {str(e)}")
    
    finally:
        browser_service.close()

def fill_custom_form(form_url, form_data):
    """填写自定义表单"""
    
    agent_executor, browser_service = create_form_agent()
    
    try:
        task = f"""
        请帮我填写位于 {form_url} 的表单。
        
        表单数据：
        {form_data}
        
        请按以下步骤操作：
        1. 打开表单页面
        2. 分析表单结构
        3. 根据提供的数据填写相应字段
        4. 处理任何验证错误
        5. 提交表单
        6. 报告结果
        """
        
        result = agent_executor.invoke({"input": task})
        return result['output']
        
    except Exception as e:
        print(f"❌ 填写表单时出现错误: {str(e)}")
        return None
    
    finally:
        browser_service.close()

def main():
    """主函数"""
    
    print("📝 LangChain Browser Use 表单填写示例")
    print("=" * 50)
    
    # 示例1：填写测试注册表单
    print("\n📋 示例1: 自动填写注册表单")
    fill_registration_form()
    
    print("\n" + "="*50)
    print("✅ 所有示例执行完成！")

if __name__ == "__main__":
    main()