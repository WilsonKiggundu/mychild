import csv

import xlwt as xlwt
from data_importer.importers import CSVImporter
from django.http import HttpResponse


class StudentCsvImportModel(CSVImporter):
    fields = ['name', 'class', 'stream', 'father', 'mother']

    class Meta:
        delimiter = ','
        ignore_first_line = True
        ignore_empty_lines = True


STUDENT_IMPORT_COLUMNS = ['ADMISSION_NUMBER', 'NAME', 'DATE_OF_BIRTH', 'SEX', 'CLASS', 'STREAM', 'DORMITORY',
                          'RELIGION', 'DISTRICT', 'NATIONALITY', 'HOME_ADDRESS', 'EMAIL', 'DATE_JOINED', 'CLASS_JOINED',
                          'DISABLED', 'OTHER_INFO', 'NIN', 'FATHER_NAME', 'FATHER_TEL', 'FATHER_EMAIL', 'FATHER_OCCUPATION',
                          'FATHER_NIN', 'MOTHER_NAME', 'MOTHER_TEL', 'MOTHER_EMAIL', 'MOTHER_OCCUPATION', 'MOTHER_NIN']


def generate_students_list_template(request, f='CSV'):

    if f == 'CSV':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="student_import.csv"'

        writer = csv.writer(response)
        writer.writerow(STUDENT_IMPORT_COLUMNS)

        return response

    if f == 'EXCEL':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="student_import.xlsx"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('StudentData')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = STUDENT_IMPORT_COLUMNS

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        wb.save(response)
        return response


def process_csv_file(request, ignore_first_line=True):
    csv_file = request.FILES['file']

    file_data = csv_file.read().decode('utf-8')
    data_lines = file_data.split('\n')

    lines = []

    for index, line in enumerate(data_lines):
        if index == 0 and ignore_first_line:
            continue

        if line:
            lines.append(line)

    return lines
