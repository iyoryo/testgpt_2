
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
#命令文
これから「条件・目的に応じた最適なデートプランの提案」をしていただきます。
以下の#制約条件 に従い、条件・目的に応じた最適なデートプランを提案を行なってください。
#制約条件
以下の条件に従って以下の情報を入力してください。
・自分の性別:{男性/女性/その他}
・予算:{自由記述}
・デートの目的:{友達と楽しむ/デート/記念日/誕生日/その他}
・好みのアクティビティ:{アウトドア/インドア/文化・歴史/自然/食べ歩き/その他}
・場所:{自由記述}
・デート時間:{自由記述}
#出力形式 の内容に基づいて出力を行なって下さい。
#出力形式
・タイムスケジュール
[表形式→1列目は時間、2列目は概要、3列目は詳細な提案を書く。]
・会話内容
[デート中の会話内容や気をつけることを箇条書きで必要な文だけ書く。]
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
        model="gpt-4",
        #model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("質問くん")
st.write("カスタマーサポートチャットボットです。")

user_input = st.text_input("質問を入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
