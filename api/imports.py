import csv
from io import BytesIO

import xlsxwriter as xlsxwriter
import xlwt as xlwt
from data_importer.importers import CSVImporter
from django.http import HttpResponse

from api.models import Student


class StudentCsvImportModel(CSVImporter):
    fields = ['name', 'class', 'stream', 'father', 'mother']

    class Meta:
        delimiter = ','
        ignore_first_line = True
        ignore_empty_lines = True


STUDENT_IMPORT_COLUMNS = ['NAME', 'ADMISSION_NUMBER', 'CLASS', 'STREAM', 'SEX',
                          'NATIONALITY', 'OTHER_INFO', 'NIN', 'FATHER_NAME', 'FATHER_TEL', 'FATHER_EMAIL',
                          'FATHER_OCCUPATION', 'FATHER_NIN', 'MOTHER_NAME', 'MOTHER_TEL', 'MOTHER_EMAIL',
                          'MOTHER_OCCUPATION', 'MOTHER_NIN']

SCHOOL_CLASS_COLUMNS = ['CLASS', 'CLASS_NUMBER', 'STREAM', 'LEVEL_SHORT', 'CURRICULUM', 'PROGRESSION']


def generate_academic_results_template(request):
    school = request.user.profile.school
    school_id = school.id
    school_name = school.name
    title = "Academic Results Upload Template"
    year = request.POST['year']
    term = request.POST['term']
    school_class = request.POST['school_class']
    subject = request.POST['subject']
    level = request.POST['level']
    upload_key = '1:2:3:4:5:6'  # request.GET['upload_key']

    ws1_name = 'Subject_Area_Results'
    ws2_name = 'Subject_Results'
    ws3_name = 'Overall_Results'

    ws1_columns = ['ID', 'Pupil', 'Subject Area 1', 'Subject Area 2', 'Subject Area 3',
                   'Subject Area 4',
                   'Subject Area 5', 'Subject Area 6', 'Subject Area 7', 'Subject Area 8',
                   'Subject Area 9',
                   'Subject Area 10']

    ws2_columns = ['ID', 'Pupil', 'Mark', 'Grade', 'Stream Position', 'Class Position', 'Comment']
    ws3_columns = ['ID', 'Pupil', 'Total Marks', 'Average Mark', 'Aggregate in 4', 'Division',
                   'Stream Position', 'Class Position', 'Class Teacher Comment', 'House Teacher Comment',
                   'Head Teacher Comment']

    if level == 'O':
        ws1_name = 'Paper_Results'

        ws1_columns = ['ID', 'Student', 'Mark', 'Grade', 'Stream Position', 'Class Position', 'Comment']
        ws2_columns = ['ID', 'Student', 'Mark', 'Grade', 'Stream Position', 'Class Position', 'Comment']
        ws3_columns = ['ID', 'Student', 'Total Marks', 'Average Mark', 'Aggregate in 8', 'Division', 'Stream Position',
                       'Class Position', 'Class Teacher Comment', 'House Teacher Comment', 'Head Teacher Comment']

    elif level == 'A':
        ws1_name = 'Paper_Results'

        ws1_columns = ['ID', 'Student', 'Mark', 'Grade', 'Stream Position', 'Class Position', 'Comment']
        ws2_columns = ['ID', 'Student', 'Grade', 'Points', 'Stream Position', 'Class Position', 'Comment']
        ws3_columns = ['ID', 'Student', 'Result', 'Points', 'Class Teacher Comment', 'House Teacher Comment',
                       'Head Teacher Comment']

    # students = Student.objects.filter(school_id=school_id, school_class=school_class, stream=stream)
    students = Student.objects.filter(school_id=school_id, )

    # create a workbook in memory
    output = BytesIO()

    wb = xlsxwriter.Workbook(output)

    # ===================================================================
    # Worksheet 1
    # ===================================================================

    ws1 = wb.add_worksheet(ws1_name)

    # Sheet header, first row
    row_num = 0

    # Row1 = School Name
    ws1.write(row_num, 0, school_name)
    row_num += 1

    # Row2 = Document Title
    ws1.write(row_num, 0, title)
    row_num += 1

    # Row3 = Year/Term
    ws1.write(row_num, 0, "Year/Term")
    ws1.write(row_num, 1, "%s / %s" % (year, term))
    row_num += 1

    # Row4 = Class/ Stream
    ws1.write(row_num, 0, "Class")
    ws1.write(row_num, 1, "%s" % school_class)
    row_num += 1

    # Row5 = Subject
    ws1.write(row_num, 0, "Subject")
    ws1.write(row_num, 1, subject)
    row_num += 2

    for col_num in range(len(ws1_columns)):
        ws1.write(row_num, col_num, ws1_columns[col_num])

    row_num += 1
    for student in students:
        ws1.write(row_num, 0, student.id)
        ws1.write(row_num, 1, "%s %s" % (student.first_name, student.last_name))
        row_num += 1

    # ===================================================================
    # Worksheet 2
    # ===================================================================

    ws2 = wb.add_worksheet(ws2_name)

    row_num = 0

    # Row1 = School Name
    ws2.write(row_num, 0, school_name)
    row_num += 1

    # Row2 = Document Title
    ws2.write(row_num, 0, title)
    row_num += 1

    # Row3 = Year/Term
    ws2.write(row_num, 0, "Year/Term")
    ws2.write(row_num, 1, "%s %s" % (year, term))
    row_num += 1

    # Row4 = Class/ Stream
    ws2.write(row_num, 0, "Class")
    ws2.write(row_num, 1, "%s" % school_class)
    row_num += 1

    # Row5 = Subject
    ws2.write(row_num, 0, "Subject")
    ws2.write(row_num, 1, subject)
    row_num += 2

    for col_num in range(len(ws2_columns)):
        ws2.write(row_num, col_num, ws2_columns[col_num])

    row_num += 1
    for student in students:
        ws2.write(row_num, 0, student.id)
        ws2.write(row_num, 1, "%s %s" % (student.first_name, student.last_name))
        row_num += 1

    # ===================================================================
    # Worksheet 3
    # ===================================================================

    ws3 = wb.add_worksheet(ws3_name)

    row_num = 0

    # Row1 = School Name
    ws3.write(row_num, 0, school_name)
    row_num += 1

    # Row2 = Document Title
    ws3.write(row_num, 0, title)
    row_num += 1

    # Row3 = Year/Term
    ws3.write(row_num, 0, "Year/Term")
    ws3.write(row_num, 1, "%s %s" % (year, term))
    row_num += 1

    # Row4 = Class/ Stream
    ws3.write(row_num, 0, "Class")
    ws3.write(row_num, 1, "%s" % school_class)
    row_num += 1

    # Row5 = Subject
    ws3.write(row_num, 0, "Subject")
    ws3.write(row_num, 1, subject)
    row_num += 2

    for col_num in range(len(ws3_columns)):
        ws3.write(row_num, col_num, ws3_columns[col_num])

    row_num += 1
    for student in students:
        ws3.write(row_num, 0, student.id)
        ws3.write(row_num, 1, "%s %s" % (student.first_name, student.last_name))
        row_num += 1

    wb.close()

    output.seek(0)

    filename = "%s_T%s_%s_%s_results_template.xlsx" % (year, term, school_class, subject)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    return response


def generate_class_list_template(request, f='CSV'):
    if f == 'CSV':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="school_classes_import.csv"'

        writer = csv.writer(response)

        # header

        writer.writerow(SCHOOL_CLASS_COLUMNS)

        return response

    if f == 'EXCEL':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="school_classes_import.xlsx"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('StudentData')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = SCHOOL_CLASS_COLUMNS

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        wb.save(response)
        return response


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
