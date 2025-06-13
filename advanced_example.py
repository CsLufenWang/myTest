"""
高级示例 - 复杂的多步骤浏览器自动化任务
演示如何使用 LangChain + Browser Use 处理复杂的工作流程
"""

import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from browser_use.agent.service import BrowserUseService
from browser_use.browser.browser import BrowserConfig

# 加载环境变量
load_dotenv()

class TaskResult:
    """任务结果类"""
    def __init__(self, task_name, success=False, data=None, error=None):
        self.task_name = task_name
        self.success = success
        self.data = data or {}
        self.error = error
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "task_name": self.task_name,
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "timestamp": self.timestamp
        }

def create_advanced_agent():
    """创建高级浏览器自动化 Agent"""
    
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.1,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    browser_config = BrowserConfig(
        headless=False,
        browser_type="chromium",
        window_width=1920,
        window_height=1080
    )
    
    browser_service = BrowserUseService(config=browser_config)
    tools = browser_service.get_tools()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个高级的网页自动化专家。你具备以下能力：

        🎯 任务规划：
        - 将复杂任务分解为可执行的步骤
        - 识别任务依赖关系和执行顺序
        - 处理异常情况和错误恢复

        🔍 智能分析：
        - 深度分析网页结构和内容
        - 识别动态加载的元素
        - 处理单页应用(SPA)和AJAX请求

        🛠️ 高级操作：
        - 处理复杂的用户交互流程
        - 管理多个标签页和窗口
        - 处理文件上传和下载
        - 截图和数据提取

        📊 数据处理：
        - 结构化数据提取
        - 数据验证和清洗
        - 结果格式化和报告

        ⚡ 性能优化：
        - 智能等待策略
        - 并行处理能力
        - 资源管理和清理

        执行原则：
        1. 始终先分析页面结构
        2. 使用显式等待而非固定延时
        3. 实现错误处理和重试机制
        4. 提供详细的执行日志
        5. 确保资源正确释放
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
        max_iterations=20
    )
    
    return agent_executor, browser_service

def research_task_workflow():
    """复杂的研究任务工作流程"""
    
    print("🔬 执行复杂研究任务工作流程...")
    
    agent_executor, browser_service = create_advanced_agent()
    results = []
    
    try:
        # 任务1：技术趋势研究
        print("\n📊 任务1: 技术趋势研究")
        task1 = """
        请执行以下研究任务：
        
        1. 访问 GitHub Trending (https://github.com/trending)
        2. 提取今日热门项目信息：
           - 项目名称和描述
           - 编程语言
           - Star 数量
           - 今日新增 Star 数
        3. 分析前10个项目的技术栈分布
        4. 生成技术趋势报告
        
        请确保数据准确性，并提供结构化的结果。
        """
        
        result1 = agent_executor.invoke({"input": task1})
        results.append(TaskResult("GitHub趋势分析", True, {"report": result1['output']}))
        
        # 任务2：竞品分析
        print("\n🏢 任务2: 竞品分析")
        task2 = """
        请执行竞品分析任务：
        
        1. 搜索 "AI代码助手" 相关产品
        2. 访问前5个产品的官网
        3. 提取以下信息：
           - 产品名称和定位
           - 主要功能特性
           - 价格信息
           - 用户评价
        4. 生成竞品对比表格
        
        请使用多个搜索引擎确保信息全面性。
        """
        
        result2 = agent_executor.invoke({"input": task2})
        results.append(TaskResult("竞品分析", True, {"analysis": result2['output']}))
        
        # 任务3：数据收集和整理
        print("\n📈 任务3: 数据收集和整理")
        task3 = """
        基于前面的研究结果，请：
        
        1. 整合所有收集的数据
        2. 识别关键趋势和模式
        3. 生成执行摘要
        4. 提出3-5个可行的建议
        5. 创建数据可视化建议
        
        请确保分析的逻辑性和实用性。
        """
        
        result3 = agent_executor.invoke({"input": task3})
        results.append(TaskResult("数据整合分析", True, {"summary": result3['output']}))
        
        # 保存结果
        save_results(results)
        
        print("✅ 所有研究任务完成！")
        return results
        
    except Exception as e:
        error_result = TaskResult("研究工作流程", False, error=str(e))
        results.append(error_result)
        print(f"❌ 研究任务出现错误: {str(e)}")
        return results
    
    finally:
        browser_service.close()

