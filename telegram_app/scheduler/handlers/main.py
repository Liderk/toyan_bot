class MainHandler:
    def __init__(self, scheduler):
        self.scheduler = scheduler

    async def iter_all_events(self):
        pass

    async def run(self):
        for data, date in self.iter_scheduled_items():
            pass


    def iter_scheduled_items(self):
        pass
