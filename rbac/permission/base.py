class BasePermission(object):
    def __init__(self,codes):
        self.codes = codes

    def list(self):
        if 'list' in self.codes:
            return True

    def add(self):
        if 'add' in self.codes:
            return True

    def edit(self):
        if 'edit' in self.codes:
            return True

    def delete(self):
        if 'del' in self.codes:
            return True
