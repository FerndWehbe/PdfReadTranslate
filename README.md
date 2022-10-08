# PdfReadTranslate

Tool to extract texts from pdf and translate the text.


### Module Extractor

Created to read and extract data of all pdfs.

Using PyPDF2 for read and extract.



### Module Translator

Created for read text, parse into sentences and translate that sentence and save the translated text.

Using nltk for parse text and tokenize into senteces.
Using argostranslate for translate a list of sentenses.

This module have 2 methods for translate.

*translator()*
* **mandatory** List of sentences
* **optional** Translate verbose (default *False*)
* **optional** Source Language (default *en*)
* **optional** Target Language (default *pt*)

This module translate, sequentially, all sentences.

*parallel()*
* **mandatory** List of sentences
* **mandatory** Number of parallel translates (default *2*)
* **optional** Source Language (default *en*)
* **optional** Target Language (default *pt*)

This module translate, in parallel, *N* sentences. For best performace, use the formula ```10 / number_of_cores ``` of your CPU.


### Usage

In main.py have a sample of how to use this tool.

#### Obs.

If you use the parallel translate, you need call this method after: ``` if __name__ == "__main__":``` for protect *multiprocessing* codes.