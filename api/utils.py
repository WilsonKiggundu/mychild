import random
import string

import sys


def generate_student_code(admission_number):
    allowed = 'ABCDEFGHJKLMNPQRSTUVWXYZ123456789'
    return ''.join(random.choices(allowed, k=10))