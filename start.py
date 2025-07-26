#!/usr/bin/env python3
"""
AI对话系统启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import fastapi
        import uvicorn
        import requests
        import pydub
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_env_file():
    """检查环境变量文件"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  未找到.env文件")
        print("正在创建.env文件...")
        
        # 复制示例文件
        example_file = Path(".env.example")
        if example_file.exists():
            with open(example_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ 已创建.env文件")
            print("请编辑.env文件并配置你的API密钥和模型路径")
            return False
        else:
            print("❌ 未找到.env.example文件")
            return False
    
    return True

def create_directories():
    """创建必要的目录"""
    directories = ["output", "models"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ 目录结构已创建")

def main():
    """主函数"""
    print("🤖 AI对话系统启动器")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查环境文件
    if not check_env_file():
        print("\n📝 请配置.env文件后重新运行")
        return
    
    # 创建目录
    create_directories()
    
    print("\n🎯 选择启动模式:")
    print("1. Web界面模式 (推荐)")
    print("2. 命令行模式")
    print("3. 系统测试")
    print("4. 退出")
    
    while True:
        try:
            choice = input("\n请输入选择 (1-4): ").strip()
            
            if choice == "1":
                print("\n🚀 启动Web界面...")
                print("📱 访问地址: http://localhost:8000")
                print("🔧 API文档: http://localhost:8000/docs")
                print("按 Ctrl+C 停止服务器")
                subprocess.run([sys.executable, "main.py"])
                break
                
            elif choice == "2":
                print("\n🚀 启动命令行模式...")
                subprocess.run([sys.executable, "main.py", "--cli"])
                break
                
            elif choice == "3":
                print("\n🔍 运行系统测试...")
                subprocess.run([sys.executable, "test_system.py"])
                break
                
            elif choice == "4":
                print("👋 再见！")
                break
                
            else:
                print("❌ 无效选择，请输入 1-4")
                
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main() 