class FakeRedisCacheClient:

    def __init__(self, host: str = '', port: str = '', db: str = '0'):
        self.host = host
        self.port = port
        self.db = db
        self.pipeline: list | None = None

    async def get(self, key: str) -> None:
        return None

    async def set(self, key: str, value: dict | list | str) -> bool:
        return False

    def set_pipeline(self):
        self.pipeline = []

    def pset(self, key: str, value: dict | list | str):
        if self.pipeline is None:
            self.set_pipeline()
        self.pipeline.append(False)

    def pget(self, key: str):
        if self.pipeline is None:
            self.set_pipeline()
        self.pipeline.append(None)

    async def execute_pipeline(self):
        result = self.pipeline
        self.set_pipeline()
        return result