def ecommerce_automation_workflow():
    """电商自动化工作流程示例"""
    
    print("🛒 执行电商自动化工作流程...")
    
    agent_executor, browser_service = create_advanced_agent()
    results = []
    
    try:
        # 创建测试电商页面
        create_test_ecommerce_page()
        
        # 任务：完整的购物流程
        task = """
        请执行完整的电商购物流程测试：
        
        1. 访问测试电商网站
        2. 浏览商品分类
        3. 搜索特定商品
        4. 查看商品详情
        5. 添加商品到购物车
        6. 修改购物车数量
        7. 进入结账流程
        8. 填写配送信息
        9. 选择支付方式
        10. 确认订单（不实际支付）
        
        请记录每个步骤的执行情况和遇到的问题。
        """
        
        result = agent_executor.invoke({"input": task})
        results.append(TaskResult("电商购物流程测试", True, {"workflow": result['output']}))
        
        return results
        
    except Exception as e:
        error_result = TaskResult("电商自动化", False, error=str(e))
        results.append(error_result)
        return results
    
    finally:
        browser_service.close()

def create_test_ecommerce_page():
    """创建测试电商页面"""
    
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>测试电商网站</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial, sans-serif; }
            .header { background: #333; color: white; padding: 1rem; }
            .nav { display: flex; justify-content: space-between; align-items: center; }
            .search-box { padding: 0.5rem; margin: 0 1rem; }
            .cart { background: #007bff; color: white; padding: 0.5rem 1rem; text-decoration: none; border-radius: 4px; }
            .categories { display: flex; background: #f8f9fa; padding: 1rem; }
            .category { margin-right: 2rem; cursor: pointer; }
            .products { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; padding: 2rem; }
            .product { border: 1px solid #ddd; padding: 1rem; text-align: center; }
            .product img { width: 100%; height: 200px; object-fit: cover; }
            .btn { background: #007bff; color: white; padding: 0.5rem 1rem; border: none; cursor: pointer; margin: 0.5rem; }
            .btn:hover { background: #0056b3; }
            #cart-items { margin: 2rem; }
            .cart-item { display: flex; justify-content: space-between; align-items: center; padding: 1rem; border-bottom: 1px solid #eee; }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="nav">
                <h1>测试电商</h1>
                <input type="text" class="search-box" placeholder="搜索商品..." id="searchBox">
                <a href="#" class="cart" onclick="showCart()">购物车 (<span id="cartCount">0</span>)</a>
            </div>
        </div>
        
        <div class="categories">
            <div class="category" onclick="filterProducts('all')">全部</div>
            <div class="category" onclick="filterProducts('electronics')">电子产品</div>
            <div class="category" onclick="filterProducts('clothing')">服装</div>
            <div class="category" onclick="filterProducts('books')">图书</div>
        </div>
        
        <div class="products" id="products">
            <div class="product" data-category="electronics" data-name="智能手机">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7miYvmnLo8L3RleHQ+PC9zdmc+" alt="智能手机">
                <h3>智能手机</h3>
                <p>最新款智能手机，性能强劲</p>
                <p>价格: ¥2999</p>
                <button class="btn" onclick="addToCart('智能手机', 2999)">加入购物车</button>
            </div>
            
            <div class="product" data-category="electronics" data-name="笔记本电脑">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7nrJTorrDmnKw8L3RleHQ+PC9zdmc+" alt="笔记本电脑">
                <h3>笔记本电脑</h3>
                <p>轻薄便携，办公首选</p>
                <p>价格: ¥5999</p>
                <button class="btn" onclick="addToCart('笔记本电脑', 5999)">加入购物车</button>
            </div>
            
            <div class="product" data-category="clothing" data-name="T恤">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5U5oGkPC90ZXh0Pjwvc3ZnPg==" alt="T恤">
                <h3>纯棉T恤</h3>
                <p>舒适透气，多色可选</p>
                <p>价格: ¥99</p>
                <button class="btn" onclick="addToCart('纯棉T恤', 99)">加入购物车</button>
            </div>
            
            <div class="product" data-category="books" data-name="编程书籍">
                <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtc2l6ZT0iMTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj7kuabnsY08L3RleHQ+PC9zdmc+" alt="编程书籍">
                <h3>Python编程指南</h3>
                <p>从入门到精通</p>
                <p>价格: ¥89</p>
                <button class="btn" onclick="addToCart('Python编程指南', 89)">加入购物车</button>
            </div>
        </div>
        
        <div id="cart-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000;">
            <div style="background: white; margin: 50px auto; padding: 20px; width: 80%; max-width: 600px;">
                <h2>购物车</h2>
                <div id="cart-items"></div>
                <div style="text-align: right; margin-top: 20px;">
                    <strong>总计: ¥<span id="total">0</span></strong>
                </div>
                <div style="margin-top: 20px;">
                    <button class="btn" onclick="checkout()">去结账</button>
                    <button class="btn" onclick="closeCart()" style="background: #6c757d;">关闭</button>
                </div>
            </div>
        </div>
        
        <script>
            let cart = [];
            
            function addToCart(name, price) {
                const existingItem = cart.find(item => item.name === name);
                if (existingItem) {
                    existingItem.quantity += 1;
                } else {
                    cart.push({ name, price, quantity: 1 });
                }
                updateCartCount();
                alert(name + ' 已添加到购物车！');
            }
            
            function updateCartCount() {
                const count = cart.reduce((sum, item) => sum + item.quantity, 0);
                document.getElementById('cartCount').textContent = count;
            }
            
            function showCart() {
                const cartItems = document.getElementById('cart-items');
                cartItems.innerHTML = '';
                let total = 0;
                
                cart.forEach((item, index) => {
                    total += item.price * item.quantity;
                    cartItems.innerHTML += `
                        <div class="cart-item">
                            <span>${item.name}</span>
                            <span>¥${item.price} x ${item.quantity}</span>
                            <button onclick="removeFromCart(${index})" style="background: #dc3545; color: white; border: none; padding: 5px;">删除</button>
                        </div>
                    `;
                });
                
                document.getElementById('total').textContent = total;
                document.getElementById('cart-modal').style.display = 'block';
            }
            
            function closeCart() {
                document.getElementById('cart-modal').style.display = 'none';
            }
            
            function removeFromCart(index) {
                cart.splice(index, 1);
                updateCartCount();
                showCart();
            }
            
            function checkout() {
                if (cart.length === 0) {
                    alert('购物车为空！');
                    return;
                }
                alert('跳转到结账页面...');
                closeCart();
            }
            
            function filterProducts(category) {
                const products = document.querySelectorAll('.product');
                products.forEach(product => {
                    if (category === 'all' || product.dataset.category === category) {
                        product.style.display = 'block';
                    } else {
                        product.style.display = 'none';
                    }
                });
            }
            
            document.getElementById('searchBox').addEventListener('input', function(e) {
                const searchTerm = e.target.value.toLowerCase();
                const products = document.querySelectorAll('.product');
                
                products.forEach(product => {
                    const name = product.dataset.name.toLowerCase();
                    if (name.includes(searchTerm)) {
                        product.style.display = 'block';
                    } else {
                        product.style.display = 'none';
                    }
                });
            });
        </script>
    </body>
    </html>
    """
    
    with open('/workspace/myTest/test_ecommerce.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

def save_results(results):
    """保存任务结果到文件"""
    
    results_data = [result.to_dict() for result in results]
    
    with open('/workspace/myTest/task_results.json', 'w', encoding='utf-8') as f:
        json.dump(results_data, f, ensure_ascii=False, indent=2)
    
    print(f"📄 结果已保存到: /workspace/myTest/task_results.json")

def main():
    """主函数"""
    
    print("🚀 LangChain Browser Use 高级示例")
    print("=" * 60)
    
    # 选择要执行的工作流程
    workflows = {
        "1": ("技术趋势研究工作流程", research_task_workflow),
        "2": ("电商自动化工作流程", ecommerce_automation_workflow)
    }
    
    print("\n可用的工作流程:")
    for key, (name, _) in workflows.items():
        print(f"{key}. {name}")
    
    choice = input("\n请选择要执行的工作流程 (1-2): ").strip()
    
    if choice in workflows:
        workflow_name, workflow_func = workflows[choice]
        print(f"\n🎯 执行: {workflow_name}")
        print("-" * 40)
        
        start_time = time.time()
        results = workflow_func()
        end_time = time.time()
        
        print(f"\n⏱️ 执行时间: {end_time - start_time:.2f} 秒")
        print(f"📊 任务结果: {len([r for r in results if r.success])} 成功, {len([r for r in results if not r.success])} 失败")
        
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()