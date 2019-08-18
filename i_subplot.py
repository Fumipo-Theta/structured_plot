import pandas as pd
from abc import ABC, abstractmethod
from data_loader import DictLoader, DataFrameLoader, TableLoader, TestLoader
from .plot_action import DummyLoader


class ISubplot(ABC):

    @abstractmethod
    def plot(self, ax, test=False):
        return ax

    @abstractmethod
    def get_axes_spec(self):
        pass

    @abstractmethod
    def set_test_mode(self, test):
        self._isTest = test
        return self

    @abstractmethod
    def isTest(self):
        return self._isTest

    @staticmethod
    def IDataLoader(data_source, isTest):
        if isTest:
            return TestLoader()

        elif type(data_source) == dict:
            return DictLoader()

        elif type(data_source) in [pd.Series, pd.DataFrame]:
            return DataFrameLoader()

        elif data_source is None:
            return DummyLoader()

        else:
            # path like values of data source
            return TableLoader()
