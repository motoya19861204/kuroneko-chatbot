# 黒猫チャットボット（仮）

Google Gemini APIとStreamlitを活用した、黒猫の神様（はっぱ姉妹の日常）とチャットができるアプリです。

## 起動方法

1. **環境構築**
   ```bash
   pip install -r requirements.txt
   ```

2. **APIキーの設定**
   `.env.example` を `.env` にリネームし、Google Gemini APIのキーを入力してください。
   ```env
   GEMINI_API_KEY=あなたのAPIキー
   ```

3. **アプリの起動**
   ```bash
   streamlit run app.py
   ```

## 特徴
- **キャラクター完全再現**: 尊大で自信満々、でもおだてに弱い「黒猫の神様」をGemini 1.5 Flashで再現。
- **漢字制限**: 小学校卒業までに習う漢字（教育漢字）のみを使用するように制御。
- **PWA対応**: manifest.jsonを同梱。
- **セッション管理**: 直近10往復の会話をコンテキストとして保持。
- **ガードレール**: 画像生成や複雑な計算は神様のプライドにかけて拒否します。
