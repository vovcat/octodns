#
#
#

from ..equality import EqualityTupleMixin


class Change(EqualityTupleMixin):
    def __init__(self, existing, new):
        self.existing = existing
        self.new = new

    @property
    def record(self):
        'Returns new if we have one, existing otherwise'
        return self.new or self.existing

    def _equality_tuple(self):
        return (self.CLASS_ORDERING, self.record.name, self.record._type)


class Create(Change):
    CLASS_ORDERING = 1

    def __init__(self, new):
        super().__init__(None, new)

    @property
    def data(self):
        return {
            'type': 'create',
            'name': self.new.name,
            'new': self.new.data,
            'record_type': self.new._type,
        }

    def __repr__(self, leader=''):
        source = self.new.source.id if self.new.source else ''
        return f'Create {self.new!r} ({source})'


class Update(Change):
    CLASS_ORDERING = 2

    @property
    def data(self):
        return {
            'type': 'update',
            'existing': self.existing.data,
            'name': self.new.name,
            'new': self.new.data,
            'record_type': self.new._type,
        }

    # Leader is just to allow us to work around heven eating leading whitespace
    # in our output. When we call this from the Manager.sync plan summary
    # section we'll pass in a leader, otherwise we'll just let it default and
    # do nothing
    def __repr__(self, leader=''):
        source = self.new.source.id if self.new.source else ''
        return (
            f'Update\n{leader}    {self.existing!r} ->\n'
            f'{leader}    {self.new!r} ({source})'
        )


class Delete(Change):
    CLASS_ORDERING = 0

    def __init__(self, existing):
        super().__init__(existing, None)

    @property
    def data(self):
        return {
            'type': 'delete',
            'existing': self.existing.data,
            'name': self.existing.name,
            'record_type': self.existing._type,
        }

    def __repr__(self, leader=''):
        return f'Delete {self.existing!r}'
