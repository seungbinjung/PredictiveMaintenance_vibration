import asyncio

class SSEManager:
    def __init__(self):
        self.connections = []  # 연결된 클라이언트들의 큐

    def subscribe(self):
        queue = asyncio.Queue()
        self.connections.append(queue)
        return queue

    def unsubscribe(self, queue):
        if queue in self.connections:
            self.connections.remove(queue)

    async def broadcast(self, data):
        if len(self.connections) == 0:
            return
        for queue in list(self.connections):
            await queue.put(data)

sse_manager = SSEManager()
