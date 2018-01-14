import codecs
import csv
from io import BytesIO

import xlrd
import xlsxwriter as xlsxwriter
import xlwt as xlwt
from data_importer.importers import CSVImporter
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse

from api.models import *
from api.options import Imports
from api.utils import generate_student_code


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
SUBJECTS_COLUMNS = ['NAME', 'SHORT_NAME', 'CODE', 'CURRICULUM', 'GROUP', 'SUBJECT AREA', 'STANDARD', 'LEVEL']
SUBJECT_GROUP_COLUMNS = ['GROUP', 'NAME', 'LEVEL']


def generate_academic_results_template(request):
    school = request.user.profile.school
    school_id = school.id
    school_name = school.name
    title = "Academic Results Upload Template"
    year = request.POST['year']
    term = request.POST['term']
    class_id = request.POST['school_class']
    subject = request.POST['subject']

    school_class = SchoolClass.objects.filter(pk=class_id).first()

    level = school_class.level
    level_short = school_class.level_short
    class_name = school_class.name
    stream = school_class.stream

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

    if level_short == 'O':
        ws1_name = 'Paper_Results'

        ws1_columns = ['ID', 'Student', 'Mark', 'Grade', 'Stream Position', 'Class Position', 'Comment']
        ws2_columns = ['ID', 'Student', 'Mark', 'Grade', 'Stream Position', 'Class Position', 'Comment']
        ws3_columns = ['ID', 'Student', 'Total Marks', 'Average Mark', 'Aggregate in 8', 'Division', 'Stream Position',
                       'Class Position', 'Class Teacher Comment', 'House Teacher Comment', 'Head Teacher Comment']

    elif level_short == 'A':
        ws1_name = 'Paper_Results'

        ws1_columns = ['ID', 'Student', 'Mark', 'Grade', 'Stream Position', 'Class Position', 'Comment']
        ws2_columns = ['ID', 'Student', 'Grade', 'Points', 'Stream Position', 'Class Position', 'Comment']
        ws3_columns = ['ID', 'Student', 'Result', 'Points', 'Class Teacher Comment', 'House Teacher Comment',
                       'Head Teacher Comment']

    # students = Student.objects.filter(school_id=school_id, school_class=school_class, stream=stream)
    students = Student.objects.filter(school_id=school_id, school_class=class_name, )

    # create a workbook in memory
    output = BytesIO()

    wb = xlsxwriter.Workbook(output)

    # ===================================================================
    # Worksheet 1
    # ===================================================================

    ws1 = wb.add_worksheet(ws1_name)

    h1_format = wb.add_format({'bold': True, 'font_size': 18, 'locked': 1})
    h2_format = wb.add_format({'bold': True, 'font_size': 15, 'locked': 1})
    bold_text = wb.add_format({'bold': True, 'font_size': 11})
    locked = wb.add_format({'locked': 1})

    # Sheet header, first row
    row_num = 0

    # Row1 = School Name
    ws1.merge_range('A1:G1', school_name, h1_format)
    row_num += 1

    # Row2 = Document Title
    ws1.merge_range('A2:G2', title, h2_format)
    row_num += 1

    # Row3 = Year/Term
    ws1.write(row_num, 0, "Year/Term", bold_text)
    ws1.write(row_num, 1, "%s" % year)
    ws1.write(row_num, 2, "Term %s" % term)
    row_num += 1

    # Row4 = Class/ Stream
    ws1.write(row_num, 0, "Class", bold_text)
    ws1.write(row_num, 1, "%s" % class_name)
    ws1.write(row_num, 2, "%s" % stream)
    ws1.write(row_num, 3, "%s" % level)
    row_num += 1

    # Row5 = Subject
    ws1.write(row_num, 0, "Subject", bold_text)
    ws1.write(row_num, 1, subject)
    row_num += 2

    for col_num in range(len(ws1_columns)):
        ws1.write(row_num, col_num, ws1_columns[col_num], bold_text)

    row_num += 1
    for student in students:
        ws1.write(row_num, 0, student.id, locked)
        ws1.write(row_num, 1, "%s %s" % (student.first_name, student.last_name))
        row_num += 1

    # ===================================================================
    # Worksheet 2
    # ===================================================================

    ws2 = wb.add_worksheet(ws2_name)

    row_num = 0

    # Row1 = School Name
    ws2.merge_range('A1:G1', school_name, h1_format)
    row_num += 1

    # Row2 = Document Title
    ws2.merge_range('A2:G2', title, h2_format)
    row_num += 1

    # Row3 = Year/Term
    ws2.write(row_num, 0, "Year/Term", bold_text)
    ws2.write(row_num, 1, "%s" % year)
    ws2.write(row_num, 1, "Term %s" % term)
    row_num += 1

    # Row4 = Class/ Stream
    ws2.write(row_num, 0, "Class", bold_text)
    ws2.write(row_num, 1, "%s" % school_class)
    ws2.write(row_num, 2, "%s" % stream)
    ws2.write(row_num, 3, "%s" % level)
    row_num += 1

    # Row5 = Subject
    ws2.write(row_num, 0, "Subject", bold_text)
    ws2.write(row_num, 1, subject)
    row_num += 2

    for col_num in range(len(ws2_columns)):
        ws2.write(row_num, col_num, ws2_columns[col_num], bold_text)

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
    ws3.merge_range('A1:K1', school_name, h1_format)
    row_num += 1

    # Row2 = Document Title
    ws3.merge_range('A2:K2', title, h2_format)
    row_num += 1

    # Row3 = Year/Term
    ws3.write(row_num, 0, "Year/Term", bold_text)
    ws3.write(row_num, 1, "%s" % year)
    ws3.write(row_num, 2, "Term %s" % term)
    row_num += 1

    # Row4 = Class/ Stream
    ws3.write(row_num, 0, "Class", bold_text)
    ws3.write(row_num, 1, "%s" % school_class)
    ws3.write(row_num, 2, "%s" % stream)
    ws3.write(row_num, 3, "%s" % level)
    row_num += 1

    # Row5 = Subject
    ws3.write(row_num, 0, "Subject", bold_text)
    ws3.write(row_num, 1, subject)
    row_num += 2

    for col_num in range(len(ws3_columns)):
        ws3.write(row_num, col_num, ws3_columns[col_num], bold_text)

    row_num += 1
    for student in students:
        ws3.write(row_num, 0, student.id)
        ws3.write(row_num, 1, "%s %s" % (student.first_name, student.last_name))
        row_num += 1

    wb.close()

    output.seek(0)

    filename = "%s_Term%s_%s_%s_results.xlsx" % (year, term, school_class, subject)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    return response


