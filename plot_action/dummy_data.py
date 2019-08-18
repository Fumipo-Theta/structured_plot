from data_loader import IDataLoader


class DummyData:
    def __init__(self):
        pass

    def __len__(self):
        return 1


class DummyLoader(IDataLoader):
    def __init__(self):
        pass

    def read(self, *arg, **kwargs):
        return DummyData()

    def query(self, *arg, **kwargs):
        return DummyData()
