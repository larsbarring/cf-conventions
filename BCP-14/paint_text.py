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
    "NOT RECOMMENDED", "RECOMMEND\S* NOT","RECOMMEND\S+",
    "CAN NOT", "COULD NOT", "CAN", "COULD", 
    "DEPRECATED", "HAVE TO"
]

# Colors according to asciidoctor default setup
#    no foreground = "black" = ""
#    no background = "white" = ""
COLOR_DICT = {
# code: fore., back.,  use  
    0: ("red", "aqua", "not worked on"),       # Before anyone starts working: set by this program
    1: ("red", "lime", "suggested change"),    # Manually change to this when there is a suggestion
    2: ("red", "yellow", "needs discussion"),  # Manually change to this if input/discussion is needed
    3: ("red", "", "agreed"),                  # Manually change to this when group is in agreement 
    4: ("", "", "ready to merge"),             # Manually change to this when the whole text piece is ready
}

def adoc_colors(color_code):
    fg = COLOR_DICT[color_code][0]
    bg = COLOR_DICT[color_code][1]
    if fg and bg:
        color = f"[{fg} {bg}-background]"
    elif fg:
        color = f"[{fg}]"
    else:
        color = ""
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


def paint(text, keywords, color_code):
    color = adoc_colors(color_code)
    count = 0
    for k in keywords:
        kin = rf"(?<= )({k.lower()})(?= )"
        if color:
            kout = rf"{color}#\1#"
        else:
            kout = kin
        text, c = re.subn(kin, kout, text)
        count += c
    return text, count


def process_file_list(file_list, keywords, color_code):
    for file in file_list:
        file_out = f"{file[1:]}"
        with open(file, "r") as fin:
            text, count = paint(fin.read(), keywords, color_code)
            with open(file_out, "w") as fut:
                fut.write(text)
        print(f"IN: {file:26}   OUT: {file_out:26} count = {count}")


def get_going():
    parser = argparse.ArgumentParser(
        prog="paint_text",
        description=("Paint words related to BCP-14 in .adoc files, "
                    "which must reside in the parent directory ('../')")
    )
    parser.add_argument("-f", "--file_name", default="*")
    parser.add_argument("-c", "--color_code",
                         default=0,
                         help=", ".join([color_help(c) for c in COLOR_DICT])
                        )
    parser.add_argument("-v", "--vocabulary",
                         default="BCP14",
                         help="Either 'BCP14' (default), 'EXT[ENDED]', or 'BOTH'"
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
        keywords = BCP14 + EXTENDED_BCP14
        print(f'         BCP-14:  {",   ".join(BCP14)}')
        print(f'Extended BCP-14:  {",   ".join(EXTENDED_BCP14)}')
    elif vocab.lower().startswith("ext"):
        keywords = EXTENDED_BCP14
        print(f'Extended BCP-14: {",   ".join(EXTENDED_BCP14)}')
    else:
        keywords = BCP14
        print(f'BCP-14: {",   ".join(BCP14)}')
    print()
    process_file_list(file_list, keywords, args.color_code)


if __name__ == "__main__":
    get_going()
    system('asciidoctor --verbose ${FINAL_TAG} -a docprodtime="$(date -u ${DATE_FMT})" cf-conventions.adoc -D conventions_build')
