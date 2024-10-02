import argparse
import re
from glob import glob
from os import system

# Order is important:
BCP14 = ["MUST NOT", "SHALL NOT", "SHOULD NOT",
            "MUST", "REQUIRED", "SHALL", "SHOULD",
            "RECOMMENDED", "MAY", "OPTIONAL"
]
EXTENDED_BCP14 = [
    "NOT RECOMMENDED", "RECOMMENDS* NOT","RECOMMENDS*",
    "NOT PERMITTED", "PERMITTED", "PERMITS*",
    "NOT REQUIRED", "NOT REQUIRES*", "REQUIRES*",
    "CAN NOT", "COULD NOT", "CAN", "COULD", "MIGHT",
    "DEPRECATED", "HAVE TO"
]
KEYWORDS = {"BCP14": BCP14, "Extended BCP14": EXTENDED_BCP14}

# Colors according to asciidoctor default setup
#    no foreground = "black" = ""
#    no background = "white" = ""
COLOR_DICT = {
# code: fore., back.,  use  
    "BCP14": ("", "aqua", "BCP14"),
    "Extended BCP14": ("", "lime", "Extended BCP14"),
}

def adoc_colors(kw):
    fg = COLOR_DICT[kw][0]
    bg = COLOR_DICT[kw][1]
    if fg and bg:
        color = f"[{fg} {bg}-background]"
    elif fg:
        color = f"[{fg}]"
    elif bg:
        color = f"[{bg}-background]"
    return color

def color_help(color_code):
    fg = COLOR_DICT[color_code][0]
    bg = COLOR_DICT[color_code][1]
    if not fg:
        fg = "black"
    if not bg:
        bg = "none"
    help = COLOR_DICT[color_code][2]
    text = f'{color_code}={fg}/{bg} [{help}]'
    return text


def paint(text, selected):
    color = adoc_colors(selected)
    count = 0
    for k in KEYWORDS[selected]:
        kin = rf"(?<= )({k.lower()})(?=[ ,.:;])"
        if color:
            kout = rf"{color}#\1#"
        else:
            kout = kin
        text, c = re.subn(kin, kout, text)
        count += c
    return text, count


def process_file_list(file_list, selection):
    for file in file_list:
        file_out = f"{file[1:]}"
        with open(file, "r") as fin:
            text = fin.read()
        count = 0
        for selected in selection:
            # print(f'{kw:>14}:  {",   ".join(KEYWORDS[kw])}')
            # print()
            text, n = paint(text, selected)
            count += n
        with open(file_out, "w") as fut:
            fut.write(text)
        print(f"IN: {file:26}   OUT: {file_out:26} count: {count}")


def get_going():
    parser = argparse.ArgumentParser(
        prog="paint_text",
        description=("\nPaint words related to BCP-14 in .adoc files, "
                     "which must reside in the parent directory ('../'). "
                     "If no filename is given then all .adoc files will be processed.")
    )
    parser.add_argument("-f", "--file_name", default="*")
    parser.add_argument("-v", "--vocabulary",
                         default="BCP14",
                         help="Either 'BCP14' (default), 'EXT[ENDED]', or 'BOTH'"
                        )
    parser.add_argument("-c", "--color_code",
                         default=0,
                         help=(", ".join([color_help(c) for c in COLOR_DICT]) +
                               "  (Extended keywords have black letters)")
                        )
    args = parser.parse_args()
    file_pattern = args.file_name
    if file_pattern == "*":
        file_pattern += ".adoc"
    indir = "../"
    file_list = glob(indir + file_pattern)
    vocab = args.vocabulary
    print("\nKeywords:")
    if vocab.lower() == "both":
        selection = ["BCP14", "Extended BCP14"]
        print(f"BCP14:    {BCP14}")
        print(f"Extended: {EXTENDED_BCP14}")
    elif vocab.lower().startswith("ext"):
        selection = ["Extended BCP14"]
        print(f"Extended: {EXTENDED_BCP14}")
    else:
        selection = ["BCP14"]
        print(f"BCP14:    {BCP14}")
    process_file_list(file_list, selection)


if __name__ == "__main__":
    print()
    get_going()
    system('asciidoctor --verbose ${FINAL_TAG} -a docprodtime="$(date -u ${DATE_FMT})" cf-conventions.adoc -D conventions_build')
    system('./fix_style.sh')
