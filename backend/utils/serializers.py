from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        include_fields = kwargs.pop('include_fields', set())
        exclude_fields = kwargs.pop('exclude_fields', set())
        super().__init__(*args, **kwargs)

        if include_fields:
            allowed = set(include_fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude_fields:
            for field_name in exclude_fields:
                self.fields.pop(field_name)


def get_fields(obj, *field_names):
    return {field: getattr(obj, field) for field in field_names}


def get_sort_dict(arr: list):
    return [{'label': l, 'filter': f} for l, f in arr]
