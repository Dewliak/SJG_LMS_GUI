from lmsapi.data_client import DataClient


class DataClientSingleton:
    _instance: DataClient = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DataClient()
        return cls._instance
