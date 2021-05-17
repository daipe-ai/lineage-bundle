class ParsedNotebookFunctionsRelation:
    def __init__(self, source, target):
        self.__source = source
        self.__target = target

    @property
    def source(self):
        return self.__source

    @property
    def target(self):
        return self.__target
