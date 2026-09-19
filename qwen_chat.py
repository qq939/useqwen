# ===== 全局参数：集中放文件最上边，方便修改 =====
BASE_URL = "http://localhost:1234/v1"            # 第13行使用：ChatOpenAI 的 base_url（本地 OpenAI 兼容地址）
API_KEY = "lm-studio"                            # 第13行使用：本地服务不校验 key，随便填
MODEL = "qwen/qwen3.8-27b"                       # 第13行使用：ChatOpenAI 的 model，和你 curl 里的一致
SYSTEM_PROMPT = "You answer only in rhymes."     # 第14行使用：作为 system 消息
USER_INPUT = "What is your favorite color?"      # 第14行使用：作为 human 消息

from langchain_openai import ChatOpenAI          # 第13行使用：LangChain 的 OpenAI 兼容客户端


def main():
    llm = ChatOpenAI(base_url=BASE_URL, api_key=API_KEY, model=MODEL)
    messages = [("system", SYSTEM_PROMPT), ("human", USER_INPUT)]
    print(llm.invoke(messages).content)


if __name__ == "__main__":
    main()
