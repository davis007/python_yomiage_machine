
import sys
import re

def is_junk_line(line: str) -> bool:
    # 完全に無意味な記号/数字/パターン
    if re.search(r"[章書車読]を読み終えるまで[:：] ?\d+分?", line): return True
    if re.search(r"[0-9]{1,3}%+", line): return True
    if re.search(r"[0-9]{1,2}[⅔⅝⅞]", line): return True
    if re.search(r"読書の速さを測定中", line): return True
    if re.search(r"Copyright|translation rights|Tuttle|Agency|Inc|Sausalito|解説|訳者あとがき", line, re.IGNORECASE): return True
    if re.search(r"[฿¥$€]\s?\d+", line): return True
    if re.search(r"^第[0-9一二三四五六七八九十]+章$", line): return True
    if re.match(r"^(章|書|車|読)", line): return True

    # 無意味な短い断片（10～15文字程度の単語列）
    if len(line) < 15: return True

    # 「ない◯◯と経」のようなOCR特有の誤爆パターン
    if re.search(r"ない[ぁ-んァ-ン一-龯]{1,4}と経", line): return True

    # 助詞/句読点を全く含まない文（自然文ではない）
    if not re.search(r"[はがをにのへと、。]", line): return True

    return False

def clean_ocr_text(text: str) -> str:
    lines = text.splitlines()
    cleaned_lines = []
    seen_lines = set()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if is_junk_line(line):
            continue

        # 同じ文の繰り返し防止
        if line in seen_lines:
            continue
        seen_lines.add(line)

        # 記号・空白整形
        line = re.sub(r"[①-⑨Ⅰ-Ⅸⅰ-ⅹⅺ-ⅿⅰ-ⅽ⅓-⅞]", "", line)
        line = re.sub(r"\s+", " ", line)

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean.py input.txt output.txt")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned = clean_ocr_text(raw_text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"✅ Cleaned text written to {output_path}")
