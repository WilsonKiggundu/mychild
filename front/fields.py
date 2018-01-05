from django.forms import ModelChoiceField


class SubjectModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name
