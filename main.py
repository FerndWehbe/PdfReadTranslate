from concurrent.futures import ProcessPoolExecutor
from itertools import chain
import pathlib
from translator import Translate
from extractor import Converter
from natsort import natsorted
import glob

volumes = glob.glob("./pdfs/Mushoku Tensei WN/*")

conv = Converter()
trans = Translate()

if __name__ == "__main__":
    for novel_path in natsorted(volumes):
        novel = pathlib.Path(novel_path).name.removesuffix(".pdf")
        novel_text = conv.to_text(novel_path)
        tokens = trans.tokenizer(novel_text)
        with open(
            f"./pdfs/English Text/{novel}.txt", "w", encoding="utf-8"
        ) as f:
            f.write("".join(tokens))
        chunks = trans._create_chuncks(tokens, 3)
        with ProcessPoolExecutor() as exe:
            process = [
                exe.submit(trans.translator, chunck, False)
                for chunck in chunks
            ]
        translated = list(chain([result.result() for result in process]))
        trans.save_to_file(
            f"./pdfs/English Text/{novel}_translated.txt", translated
        )
        break
