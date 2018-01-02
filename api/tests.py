from django.test import TestCase

# Create your tests here.
from api.models import School


class SchoolModelTestCase(TestCase):
    def setUp(self):
        self.name = "Gayaza High School"
        self.email = "info@school.com"
        self.telephone = "+256414123456"
        self.address = "gayaza"
        self.school = School(name=self.name, address=self.address, telephone=self.telephone, email=self.email, id=12)
        self.school2 = School(name="Old Kampala SSS", address=self.address, telephone=self.telephone, email=self.email, id=12)


    def test_model_can_create_a_school(self):
        old_count = School.objects.count()
        self.school.save()

        new_count = School.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_not_create_schools_with_same_id(self):
        self.school.save()
        self.school2.save()
        schools = School.objects.values_list('id')

        # id exists
        if self.school2.id in schools:
            self.assertFalse()