def generate_class_list_template(request):
    school = request.user.profile.school
    school_name = school.name
    title = "School Classes"

    # create a workbook in memory
    output = BytesIO()

    wb = xlsxwriter.Workbook(output)
    ws = wb.add_worksheet('School_Classes')

    h1_format = wb.add_format({'bold': True, 'font_size': 18, 'locked': True})
    h2_format = wb.add_format({'bold': True, 'font_size': 15, 'locked': True})
    bold_text = wb.add_format({'bold': True, 'font_size': 11})

    ws.write(0, 0, school_name, h1_format)
    ws.write(1, 0, title, h2_format)

    for col_num in range(len(SCHOOL_CLASS_COLUMNS)):
        ws.write(3, col_num, SCHOOL_CLASS_COLUMNS[col_num], bold_text)

    wb.close()

    output.seek(0)

    filename = "%s_classes_template.xlsx" % school_name
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    return response


def generate_students_list_template(request):
    school = request.user.profile.school
    school_name = school.name
    title = "Students List"

    # create a workbook in memory
    output = BytesIO()

    wb = xlsxwriter.Workbook(output)
    ws = wb.add_worksheet('Students_List')

    h1_format = wb.add_format({'bold': True, 'font_size': 18, 'locked': True})
    h2_format = wb.add_format({'bold': True, 'font_size': 15, 'locked': True})
    bold_text = wb.add_format({'bold': True, 'font_size': 11})

    ws.write(0, 0, school_name, h1_format)
    ws.write(1, 0, title, h2_format)

    for col_num in range(len(STUDENT_IMPORT_COLUMNS)):
        ws.write(3, col_num, STUDENT_IMPORT_COLUMNS[col_num], bold_text)

    wb.close()

    output.seek(0)

    filename = "%s_students_list_template.xlsx" % school_name
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    return response


