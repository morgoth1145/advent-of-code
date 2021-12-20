import numpy

class _Vec3D:
    __slots__ = ('_data',)

    def __init__(self, arr):
        self._data = arr

    @property
    def x(self):
        return self._data[0]

    @property
    def y(self):
        return self._data[1]

    @property
    def z(self):
        return self._data[2]

    def dot(self, other):
        return numpy.dot(self._data, other._data)

    def cross(self, other):
        return _Vec3D(numpy.cross(self._data, other._data))

    @property
    def magnitude(self):
        return numpy.linalg.norm(self._data)

    def __neg__(self):
        return _Vec3D(-self._data)

    def __add__(self, other):
        return _Vec3D(self._data + other._data)

    def __iadd__(self, other):
        # Don't use +=, numpy sometimes complains when switching data types!
        self._data = self._data + other._data
        return self

    def __sub__(self, other):
        return _Vec3D(self._data - other._data)

    def __isub__(self, other):
        # Don't use -=, numpy sometimes complains when switching data types!
        self._data = self._data - other._data
        return self

    def __mul__(self, val):
        return _Vec3D(self._data * val)

    def __rmul__(self, val):
        return _Vec3D(val * self._data)

    def __imul__(self, val):
        # Don't use *=, numpy sometimes complains when switching data types!
        self._data = self._data * val
        return self

    def __truediv__(self, val):
        return _Vec3D(self._data / val)

    def __itruediv__(self, val):
        # Don't use /=, numpy sometimes complains when switching data types!
        self._data = self._data / val
        return self

    def __floordiv__(self, val):
        return _Vec3D(self._data // val)

    def __ifloordiv__(self, val):
        # Don't use //=, numpy sometimes complains when switching data types!
        self._data = self._data // val
        return self

    def __hash__(self):
        # There may be a faster no-copy approach
        return hash(self._data.tobytes())

    def __eq__(self, other):
        return numpy.array_equal(self._data, other._data)

    def __iter__(self):
        return iter(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def __repr__(self):
        return f'Vec3D({self.x}, {self.y}, {self.z})'

def Vec3D(x, y, z):
    return _Vec3D(numpy.array((x, y, z)))
Point3D = Vec3D

X_AXIS = Vec3D(1, 0, 0)
Y_AXIS = Vec3D(0, 1, 0)
Z_AXIS = Vec3D(0, 0, 1)

# Rotations only!
class _Mat3D:
    __slots__ = ('_data',)

    def __init__(self, matrix):
        self._data = matrix

    def __mul__(self, other):
        t = type(other)
        if t == _Vec3D:
            return _Vec3D(numpy.asarray(numpy.dot(other._data, self._data)).flatten())
        val = other._data if t == _Mat3D else other
        return _Mat3D(self._data * val)

    def __imul__(self, other):
        val = other._data if isinstance(other, _Mat3D) else other
        # Don't use *=, numpy sometimes complains when switching data types!
        self._data = self._data * val
        return self

    def __truediv__(self, val):
        return _Mat3D(self._data / val)

    def __itruediv__(self, val):
        # Don't use /=, numpy sometimes complains when switching data types!
        self._data = self._data / val
        return self

    def __floordiv__(self, val):
        return _Mat3D(self._data // val)

    def __ifloordiv__(self, val):
        # Don't use //=, numpy sometimes complains when switching data types!
        self._data = self._data // val
        return self

    def __hash__(self):
        # There may be a faster no-copy approach
        return hash(self._data.tobytes())

    def __eq__(self, other):
        return numpy.array_equal(self._data, other._data)

    def __repr__(self):
        # Base on the string representation of the underlying matrix
        # That will do some nice column alignment!
        x, y, z = str(self._data).splitlines()
        return f'Mat3D({x[1:]},\n      {y[1:]},\n      {z[1:-1]})'

def Mat3D(x_axis=X_AXIS, y_axis=Y_AXIS, z_axis=None):
    if z_axis is None:
        z_axis = x_axis.cross(y_axis)
    return _Mat3D(numpy.matrix((list(x_axis),
                                list(y_axis),
                                list(z_axis))))
