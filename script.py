from io import BytesIO
import xlrd
import xlwt
import re
from collections import Counter


class XlsReader:
    """Класс для вычисления количества повторящихся слов"""
    TRASH_WORDS = (
            'to', 'the', 'a', 'as', 'in', 'and', 'or', 'up', 'by', 'of', 'at',
            'on', 'is', 'was', 'has', 'have', 'had', 'no', 'not', 'for', 'be',
            'with', 'if'
        )

    def __init__(self, file, list_count=1, col_num=7, page_num=1):
        self.file = file
        self.page_num = page_num - 1
        self.col_num = col_num - 1

    def taking_out_the_trash(self, word):
        if word in self.TRASH_WORDS or word.isdigit():
            return True
        else:
            return False

    def read_file(self):
        workbook = xlrd.open_workbook(file_contents=self.file)
        
        worksheet = workbook.sheet_by_index(self.page_num)
        
        col_v = worksheet.col_values(self.col_num)
        text = ' '.join(col_v[1:])
        words = re.findall(r'\b\w+\b', text.lower())
        counter = Counter(words)

        new_workbook = xlwt.Workbook()
        new_worksheet = new_workbook.add_sheet('Sheet')
        new_worksheet.write(0, 0, 'Слово')
        new_worksheet.write(0, 1, 'Количество')

        index = 1
        for word, count in counter.most_common():
            if self.taking_out_the_trash(word=word):
                continue
            new_worksheet.write(index, 0, word)
            new_worksheet.write(index, 1, count)
            index += 1

        output = BytesIO()
        new_workbook.save(output)
        output.seek(0)
        
        return output
