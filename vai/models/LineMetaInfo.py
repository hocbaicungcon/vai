from vaitk import core
import collections

# New class to store meta information in a separate
# object, so that we can listen to specific notifications
# from specific meta objects. We need to keep it synchronized
# to the current document though.
class LineMetaInfo:
    def __init__(self, meta_type, document):
        self._meta_type = meta_type
        self._document = document
        self._data = [None] * self._document.numLines()

        self.contentChanged = core.VSignal(self)

    def numLines(self):
        return len(self._data)

    def addLines(self, line_number, how_many):
        for i in range(how_many):
            self._data.insert(line_number-1, None)
        self.notifyObservers()

    def deleteLines(self, line_number, how_many):
        for i in range(how_many):
            self._data.pop(line_number-1)
        self.notifyObservers()

    def setData(self, from_line, data):
        # As a method, so we can bind to it via signal/slot. Property with slice needed.
        if not isinstance(data, collections.Iterable) or isinstance(data, str):
            data = [ data ]

        try:
            for idx, d in enumerate(data):
                self._data[from_line-1+idx] = d
        except IndexError:
            pass

        self.notifyObservers()

    def data(self, from_line, how_many=None):
        if how_many is None:
            how_many = 1

        return self._data[from_line-1:from_line-1+how_many]

    def clear(self):
        self._data = [None] * self._document.numLines()
        self.notifyObservers()

    def notifyObservers(self):
        self.contentChanged.emit()

    @property
    def meta_type(self):
        return self._meta_type

    @property
    def document(self):
        return self._document