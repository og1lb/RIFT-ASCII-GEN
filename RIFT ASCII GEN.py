import os
import sys

try:
    import pyfiglet
except ImportError:
    print("pip install pyfiglet")
    sys.exit(1)

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


BANNER = r"""
  ___ ___ ___ _____     _   ___  ___ ___ ___    ___ ___ _  _ 
 | _ \_ _| __|_   _|   /_\ / __|/ __|_ _|_ _|  / __| __| \| |
 |   /| || _|  | |    / _ \\__ \ (__ | | | |  | (_ | _|| .` |
 |_|_\___|_|   |_|   /_/ \_\___/\___|___|___|  \___|___|_|\_|
                                                             
"""


REQUESTED_FONTS = [
    "1Row", "3-D", "3D Diagonal", "3D-ASCII", "3x5", "4Max",
    "5 Line Oblique", "Acrobatic", "Alligator", "Alligator2",
    "Alphabet", "Avatar", "Banner", "Banner3-D", "Banner3",
    "Banner4", "Barbwire", "Basic", "Bell", "Big", "Big Chief",
    "Binary", "Block", "Bubble", "Bulbhead", "Caligraphy",
    "Chunky", "Colossal", "Computer", "Cursive", "Cyberlarge",
    "Cybermedium", "Cybersmall", "Digital", "Doom",
    "Dot Matrix", "Double", "Epic", "Ghost", "Graffiti",
    "Hex", "Hollywood", "Isometric1", "Isometric2",
    "Isometric3", "Isometric4", "Italic", "Katakana",
    "Larry3D", "Lean", "Letters", "Linux", "Mini", "Mirror",
    "Nancyj", "Ogre", "Pawp", "Pebbles", "Poison",
    "Puffy", "Rectangles", "Relief", "Relief2", "Roman",
    "Rounded", "Script", "Shadow", "Short", "Slant",
    "Small", "Soft", "Speed", "Standard", "Star Wars",
    "Straight", "Sub-Zero", "Sweet", "Thin", "Ticks",
    "Tombstone", "Trek", "Twisted", "Univers", "Varsity",
    "Whimsy"
]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def normalize(name):
    return "".join(
        x for x in name.lower()
        if x.isalnum()
    )


def build_font_map():
    installed = pyfiglet.FigletFont.getFonts()

    fonts = {
        normalize(x): x
        for x in installed
    }

    result = {}

    for name in REQUESTED_FONTS:
        key = normalize(name)

        if key in fonts:
            result[name] = fonts[key]
            continue

        found = None

        for k, v in fonts.items():
            if k.startswith(key) or key.startswith(k):
                found = v
                break

        result[name] = found

    return result


def show_fonts(font_map):
    available = []

    print("\nFonts:\n")

    for name, slug in font_map.items():
        if slug:
            available.append(name)
            print(
                f"{len(available):3}. {name}"
            )

    return available


def choose_font(font_map):
    fonts = show_fonts(font_map)

    while True:
        choice = input(
            "\nChoose font: "
        ).strip()

        if choice.lower() == "q":
            return None

        if choice.isdigit():
            index = int(choice) - 1

            if 0 <= index < len(fonts):
                return font_map[fonts[index]]

        for name, slug in font_map.items():
            if normalize(choice) == normalize(name):
                return slug

        print("Invalid choice")


def generate(text, font):
    return pyfiglet.figlet_format(
        text,
        font=font
    )


def copy(text):
    if CLIPBOARD_AVAILABLE:
        try:
            pyperclip.copy(text)
            print("\nCopied to clipboard.")
        except:
            pass


def main():
    clear_screen()
    print(BANNER)

    font_map = build_font_map()

    text = input(
        "Enter text: "
    ).strip()

    if not text:
        text = "ASCII"


    while True:

        font = choose_font(font_map)

        if font is None:
            break

        result = generate(
            text,
            font
        )

        clear_screen()
        print(BANNER)
        print(result)

        copy(result)

        print(
            "\n1. Choose another font"
            "\n2. New text"
            "\n3. Exit"
        )

        choice = input(
            "> "
        )

        if choice == "2":
            text = input(
                "Enter text: "
            ).strip()

        elif choice == "3":
            break


if __name__ == "__main__":
    main()
