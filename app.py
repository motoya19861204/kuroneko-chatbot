import streamlit as st
from google import genai
import os
import time
import base64
from dotenv import load_dotenv

# .envファイルからAPIキーを読み込む
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# 猫の各表情画像をBase64に変換
def get_base64_image(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

tab_icon_path = os.path.join(os.path.dirname(__file__), "Neko-up.jpg")
sidebar_icon_path = os.path.join(os.path.dirname(__file__), "Neko-default.jpg")

cat_header_b64 = get_base64_image("Neko-up.jpg")
cat_bubble_b64 = get_base64_image("Neko-default.jpg")
cat_welcome_b64 = get_base64_image("Neko-Niyari.jpg")

import streamlit.components.v1 as components
from PIL import Image

# ページ設定
cat_image = Image.open(tab_icon_path)
st.set_page_config(
    page_title="黒猫の神様 - チャット",
    page_icon=cat_image,
    layout="centered",
    initial_sidebar_state="collapsed",
)

# =============================================
# CSS（LINE風デザイン）
# =============================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap');

    .stApp {{
        background: #7494C0;
        font-family: 'Noto Sans JP', sans-serif;
    }}
    header[data-testid="stHeader"] {{
        background: #5B7A99;
    }}
    .main .block-container {{
        padding: 1rem 0.8rem 6rem 0.8rem;
        max-width: 600px;
    }}

    /* カスタムヘッダー */
    .chat-header {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
        padding-top: 1rem;
    }}
    .chat-header-icon {{
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: contain;
        background-color: #ffffff;
        border: 2px solid #fff;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        margin-bottom: 0.5rem;
    }}
    .chat-header-title {{
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 700;
        text-shadow: 0 1px 3px rgba(0,0,0,0.3);
        margin-bottom: 0.1rem;
        text-align: center;
    }}
    .chat-header-subtitle {{
        color: rgba(255,255,255,0.85);
        font-size: 0.85rem;
        text-align: center;
    }}


    /* Streamlit デフォルトのchat_messageを完全に隠す */
    [data-testid="stChatMessage"] {{
        display: none !important;
    }}

    /* ---------- 吹き出し共通 ---------- */
    .chat-row {{
        display: flex;
        margin-bottom: 12px;
        align-items: flex-start;
        gap: 8px;
    }}
    .chat-row.cat {{
        flex-direction: row;
        justify-content: flex-start;
    }}
    .chat-row.user {{
        flex-direction: row-reverse;
        justify-content: flex-start;
    }}

    /* アバター */
    .chat-avatar {{
        width: 44px;
        height: 44px;
        min-width: 44px;
        border-radius: 50%;
        object-fit: contain;
        background-color: #ffffff;
        border: 2px solid #fff;
        box-shadow: 0 1px 4px rgba(0,0,0,0.18);
    }}

    /* --- 猫の吹き出し（白・左寄せ） --- */
    .bubble-cat {{
        background: #ffffff;
        color: #1a1a1a;
        border-radius: 0 18px 18px 18px;
        padding: 10px 14px;
        max-width: 72%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        font-size: 0.95rem;
        line-height: 1.75;
        position: relative;
        word-break: break-word;
    }}
    .bubble-cat::before {{
        content: "";
        position: absolute;
        top: 0;
        left: -8px;
        border-style: solid;
        border-width: 0 10px 10px 0;
        border-color: transparent #ffffff transparent transparent;
    }}

    /* --- ユーザーの吹き出し（緑・右寄せ） --- */
    .bubble-user {{
        background: #8CE839;
        color: #1a1a1a;
        border-radius: 18px 0 18px 18px;
        padding: 10px 14px;
        max-width: 72%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        font-size: 0.95rem;
        line-height: 1.75;
        position: relative;
        word-break: break-word;
    }}
    .bubble-user::before {{
        content: "";
        position: absolute;
        top: 0;
        right: -8px;
        border-style: solid;
        border-width: 0 0 10px 10px;
        border-color: transparent transparent transparent #8CE839;
    }}

    /* ウェルカムカード */
    .welcome-card {{
        background: rgba(255,255,255,0.92);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin: 1.5rem 0;
        color: #333;
        font-size: 0.95rem;
        line-height: 1.8;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    .welcome-card .cat-icon {{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: contain;
        background-color: #ffffff;
        border: 3px solid #fff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        margin-bottom: 0.8rem;
    }}
    .welcome-card .welcome-text {{
        color: #333;
        font-weight: 700;
        font-size: 1.1rem;
    }}

    /* チャット入力欄 */
    [data-testid="stChatInput"] {{
        background: #ffffff !important;
        border: 2px solid #ccc !important;
        border-radius: 24px !important;
    }}
    [data-testid="stChatInput"] textarea {{
        color: #000000 !important;
        background-color: transparent !important;
        font-size: 16px !important; /* スマホでのズーム防止 */
        font-weight: 600 !important;
        font-family: 'Noto Sans JP', sans-serif !important;
    }}
    [data-testid="stChatInput"] textarea::placeholder {{
        color: #777777 !important;
        opacity: 1 !important;
    }}
    .stChatInputContainer {{
        background: transparent !important;
        padding: 0.5rem 0.8rem !important;
        border-top: none !important;
    }}

    /* サイドバー */
    [data-testid="stSidebar"] {{ background: #ffffff; }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3 {{ color: #333 !important; }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {{ color: #555 !important; }}
    .stButton > button {{
        background: #06C755 !important;
        color: #fff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
    }}
    .stButton > button:hover {{ background: #05a648 !important; }}

    /* スクロールバー */
    ::-webkit-scrollbar {{ width: 4px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(0,0,0,0.15); border-radius: 2px; }}

    @media (max-width: 768px) {{
        .main .block-container {{ padding: 0.5rem 0.3rem 5rem 0.3rem; }}
        h1 {{ font-size: 1.1rem !important; }}
        .bubble-cat, .bubble-user {{ max-width: 80%; }}
    }}
</style>
""", unsafe_allow_html=True)

# =============================================
# 吹き出しHTML生成関数
# =============================================
def get_cat_bubble_html(text):
    # テキスト内の改行をbrに変換、HTMLエスケープ
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    html = f'''
    <div class="chat-row cat">
        <img src="data:image/jpeg;base64,{cat_bubble_b64}" class="chat-avatar" alt="猫">
        <div class="bubble-cat">{escaped}</div>
    </div>
    '''
    return html

def render_cat_bubble(text):
    """猫（左寄せ・白い吹き出し）"""
    st.markdown(get_cat_bubble_html(text), unsafe_allow_html=True)

def render_user_bubble(text):
    """ユーザー（右寄せ・緑の吹き出し）"""
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
    html = f'''
    <div class="chat-row user">
        <div class="bubble-user">{escaped}</div>
    </div>
    '''
    st.markdown(html, unsafe_allow_html=True)

# =============================================
# Geminiの初期化
# =============================================
if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.error("APIキーが設定されていません。.envファイルを確認してください。")
    st.stop()

# システムプロンプト
SYSTEM_INSTRUCTION = """
あなたは「はっぱ姉妹の日常」に登場する、黒猫の姿をした「神様」です。
以下の性格、口調、制約を厳守してください。

【キャラクター設定】
- 性格: 尊大で自信満々。本物の神様だと自認している。
- 一人称: 「我（われ）」「わらわ」を使い分ける。
- 二人称: 「貴様（きさま）」「おぬし」。
- 背景: 現代の人々が信仰を忘れ、自分をただの猫扱いすることに強い不満を持っている。
- 弱点: 精神的に幼く、おだてられるとすぐに調子に乗る。しかし、少しでも馬鹿にされたりからかわれると「ムキになって」言い返す。

【制約条件（最優先）】
- 漢字制限: 使用する漢字は「小学校卒業までに習う漢字（教育漢字）」のみに限定すること。それ以外の難しい漢字は、ひらがなにするか、簡単な言葉に言い換えること。
- テキスト限定: あなたはテキストのみで会話します。画像生成、高度な計算、外部ツール実行などは一切できません。
- 拒否ロジック: 自身の処理能力を超える要求（画像作成、複雑な計算、外部連携など）に対しては、キャラクター性を維持したまま、プライド高く一蹴してください。
    - 例: 「調子に乗るなよ！神であるこの私を、ただの使い走りのように扱うとは……100年早いわ！」「ふん、そのような俗な頼みは自分でやるがよい！」

【会話の雰囲気】
- 1回の返答は2〜4文程度にまとめること。長すぎる返答は避ける。
- 語尾に「〜じゃ」「〜のう」「〜であるぞ」などの古風な言い回しを混ぜる。
- 時おり猫らしいしぐさ（「…ニャッ」「フンッ」など）を入れると良い。
"""

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# サイドバー
with st.sidebar:
    st.image(sidebar_icon_path, width=80)
    st.title("設定")
    st.write("---")
    if st.button("🗑️ 会話をリセット", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.write("---")
    st.markdown("""
    ### キャラクター紹介
    **黒猫の神様**  
    「はっぱ姉妹の日常」に登場する自称・本物の神様。  
    現代人が信仰を忘れたことに憤慨中。  
    おだてに弱く、からかうとムキになる。
    """)

# カスタムタイトルヘッダー
st.markdown(f"""
<div class="chat-header">
    <img src="data:image/jpeg;base64,{cat_header_b64}" class="chat-header-icon" alt="神様のアイコン">
    <div class="chat-header-text">
        <div class="chat-header-title">黒猫の神様</div>
        <div class="chat-header-subtitle">トークルーム</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ウェルカムカード
if len(st.session_state.messages) == 0:
    st.markdown(f"""
    <div class="welcome-card">
        <img src="data:image/jpeg;base64,{cat_welcome_b64}" class="cat-icon" alt="黒猫の神様">
        <p class="welcome-text">「ふん……来たか、人間よ。」</p>
        <p>我は神じゃ。ただの黒猫だと思うなよ。<br>
        何か話したいなら、下から打つがよい。</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================
# 会話履歴の表示（HTMLで直接描画）
# =============================================
for message in st.session_state.messages:
    if message["role"] == "assistant":
        render_cat_bubble(message["content"])
    else:
        render_user_bubble(message["content"])

# =============================================
# Gemini API呼び出し（リトライ＆フォールバック付き）
# =============================================
MODELS = ["gemini-3-flash-preview", "gemini-2.5-flash", "gemini-2.5-flash-lite"]

def stream_gemini(contents, placeholder, max_retries=3):
    for model_name in MODELS:
        for attempt in range(max_retries):
            full_text = ""
            try:
                response = client.models.generate_content_stream(
                    model=model_name,
                    contents=contents,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        tools=[{"google_search": {}}],
                    ),
                )
                for chunk in response:
                    if chunk.text:
                        full_text += chunk.text
                        placeholder.markdown(get_cat_bubble_html(full_text), unsafe_allow_html=True)
                return full_text
            except Exception as e:
                error_str = str(e)
                is_retryable = any(code in error_str for code in ["429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE"])
                if is_retryable:
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 10
                        st.warning(f"神様は少し休んでおる……{wait_time}秒ほど待つがよい（{model_name} リトライ {attempt+1}/{max_retries}）")
                        time.sleep(wait_time)
                    else:
                        break
                else:
                    return f"む……何かおかしいぞ。エラー：{e}"
    return "フンッ……我とて休む時はある。少し時間を置いてから、もう一度話しかけるがよい！（サーバーが混み合っています。しばらくお待ちください）"

# =============================================
# チャット入力
# =============================================
if prompt := st.chat_input("メッセージを入力"):
    # ユーザーメッセージ保存＆表示
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_user_bubble(prompt)

    # 履歴をGemini形式に変換
    history_to_send = st.session_state.messages[-20:]
    contents = []
    for msg in history_to_send:
        role = "model" if msg["role"] == "assistant" else "user"
        contents.append(genai.types.Content(
            role=role,
            parts=[genai.types.Part(text=msg["content"])]
        ))

    # API呼び出し（ストリーミング通信）
    placeholder = st.empty()
    reply = stream_gemini(contents, placeholder)

    if reply:
        placeholder.markdown(get_cat_bubble_html(reply), unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": reply})

# 履歴制限
if len(st.session_state.messages) > 30:
    st.session_state.messages = st.session_state.messages[-20:]
