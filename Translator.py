# Making Translator using Python

# Befor run the program run the following in the terminal:

# C:\Users\maril\AppData\Local\Programs\Python\Python314\python.exe -m pip install deep-translator langdetect
# C:\Users\maril\AppData\Local\Programs\Python\Python314\python.exe -c "from deep_translator import GoogleTranslator; from langdetect import detect; print('All libraries installed successfully!')"

from deep_translator import GoogleTranslator
from langdetect import detect

print("===== 👋 Welcome to the Translator! 🌍✨ =====")
print("Type exit anytime if you want to quit. 😊\n")

while True:
    print("Codes: fr(French), en(English), ur(Urdu), hi(Hindi), ar(Arabic), zh(Chinese), de(German), es(Spanish), el(Greek), tr(Turkish), ru(Russian), ja(Japanese), pt(Portuguese), it(Italian), ko(Korean)")
    print("🔍 For auto detection, type auto. 😊")

    src = input("From (or auto): ").strip().lower()

    if src == "exit":
        break

    if src in ("", "auto"):
        src = "auto"

    dest = input("To: ").strip().lower()

    if dest == "exit":
        break

    text = input("Text: ").strip()

    if text.lower() == "exit":
        break

    if not text:
        print("⚠️ Oops! Text is empty. Please enter some text to translate.\n")
        continue

    try:
        result = GoogleTranslator(
            source=src,
            target=dest
        ).translate(text)

        print("\n😉 Here's your Result:", result, "\n")
    except Exception:
        print(
            "⚠️ Error! Check language codes or internet Or try again.\n"
        )

    if input("🔄 Would you like to try again? (y/n): ").strip().lower() != "y":
        break

print("👋 Translator closed. Thanks for using it! 😃")
