class UserBot:
    def __init__(self, client):
        self.client = client

    async def start(self):
        await self.client.start()

    async def run(self):
        await self.start()
        await self.client.run_until_disconnected()

