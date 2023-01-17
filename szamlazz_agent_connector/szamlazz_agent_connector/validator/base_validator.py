import inspect


class BaseValidator:
    def check_fields(self, obj):
        fields = inspect.getmembers(obj, lambda a: not (inspect.isroutine(a)))
        fields = [a for a in fields if not (a[0].startswith('__') and a[0].endswith('__'))]
        for item in fields:
            self._check_field(item[0], item[1])

    def _check_field(self, field, value):
        pass
