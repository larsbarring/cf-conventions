import argparse
from glob import glob
from pathlib import Path
from os import system

 
KEYWORDS = ["MUST NOT", "SHALL NOT", "SHOULD NOT",
            "MUST", "REQUIRED", "SHALL", "SHOULD",
            "RECOMMENDED", "MAY", "OPTIONAL"
]
# undecided: aqua, 
# discuss: yellow, 
# done: lime,
# agreed: no background color (red text),
# ready to merge: black text (still no background color)

HIGHLIGHT_LIST = ["red aqua-background", "red yellow-background", "red lime-background", "red"]
HIGHLIGHT = HIGHLIGHT_LIST[3]


def paint(text):
    for k in KEYWORDS:
        klower = k.lower()
        kin = f" {klower} "
        kout = f" [{HIGHLIGHT}]#{klower}# "
        text = text.replace(kin, kout)
    return text


def process_file_list(file_list):
    for file in file_list:
        file_out = f"{file[1:]}"
        print(f"IN: {file},   OUT: {file_out}")
        with open(file, "r") as fin:
            text = paint(fin.read())
            with open(file_out, "w") as fut:
                fut.write(text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                        prog="paint_text",
                        description="Paint BCP-14 keywords in .adoc files.")
    parser.add_argument("filename", default="test_ch02.adoc")
    args = parser.parse_args()
    file_pattern = args.filename
    if file_pattern == "*":
        file_pattern += ".adoc"
    indir = "../"
    # print(indir + file_pattern)
    file_list = glob(indir + file_pattern)
    print(file_list)
    process_file_list(file_list)

    system('asciidoctor --verbose ${FINAL_TAG} -a docprodtime="$(date -u ${DATE_FMT})" cf-conventions.adoc -D conventions_build')

