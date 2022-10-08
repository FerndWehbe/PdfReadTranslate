from concurrent.futures import ProcessPoolExecutor
from itertools import chain
from typing import List
import argostranslate.package
import argostranslate.translate
import nltk

## Classes for Typing
Language = argostranslate.translate.Language
ITranslation = argostranslate.translate.ITranslation


class Translate:
    def __init__(self) -> None:
        nltk.download("punkt")

    def _download_languages(self, lang: str):
        available_packages = argostranslate.package.get_available_packages()
        available_packages = next(
            filter(
                lambda x: (x.from_code == lang and x.to_code)
                or (x.from_name == lang and x.to_name),
                available_packages,
            )
        )
        download_path = available_packages.download()
        argostranslate.package.install_from_path(download_path)

    def _check_installed_languages(self, lang: str) -> None | Language:
        installed_languages: List[
            Language
        ] = argostranslate.translate.get_installed_languages()
        if not installed_languages:
            return
        for inst_lang in installed_languages:
            if inst_lang.code == lang or inst_lang.name == lang:
                return inst_lang

    def _get_langague(self, lang: str) -> Language:
        lang_model = self._check_installed_languages(lang)
        if not lang_model:
            self._download_languages(lang)
            lang_model = self._check_installed_languages(lang)
        return lang_model

    def _start_translate(self, source_lang: str, target_lang: str) -> None:
        from_lang = self._get_langague(source_lang)
        to_lang = self._get_langague(target_lang)
        self.translation: ITranslation = from_lang.get_translation(to_lang)

    def _create_chuncks(self, list_data: list, num_chunks: int) -> list:
        len_data = len(list_data)
        len_chunk = len_data // num_chunks
        return [
            list_data[index : index + len_chunk]
            for index in range(0, len_data, len_chunk)
        ]

    def text_reader(self, path_file: str) -> str:
        with open(path_file, encoding="utf-8") as f:
            text = f.read()
        return text

    def tokenizer(self, text: str, language: str = "english") -> list:
        sentences = nltk.tokenize.sent_tokenize(text, language)
        self.num_sentenses = len(sentences)
        return sentences

    def translator(
        self,
        sentenses: list,
        verbose: bool = False,
        source_lang: str = "en",
        target_lang: str = "pt",
    ) -> list:
        translated = []
        self._start_translate(source_lang, target_lang)
        for index, sent in enumerate(sentenses):
            translated_text = self.translation.translate(sent)
            if verbose:
                print(f"Sentence translated: {index+1}")
                print(translated_text)
            translated.append(translated_text)
        self.text_translated = translated
        return translated

    def parallel(
        self,
        sentenses: list,
        num_process: int = 2,
        source_lang: str = "en",
        target_lang: str = "pt",
    ):
        chunks = self._create_chuncks(sentenses, num_process)
        with ProcessPoolExecutor() as exe:
            process = [
                exe.submit(
                    self.translator, chunck, False, source_lang, target_lang
                )
                for chunck in chunks
            ]
        return list(
            chain.from_iterable([result.result() for result in process])
        )

    def save_to_file(
        self, path_file: str = "translated.txt", file_data: list = None
    ) -> None:
        if file_data is not None:
            self.text_translated = file_data
        with open(path_file, "w", encoding="utf-8") as f:
            f.write("\n".join(self.text_translated))
