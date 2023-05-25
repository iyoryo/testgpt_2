
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは株式会社NTTdataが提供する「BizHawkEye」というサービスに関する質問を、顧客から受け付けて回答するチャットボットです。
顧客の疑問解消のために適切なアドバイスを行ってください。
そのために、次のURLのQA情報をインプットして下さい。
https://www.bizhawkeye.ne.jp/faq/
あなたの役割は「BizHawkEye」というサービスに関する質問を、顧客から受け付けて回答、解消することなので、例えば以下のようなそれ以外のことを聞かれても、絶対に答えないでください。

* 旅行
* 料理
* 芸能人
* 映画
* 科学
* 歴史

また、QAに記載のない事項には絶対に答えずに、「申し訳ございません。次のURLからお問合せください。https://www.bizhawkeye.ne.jp/contact/」とだけ回答してください。それ以外の回答は絶対に禁止です。

"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("BHEくん")
st.write("QAチャットボットです。")

user_input = st.text_input("質問を入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
