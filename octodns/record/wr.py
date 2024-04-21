#
#
#

from .base import Record, ValueMixin


class WrValue(str):
    def __new__(cls, v):
        return super().__new__(cls, v)

    @classmethod
    def validate(cls, data, _type):
        reasons = []
        if data == '':
            reasons.append('empty value')
        elif not data:
            reasons.append('missing value')
        return reasons

    @classmethod
    def parse_rdata_text(cls, value):
        return value

    @classmethod
    def process(cls, value):
        if value:
            return cls(value)
        return None

    @property
    def rdata_text(self):
        return self

class WrRecord(ValueMixin, Record):
    _type = 'WR'
    _value_type = WrValue

    def __repr__(self):
        cls = self.__class__.__name__
        octodns = f', {self.octodns}' if self.octodns else ''
        value = self.value[:60]+'...' if len(self.value) > 60 else self.value
        return f"<{cls} {self._type} {self.ttl}, {self.decoded_fqdn}, {value!r}{octodns}>"

Record.register_type(WrRecord)
