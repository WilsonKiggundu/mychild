import datetime

GENDER = (
    ('M', 'Male'),
    ('F', 'Female')
)

NOK_TYPE = (
    ('Father', 'Father'),
    ('Mother', 'Mother'),
    ('Guardian', 'Guardian'),
)

PROFILE_TYPE = (
    ('Parent', 'Parent'),
    ('Teacher', 'Teacher'),
    ('Student', 'Student'),
    ('Administrator', 'Administrator'),
)

STATUS = (
    ('ACTIVE', 'Active'),
    ('INACTIVE', 'Inactive'),
    ('DELETED', 'Deleted'),
)

CURRICULUM_LEVELS = (
    ('P', 'Primary'),
    ('O', 'O Level'),
    ('A', 'A Level'),
)

ASSESSMENT_TYPES = (
    ('RAW', 'Raw'),
    ('WEIGHTED', 'Weighted'),
    ('AVERAGE', 'Average'),
)

YES_NO = (
    ('Y', 'Yes'),
    ('N', 'No'),
)

PRINCIPAL_SUBSIDIARY = (
    ('P', 'Principal'),
    ('S', 'Subsidiary'),
    ('N', 'None'),
)

MARITAL_STATUS = (
    ('Married', 'Married'),
    ('Single', 'Single'),
)

POST_TYPE = (
    ('Event', 'Event'),
    ('Blog', 'Blog'),
    ('Marks', 'Marks'),
)

ATTACHMENT_TYPE = (
    ('Video', 'Video'),
    ('Picture', 'Picture'),
    ('Audio', 'Audio'),
)

VIEWERS = (
    #('1', 'All Users'),
    ('2', 'Teachers'),
    ('3', 'Parents'),
    ('4', 'Students'),
    ('5', 'Public'),
)

IMPORTS = (
    ('1', 'Students'),
    ('2', 'Teachers'),
    ('3', 'Subjects'),
    ('4', 'Marks'),
    ('5', 'Classes')
)

now = datetime.datetime.now()
year = now.year

YEARS = (
    (year - 1, year - 1),
    (year, year),
    (year + 1, year + 1)
)

TERMS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
)