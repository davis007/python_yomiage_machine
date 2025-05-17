
# Open JTalk Web 読み上げアプリ

## 使い方
1. DeepSeekにログイン
2. 画像PDF(100MまでOK)を読ませる
3. プロンプト「本書が語っている各章を端的に要約して下さい」で各章の気になる部分を調べる
4. プロンプトで知りたい部分の章とプロンプト「〜の章の要点とポイントを詳しく解説して下さい」
5. python index.py でアプリ起動 http://127.0.0.1:5000/ にアクセス
6. 読み上げボタンで完了！


## 🔧 必要な環境

- Python 3.8〜3.11（推奨）
- pip
- `open_jtalk`（音声合成エンジン）  
  → macOSの場合: `brew install open-jtalk`
- `sox`（音声結合ツール）  
  → macOSの場合: `brew install sox`

## 📁 必要ファイルの配置

以下のディレクトリに、必要な辞書ファイルと音声ファイルを設置してください：

```
/Volumes/ARSTH-2TB/dev/Voice/
├── nitech_jp_atr503_m001.htsvoice
└── open_jtalk_dic_utf_8-1.11/
```

> パスが異なる場合は、`index.py` 内の VOICE_DIR を適宜修正してください。

---

## 🚀 セットアップ手順

1. 依存ライブラリのインストール：

```
pip install -r requirements.txt
```

2. Flaskアプリの起動：

```
python index.py
```

3. ブラウザでアクセス：

```
http://localhost:5000
```

---

## 📝 使い方

1. テキストエリアに日本語テキストを貼り付け
2. 読み上げ速度をスライダーで選択
3. 「▶ 読み上げる」ボタンをクリック
4. ブラウザ内で音声が自動再生されます

---

## 📦 出力ファイル

一時的な `.txt` / `.wav` ファイルは `/tmp` に生成されます。  
必要に応じて自動削除処理を追加してください。

---

## 📄 ライセンス

- Open JTalk: [http://open-jtalk.sourceforge.net/](http://open-jtalk.sourceforge.net/)
- Nitech HTS Voice: Creative Commons Attribution 3.0

