"""
工具函数模块
提供通用的浏览器自动化工具函数
"""

import os
import time
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from browser_use.browser.browser import BrowserConfig
from browser_use.agent.service import BrowserUseService

class BrowserUtils:
    """浏览器工具类"""
    
    @staticmethod
    def create_browser_service(headless: bool = False, 
                             browser_type: str = "chromium",
                             window_width: int = 1920,
                             window_height: int = 1080) -> BrowserUseService:
        """创建浏览器服务"""
        
        config = BrowserConfig(
            headless=headless,
            browser_type=browser_type,
            window_width=window_width,
            window_height=window_height
        )
        
        return BrowserUseService(config=config)
    
    @staticmethod
    def wait_for_element(browser_service, selector: str, timeout: int = 10) -> bool:
        """等待元素出现"""
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # 这里需要根据实际的 browser_use API 来实现
                # 这是一个示例实现
                return True
            except:
                time.sleep(0.5)
        
        return False
    
    @staticmethod
    def safe_click(browser_service, selector: str, timeout: int = 10) -> bool:
        """安全点击元素"""
        
        if BrowserUtils.wait_for_element(browser_service, selector, timeout):
            try:
                # 实际的点击实现
                return True
            except Exception as e:
                print(f"点击失败: {e}")
                return False
        
        return False

class DataExtractor:
    """数据提取工具类"""
    
    @staticmethod
    def extract_text_content(html: str, selector: str) -> List[str]:
        """从HTML中提取文本内容"""
        
        # 这里可以使用 BeautifulSoup 或其他HTML解析库
        # 这是一个简化的示例
        return []
    
    @staticmethod
    def extract_links(html: str, base_url: str = "") -> List[Dict[str, str]]:
        """提取页面中的链接"""
        
        # 实现链接提取逻辑
        return []
    
    @staticmethod
    def extract_images(html: str, base_url: str = "") -> List[Dict[str, str]]:
        """提取页面中的图片"""
        
        # 实现图片提取逻辑
        return []

class FormHelper:
    """表单操作助手"""
    
    @staticmethod
    def detect_form_fields(html: str) -> List[Dict[str, Any]]:
        """检测表单字段"""
        
        fields = []
        # 实现表单字段检测逻辑
        # 返回字段信息：类型、名称、是否必填等
        
        return fields
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱格式"""
        
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """验证手机号格式"""
        
        import re
        pattern = r'^1[3-9]\d{9}$'
        return re.match(pattern, phone) is not None

class TaskLogger:
    """任务日志记录器"""
    
    def __init__(self, log_file: str = "browser_automation.log"):
        self.log_file = log_file
        self.logs = []
    
    def log(self, level: str, message: str, data: Optional[Dict] = None):
        """记录日志"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "data": data or {}
        }
        
        self.logs.append(log_entry)
        
        # 打印到控制台
        print(f"[{level}] {message}")
        
        # 写入文件
        self._write_to_file(log_entry)
    
    def info(self, message: str, data: Optional[Dict] = None):
        """记录信息日志"""
        self.log("INFO", message, data)
    
    def warning(self, message: str, data: Optional[Dict] = None):
        """记录警告日志"""
        self.log("WARNING", message, data)
    
    def error(self, message: str, data: Optional[Dict] = None):
        """记录错误日志"""
        self.log("ERROR", message, data)
    
    def success(self, message: str, data: Optional[Dict] = None):
        """记录成功日志"""
        self.log("SUCCESS", message, data)
    
    def _write_to_file(self, log_entry: Dict):
        """写入日志文件"""
        
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"写入日志文件失败: {e}")
    
    def save_summary(self, output_file: str = "task_summary.json"):
        """保存任务摘要"""
        
        summary = {
            "total_logs": len(self.logs),
            "levels": {},
            "start_time": self.logs[0]["timestamp"] if self.logs else None,
            "end_time": self.logs[-1]["timestamp"] if self.logs else None,
            "logs": self.logs
        }
        
        # 统计各级别日志数量
        for log in self.logs:
            level = log["level"]
            summary["levels"][level] = summary["levels"].get(level, 0) + 1
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"任务摘要已保存到: {output_file}")

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """加载配置文件"""
        
        default_config = {
            "browser": {
                "headless": False,
                "browser_type": "chromium",
                "window_width": 1920,
                "window_height": 1080,
                "timeout": 30
            },
            "openai": {
                "model": "gpt-4",
                "temperature": 0.1,
                "max_tokens": 2000
            },
            "automation": {
                "retry_count": 3,
                "retry_delay": 2,
                "screenshot_on_error": True,
                "save_html_on_error": True
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # 合并配置
                    self._merge_config(default_config, user_config)
            except Exception as e:
                print(f"加载配置文件失败，使用默认配置: {e}")
        
        return default_config
    
    def _merge_config(self, default: Dict, user: Dict):
        """合并配置"""
        
        for key, value in user.items():
            if key in default:
                if isinstance(value, dict) and isinstance(default[key], dict):
                    self._merge_config(default[key], value)
                else:
                    default[key] = value
            else:
                default[key] = value
    
    def get(self, key_path: str, default=None):
        """获取配置值"""
        
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value):
        """设置配置值"""
        
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def save(self):
        """保存配置到文件"""
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print(f"配置已保存到: {self.config_file}")
        except Exception as e:
            print(f"保存配置失败: {e}")

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.checkpoints = []
    
    def start(self):
        """开始监控"""
        self.start_time = time.time()
        self.checkpoints = []
    
    def checkpoint(self, name: str):
        """添加检查点"""
        if self.start_time is None:
            self.start()
        
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        self.checkpoints.append({
            "name": name,
            "timestamp": current_time,
            "elapsed": elapsed
        })
        
        print(f"⏱️ {name}: {elapsed:.2f}s")
    
    def end(self):
        """结束监控"""
        self.end_time = time.time()
        total_time = self.end_time - self.start_time if self.start_time else 0
        
        print(f"🏁 总执行时间: {total_time:.2f}s")
        return total_time
    
    def get_report(self) -> Dict:
        """获取性能报告"""
        
        if not self.start_time:
            return {"error": "监控未开始"}
        
        total_time = (self.end_time or time.time()) - self.start_time
        
        return {
            "total_time": total_time,
            "checkpoints": self.checkpoints,
            "average_checkpoint_time": total_time / len(self.checkpoints) if self.checkpoints else 0
        }

# 全局实例
logger = TaskLogger()
config = ConfigManager()
monitor = PerformanceMonitor()

# 导出常用函数
__all__ = [
    'BrowserUtils',
    'DataExtractor', 
    'FormHelper',
    'TaskLogger',
    'ConfigManager',
    'PerformanceMonitor',
    'logger',
    'config',
    'monitor'
]