def generate_subjects_list_template(request):
    school = request.user.profile.school
    school_name = school.name
    title = "Subjects List"

    # create a workbook in memory
    output = BytesIO()

    wb = xlsxwriter.Workbook(output)
    h1_format = wb.add_format({'bold': True, 'font_size': 18, 'locked': True})
    h2_format = wb.add_format({'bold': True, 'font_size': 15, 'locked': True})
    bold_text = wb.add_format({'bold': True, 'font_size': 11})

    ws = wb.add_worksheet('Subjects')

    ws.write(0, 0, school_name, h1_format)
    ws.write(1, 0, title, h2_format)

    for col_num in range(len(SUBJECTS_COLUMNS)):
        ws.write(3, col_num, SUBJECTS_COLUMNS[col_num], bold_text)

    ws = wb.add_worksheet('Groups')

    ws.write(0, 0, school_name, h1_format)
    ws.write(1, 0, title, h2_format)

    for col_num in range(len(SUBJECT_GROUP_COLUMNS)):
        ws.write(3, col_num, SUBJECT_GROUP_COLUMNS[col_num], bold_text)

    wb.close()

    output.seek(0)

    filename = "%s_subjects_list_template.xlsx" % school_name
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    return response


def process_excel_file(request, category):
    file = request.FILES['file']
    school_id = request.user.profile.school_id

    book = xlrd.open_workbook(file_contents=file.read())
    sheets = book.sheet_names()

    for sheet in sheets:
        ws = book.sheet_by_name(sheet)
        rows = ws.get_rows()

        # results
        if category == Imports.results:

            try:
                year = ws.cell(2, 1).value
                term_label = ws.cell(2, 2).value  # Term 1

                term = term_label.split(' ')[1]

                school_class = ws.cell(3, 1).value
                stream = ws.cell(3, 2).value
                level = ws.cell(3, 3).value

                if level == 'Primary':
                    level = 'P'
                elif level == 'O level':
                    level = 'O'
                elif level == 'A level':
                    level = 'A'

                subject_name = ws.cell(4, 1).value
                subject = Subject.objects.filter(name=subject_name, school_id=school_id).first()
                subject_id = subject.id

                for (i, row) in enumerate(rows):
                    if i <= 7:
                        continue

                    student_id = ws.cell(i, 0).value
                    if student_id is None:
                        continue

                    if sheet == 'Subject_Area_Results':
                        subject_area_1 = ws.cell(i, 2).value
                        subject_area_2 = ws.cell(i, 3).value
                        subject_area_3 = ws.cell(i, 4).value
                        subject_area_4 = ws.cell(i, 5).value
                        subject_area_5 = ws.cell(i, 6).value
                        subject_area_6 = ws.cell(i, 7).value
                        subject_area_7 = ws.cell(i, 8).value
                        subject_area_8 = ws.cell(i, 9).value
                        subject_area_9 = ws.cell(i, 10).value
                        subject_area_10 = ws.cell(i, 11).value

                        AcademicsResultsLocalPrimarySubject(
                            student_id=student_id, school_id=school_id, school_class=school_class, stream=stream,
                            term=term, year=year,
                            # TODO: complete this
                        ).save()

                    if sheet == 'Subject_Results':
                        if level == 'P' or level == 'O':
                            mark = ws.cell(i, 2).value

                            # save nothing if there is no mark to save
                            if mark is None:
                                continue

                            grade = ws.cell(i, 3).value
                            stream_position = ws.cell(i, 4).value
                            class_position = ws.cell(i, 5).value
                            comment = ws.cell(i, 6).value

                            try:
                                if level == 'O':
                                    AcademicsResultsLocalOLevelSubject(
                                        school_id=school_id, student_id=student_id,
                                        mark=mark, grade=grade, year=year, term=term,
                                        class_position=class_position,
                                        stream_position=stream_position,
                                        school_class=school_class,
                                        stream=stream, subject=subject,
                                        comment=comment
                                    ).save()

                                if level == 'P':
                                    AcademicsResultsLocalPrimarySubject(
                                        school_id=school_id, student_id=student_id,
                                        result=mark, grade=grade, year=year, term=term,
                                        class_position=class_position,
                                        stream_position=stream_position,
                                        school_class=school_class,
                                        stream=stream, subject=subject,
                                        comment=comment
                                    ).save()

                            except():
                                pass

                        if level == 'A':
                            grade = ws.cell(i, 2).value
                            points = ws.cell(i, 3).value
                            stream_position = ws.cell(i, 4).value
                            class_position = ws.cell(i, 5).value
                            comment = ws.cell(i, 6).value

                    if sheet == 'Overall_Results':
                        if level == 'P' or level == 'O':
                            total_mark = ws.cell(i, 2).value

                            # save nothing if there is no mark to save
                            if total_mark is None:
                                continue

                            average_mark = ws.cell(i, 3).value
                            aggregate = ws.cell(i, 4).value
                            division = ws.cell(i, 5).value
                            stream_position = ws.cell(i, 6).value
                            class_position = ws.cell(i, 7).value
                            class_teacher_comment = ws.cell(i, 8).value
                            house_teacher_comment = ws.cell(i, 9).value
                            head_teacher_comment = ws.cell(i, 10).value

                            if level == 'P':
                                AcademicsResultsLocalPrimaryOverall(
                                    total_marks=total_mark, average_mark=average_mark, aggregate=aggregate,
                                    division=division, class_position=class_position, stream_position=stream_position,
                                    class_teacher_comment=class_teacher_comment,
                                    house_teacher_comment=house_teacher_comment,
                                    head_teacher_comment=head_teacher_comment,
                                    school_class=school_class, stream=stream, term=term, year=year,
                                    student_id=student_id, school_id=school_id, subject_id=subject_id
                                ).save()

                            elif level == 'O':
                                AcademicsResultsLocalOLevelOverall(
                                    total_marks=total_mark, average_mark=average_mark, aggregate=aggregate,
                                    division=division, class_position=class_position, stream_position=stream_position,
                                    class_teacher_comment=class_teacher_comment,
                                    house_teacher_comment=house_teacher_comment,
                                    head_teacher_comment=head_teacher_comment,
                                    school_class=school_class, stream=stream, term=term, year=year,
                                    student_id=student_id, school_id=school_id, subject_id=subject_id
                                ).save()

                        if level == 'A':
                            result = ws.cell(i, 2).value

                            # save nothing if there is no mark to save
                            if result is None:
                                continue

                            points = ws.cell(i, 3).value
                            class_teacher_comment = ws.cell(i, 4).value
                            house_teacher_comment = ws.cell(i, 5).value
                            head_teacher_comment = ws.cell(i, 6).value

                            AcademicsResultsLocalALevelOverall(
                                points=points,
                                class_teacher_comment=class_teacher_comment,
                                house_teacher_comment=house_teacher_comment,
                                head_teacher_comment=head_teacher_comment,
                                school_id=school_id,
                                student_id=student_id,
                                school_class=school_class,
                                stream=stream,
                                term=term, year=year
                            ).save()

                    if sheet == 'Paper_Results':
                        if level == 'P':
                            continue

                        if level == 'O' or level == 'A':
                            mark = ws.cell(i, 2).value

                            # save nothing if there is no mark to save
                            if mark is None:
                                continue

                            grade = ws.cell(i, 3).value
                            stream_position = ws.cell(i, 4).value
                            class_position = ws.cell(i, 5).value
                            comment = ws.cell(i, 6).value

                            AcademicsResultsMarks(
                                grade=grade, stream_position=stream_position, class_position=class_position,
                                comment=comment, student_id=student_id, school_id=school_id, type=1,
                                subject_id=subject_id, school_class=school_class, stream=stream, year=year, term=term,
                            ).save()
            except():
                pass

        # students
        elif category == Imports.students:

            for (i, row) in enumerate(rows):
                # skip the header row
                if i >= 4:
                    name = ws.cell(i, 0).value.split(' ')

                    first_name = name[0]
                    last_name = name[1]

                    admission_number = ws.cell(i, 1).value

                    code = generate_student_code(admission_number=admission_number)

                    school_class = ws.cell(i, 2).value
                    stream = ws.cell(i, 3).value
                    gender = ws.cell(i, 4).value
                    nationality = ws.cell(i, 5).value
                    other_info = ws.cell(i, 6).value
                    student_nin = ws.cell(i, 7).value

                    father_name = ws.cell(i, 8).value
                    father_telephone = ws.cell(i, 9).value
                    father_email = ws.cell(i, 10).value
                    father_occupation = ws.cell(i, 11).value
                    father_nin = ws.cell(i, 12).value

                    mother_name = ws.cell(i, 13).value
                    mother_telephone = ws.cell(i, 14).value
                    mother_email = ws.cell(i, 15).value
                    mother_occupation = ws.cell(i, 16).value
                    mother_nin = ws.cell(i, 17).value

                    try:
                        student = Student(first_name=first_name, last_name=last_name, nationality=nationality,
                                          gender=gender, school_class=school_class, stream=stream,
                                          other_info=other_info,
                                          nin=student_nin, admission_number=admission_number, school_id=school_id,
                                          code=code)
                        student.save()

                        ''' add parents '''
                        if father_name:
                            name = father_name.split(' ')
                            user = User(email=father_email, username=father_email, is_active=True, first_name=name[0],
                                        last_name=name[1], )

                            user.set_password('sw33th0m3')
                            user.save()

                            profile = Profile(user=user, telephone=father_telephone, type='Parent', )
                            profile.save()

                            father = Nok(name=father_name, student=student, occupation=father_occupation,
                                         relationship='Father',
                                         nin=father_nin, profile=profile)

                            father.save()

                        if mother_name:
                            name = mother_name.split(' ')
                            user = User(email=mother_email, username=mother_email, is_active=True, first_name=name[0],
                                        last_name=name[1], )

                            user.set_password('sw33th0m3')
                            user.save()

                            profile = Profile(user=user, telephone=mother_telephone, type='Parent', )
                            profile.save()

                            mother = Nok(name=mother_name, student=student, occupation=mother_occupation,
                                         relationship='Mother',
                                         nin=mother_nin, profile=profile)

                            mother.save()

                    except IntegrityError:
                        pass

        # subjects
        elif category == Imports.subjects:
            if sheet == 'Subjects':
                for (i, row) in enumerate(rows):
                    if i <= 3:
                        continue

                    name = ws.cell(i, 0).value
                    short_name = ws.cell(i, 1).value
                    code = ws.cell(i, 2).value
                    curriculum = ws.cell(i, 3).value
                    group = ws.cell(i, 4).value
                    subject_area = ws.cell(i, 5).value
                    standard = ws.cell(i, 6).value
                    level = ws.cell(i, 7).value

                    exists = Subject.objects.filter(
                        name__exact=name,
                        code__exact=code,
                        level__exact=level,
                        school_id__exact=school_id
                    ).count() > 0

                    if not exists:
                        Subject(
                            name=name,
                            short=short_name,
                            code=code,
                            curriculum=curriculum,
                            group=group,
                            area=subject_area,
                            standard=standard,
                            level=level,
                            school_id=school_id
                        ).save()
            else:
                for (i, row) in enumerate(rows):
                    if i <= 3:
                        continue

                    name = ws.cell(i, 0).value
                    group = ws.cell(i, 1).value
                    level = ws.cell(i, 2).value

                    exists = SubjectGroup.objects.filter(
                        name__exact=name,
                        group__exact=group,
                        level__exact=level,
                        school_id__exact=school_id
                    ).count() > 0

                    if not exists:

                        SubjectGroup(
                            name=name,
                            group=group,
                            level=level
                        ).save()

        # classes
        elif category == Imports.classes:
            for (i, row) in enumerate(rows):

                if i <= 3:
                    continue

                name = ws.cell(i, 0).value
                class_number = ws.cell(i, 1).value
                stream = ws.cell(i, 2).value
                level_short = ws.cell(i, 3).value
                curriculum = ws.cell(i, 4).value

                # pass if class already exists
                exists = SchoolClass.objects.filter(name__exact=name,
                                                    stream__exact=stream,
                                                    school_id=school_id).count() > 0
                if not exists:
                    SchoolClass(
                        name=name,
                        stream=stream,
                        level_short=level_short,
                        class_number=class_number,
                        curriculum=curriculum,
                        school_id=school_id
                    ).save()
