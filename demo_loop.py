#!/usr/bin/env python3
"""演示 Agent Loop 工作过程"""

import os
import subprocess
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv(override=True)
if os.getenv("ANTHROPIC_BASE_URL"):
    os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

client = Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"))
MODEL = os.environ["MODEL_ID"]

# 工具定义
TOOLS = [{
    "name": "bash",
    "description": "Run a shell command.",
    "input_schema": {
        "type": "object",
        "properties": {"command": {"type": "string"}},
        "required": ["command"],
    },
}]

def run_bash(command: str) -> str:
    try:
        r = subprocess.run(command, shell=True, cwd=os.getcwd(),
                           capture_output=True, text=True, timeout=30)
        out = (r.stdout + r.stderr).strip()
        return out[:2000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout"

# ===== 演示开始 =====
print("=" * 60)
print("【演示】Agent Loop 工作过程")
print("=" * 60)

# 任务：列出当前目录的 Python 文件
user_query = "List all .py files in the current directory"
print(f"\n用户输入: {user_query}")
print("-" * 60)

# 初始化消息
messages = [{"role": "user", "content": user_query}]

# 循环计数
loop_count = 0

while True:
    loop_count += 1
    print(f"\n=== 第 {loop_count} 轮循环 ===")
    print("-" * 40)

    # ① 调用 LLM
    print("  1. 调用 LLM...")
    response = client.messages.create(
        model=MODEL,
        system="You are a coding agent. Use bash to solve tasks.",
        messages=messages,
        tools=TOOLS,
        max_tokens=1000,
    )

    # ② 追加助手响应
    messages.append({"role": "assistant", "content": response.content})

    # ③ 检查 stop_reason
    print(f"  2. stop_reason = {response.stop_reason}")

    if response.stop_reason != "tool_use":
        print("  3. LLM 没有调用工具 -> 任务完成!")
        # 打印最终回复
        for block in response.content:
            if hasattr(block, 'text'):
                print(f"\n[LLM 最终回复]\n{block.text}")
        break

    # ④ 执行工具
    print("  3. LLM 要调用工具!")
    results = []
    for block in response.content:
        if block.type == "tool_use":
            cmd = block.input["command"]
            print(f"  4. 执行命令: {cmd}")
            output = run_bash(cmd)
            print(f"  5. 工具结果: {output[:150]}...")
            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": output,
            })

    # ⑤ 追加结果
    messages.append({"role": "user", "content": results})
    print("  6. 结果追加到 messages，继续下一轮...")

print("\n" + "=" * 60)
print(f"任务完成! 总共用了 {loop_count} 轮循环")
print("=" * 60)
