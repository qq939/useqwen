# ===== 全局参数：集中放文件最上边，方便修改 =====
BASE_URL = "http://localhost:1234/v1"            # 第14行使用：ChatOpenAI 的 base_url（本地 OpenAI 兼容地址）
API_KEY = "lm-studio"                            # 第14行使用：本地服务不校验 key，随便填
MODEL = "qwen/qwen3.8-27b"                       # 第14行使用：ChatOpenAI 的 model，和你 curl 里的一致
SYSTEM_PROMPT = "You answer only in rhymes."     # 第15行使用：作为 system 消息
USER_INPUT = "What is your favorite color?"      # 第13行使用：命令行没给问题时的默认问题

import sys                                       # 第13行使用：读取命令行后面跟的问题
from langchain_openai import ChatOpenAI          # 第14行使用：LangChain 的 OpenAI 兼容客户端


def main():
    question = " ".join(sys.argv[1:]) or USER_INPUT  # 命令行后面跟的问题，如 python qwen_chat.py 你最喜欢的颜色？
    llm = ChatOpenAI(base_url=BASE_URL, api_key=API_KEY, model=MODEL, timeout=120)  # timeout=120：本地模型较慢，给 120 秒，超时就报错不会一直卡住
    messages = [("system", SYSTEM_PROMPT), ("human", question)]
    print(llm.invoke(messages).content)


if __name__ == "__main__":
    main()
