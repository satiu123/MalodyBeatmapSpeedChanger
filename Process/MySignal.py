class Signal():
    def __init__(self):
        self._callbacks = []
    def connect(self, callback):
        self._callbacks.append(callback)

    def emit(self, *args, **kwargs):
        for callback in self._callbacks:
            callback(*args, **kwargs)

signal1=Signal()
'''
    using this signal to update the text in MyText
'''        
signal2=Signal()
'''
    using this signal to pass the version and title to the main window
'''