from io import BufferedReader
import PyPDF2


class Converter:
    def _read_page(self, page_obj: PyPDF2.PageObject) -> str:
        text: str = page_obj.extract_text()
        return text

    def to_text(self, pdf_data: BufferedReader) -> str:
        if isinstance(pdf_data, BufferedReader):
            raise TypeError
        data = PyPDF2.PdfReader(pdf_data)
        self.num_pages = data.numPages
        return "\n".join(
            self._read_page(data.getPage(num_page))
            for num_page in range(self.num_pages)
        )
