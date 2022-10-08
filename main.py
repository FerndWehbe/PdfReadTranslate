from translator import Translate
from extractor import Converter
from natsort import natsorted
from datetime import datetime
import pathlib
import glob

volumes = glob.glob("./pdfs/*")

conv = Converter()
trans = Translate()


def timmer(_):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        _(*args, **kwargs)
        end = datetime.now()
        print(f"Tempo de execução: {end-start}")

    return wrapper


@timmer
def runner(novel_path):
    novel = pathlib.Path(novel_path).name.removesuffix(".pdf")
    novel_text = conv.to_text(novel_path)
    tokens = trans.tokenizer(novel_text)
    with open(f"./pdfs/English Text/{novel}.txt", "w", encoding="utf-8") as f:
        f.write("".join(tokens))
    translated = trans.parallel(tokens, 2)
    trans.save_to_file(
        f"./pdfs/English Text/{novel}_translated.txt", translated
    )


if __name__ == "__main__":
    for novel_path in natsorted(volumes):
        runner(novel_path)
