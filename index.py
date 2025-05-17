from flask import Flask, render_template_string, request, send_file
import subprocess
import os
import uuid
import textwrap
import shutil

app = Flask(__name__)

VOICE_DIR = "/Volumes/ARSTH-2TB/dev/Voice"
DICT_PATH = os.path.join(VOICE_DIR, "open_jtalk_dic_utf_8-1.11")
VOICE_PATH = os.path.join(VOICE_DIR, "nitech_jp_atr503_m001.htsvoice")
TMP_DIR = os.path.join(VOICE_DIR, "tmp")
os.makedirs(TMP_DIR, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang=\"ja\">
<head>
  <meta charset=\"UTF-8\">
  <title>Open JTalk Web 読み上げ</title>
  <style>
    body { background-color: #1e1e1e; color: #f0f0f0; font-family: sans-serif; padding: 2rem; }
    textarea { width: 100%; height: 200px; background: #2e2e2e; color: #f0f0f0; border: none; padding: 1rem; font-size: 16px; }
    input[type=range] { width: 300px; }
    .button { padding: 0.5rem 1rem; margin-top: 1rem; background: #444; color: white; border: none; font-size: 1rem; cursor: pointer; }
    audio { display: block; margin-top: 2rem; }
  </style>
</head>
<body>
  <h1>Open JTalk 読み上げ</h1>
  <form method=\"POST\">
    <label for=\"text\">テキスト:</label><br>
    <textarea name=\"text\">{{ text or '' }}</textarea><br>
    <label for=\"speed\">速度: {{ speed or 1.0 }}</label><br>
    <input type=\"range\" name=\"speed\" min=\"0.5\" max=\"2.0\" step=\"0.1\" value=\"{{ speed or 1.0 }}\"><br>
    <button class=\"button\" type=\"submit\">▶ 読み上げる</button>
  </form>
  {% if wav_file %}
    <audio controls autoplay>
      <source src=\"{{ url_for('audio', filename=wav_file) }}\" type=\"audio/wav\">
      お使いのブラウザはaudioタグをサポートしていません。
    </audio>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    wav_file = None
    text = ""
    speed = 1.0

    if request.method == "POST":
        text = request.form.get("text", "")
        speed = float(request.form.get("speed", 1.0))
        uid = str(uuid.uuid4())
        part_files = []

        chunks = textwrap.wrap(text, 500)
        for i, chunk in enumerate(chunks):
            tmp_txt = os.path.join(TMP_DIR, f"{uid}_{i}.txt")
            tmp_wav = os.path.join(TMP_DIR, f"{uid}_{i}.wav")
            with open(tmp_txt, "w", encoding="utf-8") as f:
                f.write(chunk)
            subprocess.call([
                "open_jtalk",
                "-x", DICT_PATH,
                "-m", VOICE_PATH,
                "-r", str(speed),
                "-ow", tmp_wav,
                tmp_txt
            ])
            part_files.append(tmp_wav)

        output_path = os.path.join(TMP_DIR, f"{uid}_combined.wav")
        subprocess.call(["sox"] + part_files + [output_path])
        wav_file = os.path.basename(output_path)

    return render_template_string(HTML_TEMPLATE, wav_file=wav_file, text=text, speed=speed)

@app.route("/audio/<filename>")
def audio(filename):
    path = os.path.join(TMP_DIR, filename)
    return send_file(path, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
