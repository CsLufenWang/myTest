#!/usr/bin/env python3
"""
LangChain Browser Use 示例运行器
提供一个统一的入口来运行各种示例
"""

import sys
import os
from typing import Dict, Callable

def run_basic_example():
    """运行基础示例"""
    print("🚀 运行基础示例...")
    try:
        from basic_example import main
        main()
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保安装了所有依赖: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

def run_search_example():
    """运行搜索示例"""
    print("🔍 运行搜索示例...")
    try:
        from search_example import main
        main()
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保安装了所有依赖: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

def run_form_example():
    """运行表单示例"""
    print("📝 运行表单示例...")
    try:
        from form_example import main
        main()
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保安装了所有依赖: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

def run_advanced_example():
    """运行高级示例"""
    print("🎯 运行高级示例...")
    try:
        from advanced_example import main
        main()
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保安装了所有依赖: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

def interactive_search():
    """运行交互式搜索"""
    print("🔍 启动交互式搜索...")
    try:
        from search_example import interactive_search
        interactive_search()
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("请确保安装了所有依赖: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

def check_environment():
    """检查环境配置"""
    print("🔧 检查环境配置...")
    
    # 检查 Python 版本
    python_version = sys.version_info
    print(f"Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("⚠️ 警告: 建议使用 Python 3.8 或更高版本")
    
    # 检查必要的包
    required_packages = [
        'langchain',
        'langchain_openai',
        'browser_use',
        'playwright',
        'python_dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} 未安装")
    
    if missing_packages:
        print(f"\n📦 缺少以下包，请运行: pip install {' '.join(missing_packages)}")
    
    # 检查环境变量
    env_vars = ['OPENAI_API_KEY']
    for var in env_vars:
        if os.getenv(var):
            print(f"✅ {var} 已设置")
        else:
            print(f"❌ {var} 未设置")
    
    # 检查配置文件
    config_files = ['.env', 'config.json']
    for file in config_files:
        if os.path.exists(file):
            print(f"✅ {file} 存在")
        else:
            print(f"⚠️ {file} 不存在（可选）")

def show_help():
    """显示帮助信息"""
    help_text = """
🤖 LangChain Browser Use 示例运行器

用法: python run_examples.py [选项]

可用选项:
  basic       运行基础浏览器操作示例
  search      运行搜索示例
  form        运行表单填写示例
  advanced    运行高级自动化示例
  interactive 启动交互式搜索模式
  check       检查环境配置
  help        显示此帮助信息

示例:
  python run_examples.py basic
  python run_examples.py search
  python run_examples.py interactive

如果不提供参数，将显示交互式菜单。

📋 环境要求:
- Python 3.8+
- OpenAI API Key
- 安装所有依赖包: pip install -r requirements.txt

🔧 配置:
- 复制 .env.example 到 .env 并设置 API Key
- 根据需要修改 config.json 中的配置

📚 更多信息请查看 README.md
    """
    print(help_text)

def interactive_menu():
    """显示交互式菜单"""
    
    examples: Dict[str, Callable] = {
        "1": ("基础浏览器操作示例", run_basic_example),
        "2": ("搜索示例", run_search_example),
        "3": ("表单填写示例", run_form_example),
        "4": ("高级自动化示例", run_advanced_example),
        "5": ("交互式搜索", interactive_search),
        "6": ("检查环境配置", check_environment),
        "7": ("显示帮助", show_help)
    }
    
    while True:
        print("\n" + "="*50)
        print("🤖 LangChain Browser Use 示例")
        print("="*50)
        
        for key, (name, _) in examples.items():
            print(f"{key}. {name}")
        print("0. 退出")
        
        choice = input("\n请选择要运行的示例 (0-7): ").strip()
        
        if choice == "0":
            print("👋 再见！")
            break
        elif choice in examples:
            name, func = examples[choice]
            print(f"\n🎯 运行: {name}")
            print("-" * 30)
            try:
                func()
            except KeyboardInterrupt:
                print("\n⏹️ 用户中断")
            except Exception as e:
                print(f"❌ 运行出错: {e}")
            
            input("\n按 Enter 键继续...")
        else:
            print("❌ 无效选择，请重试")

def main():
    """主函数"""
    
    if len(sys.argv) < 2:
        # 没有参数，显示交互式菜单
        interactive_menu()
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        "basic": run_basic_example,
        "search": run_search_example,
        "form": run_form_example,
        "advanced": run_advanced_example,
        "interactive": interactive_search,
        "check": check_environment,
        "help": show_help
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"❌ 未知命令: {command}")
        print("运行 'python run_examples.py help' 查看可用命令")

if __name__ == "__main__":
    main()