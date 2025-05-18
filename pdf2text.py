from pathlib import Path
import PyPDF2
import re
import os


def pdf_to_text(pdf_path: str | Path) -> str:
    pdf_path = Path(pdf_path)
    all_text = []

    with open(pdf_path, "rb") as f:
        pdf_reader = PyPDF2.PdfReader(f)

        
        for page_idx in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page_idx]
            content = page_obj.extract_text() or ""   
            all_text.append(content)

   
    text = "\n".join(all_text)
   
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text


def batch_convert(src_root: Path, dest_root: Path) -> None:
    """Walk stock dirs under *src_root* and save txt files under *dest_root*."""
    dest_root.mkdir(parents=True, exist_ok=True)

    for stock_dir in src_root.iterdir():
        if not stock_dir.is_dir():
            continue

        out_dir = dest_root / stock_dir.name
        out_dir.mkdir(exist_ok=True)

        for pdf_file in stock_dir.glob("*.pdf"):
            txt_path = out_dir / f"{pdf_file.stem}.txt"
            if txt_path.exists():
                print("跳过已存在:", txt_path)
                continue
            try:
                text = pdf_to_text(pdf_file)
                txt_path.write_text(text, encoding="utf-8")
                print(
                    f" {pdf_file.relative_to(src_root)} → {txt_path.name} "
                    f"({len(text):,} 字符)"
                )
            except Exception as e:
                print(f" 解析失败 {pdf_file.name}: {e}")

def parse_args():
    p = argparse.ArgumentParser(description="Convert PDFs in nested folders into txt.")
    p.add_argument("--src", required=True, type=Path, help="PDF 根目录")
    p.add_argument("--dst", required=True, type=Path, help="文本输出根目录")
    return p.parse_args()



if __name__ == "__main__":
    args = parse_args()
    batch_convert(args.src, args.dst)
