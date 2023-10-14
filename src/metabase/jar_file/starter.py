import os
import re
import subprocess
import webbrowser
from pathlib import Path
from shutil import which

# 先检查 Java 是否安装
if which("java") is None:
    raise EnvironmentError("Java 没有安装在这台机器上。请先安装 Java。"
                           "https://www.java.com/zh-CN/download/")

# 定义 JAR 文件的路径
jar_path = Path(__file__).parent / 'metabase.jar'
jar_path = jar_path.resolve()  # 获取绝对路径
print(f"JAR 文件路径: {jar_path}")


def reset_password(email: str):
    command = f"java -Dfile.encoding=UTF-8 -jar {jar_path}  reset-password {email}"

    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    # 等待命令执行完成
    stdout, stderr = process.communicate()

    # 从输出中提取 token
    token_pattern = re.compile(r"\[\[\[([\w-]+)\]\]\]")
    match = token_pattern.search(stdout.decode('utf-8', errors='ignore'))

    if match:
        # 提取 token
        token = match.group(1)

        # 生成 URL
        url = f"https://metabase.example.com/auth/reset_password/{token}"

        # 自动在浏览器中打开 URL
        webbrowser.open(url)
    else:
        print("无法从输出中提取 token。")


def start_metabase(port: int = 3008):
    try:
        print("启动 Metabase...")
        print(f"启动 Metabase 在端口 {port}...")

        # 设置环境变量
        os.environ['MB_JETTY_PORT'] = str(port)

        proc = subprocess.Popen(
            ["java", "-Dfile.encoding=UTF-8", "-jar", jar_path.as_posix()],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # 使输出为文本格式，而不是二进制格式
            encoding='utf-8',  # 显式设置编码
            errors='replace'  # 替换无法解码的字符
        )
        while True:
            output = proc.stdout.readline()
            if output == '' and proc.poll() is not None:
                break
            if output:
                print(f"stdout: {output.strip()}")

        return_code = proc.wait()
        if return_code != 0:
            print(f"Metabase failed to start. Return code: {return_code}")
        else:
            print("启动 Metabase 成功: http://localhost:3008")
    except FileNotFoundError:
        print("系统找不到指定的文件。请确保 Java 已经安装并且可在命令行中运行。")
    except Exception as e:
        print(f"发生未知错误: {e}")
    finally:
        #         关闭进程
        proc.terminate()


if __name__ == "__main__":
    start_metabase(3008)
    # reset_password("zhouge1831@gmail")
