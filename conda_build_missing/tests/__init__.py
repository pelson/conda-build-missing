import collections


_DummyPackage = collections.namedtuple('_DummyPackage',
                                       ['pkg_name', 'run_deps', 'build_deps'])


class DummyPackage(_DummyPackage):
    def __new__(cls, name, run_deps=None, build_deps=None):
        return super(DummyPackage, cls).__new__(cls, name, run_deps or (),
                                                build_deps or ())

    def name(self):
        return self.pkg_name

    def get_value(self, item, default):
        if item == 'requirements/run':
            return self.run_deps
        elif item == 'requirements/build':
            return self.build_deps
        else:
            raise AttributeError(item)

    def __repr__(self):
        # For testing purposes, this is particularly convenient.
        return self.name()
