import asyncio

class SSEManager:
    def __init__(self):
        self.vibration_connections = []  # 연결된 클라이언트들의 큐
        self.result_connections = []
        #진동 파트
    def subscribe_vibration(self):
        queue = asyncio.Queue()
        self.vibration_connections.append(queue)
        return queue

    def unsubscribe_vibration(self, queue):
        if queue in self.vibration_connections:
            self.vibration_connections.remove(queue)

    async def broadcast_vibration(self, data):
        if len(self.vibration_connections) == 0:
            return
        for queue in list(self.vibration_connections):
            await queue.put(data)

        # 새로운 설비 상태 SSE
    def subscribe_result(self):
        queue = asyncio.Queue()
        self.result_connections.append(queue)
        return queue

    async def broadcast_result(self, data):
        for q in list(self.result_connections):
            await q.put(data)

sse_manager = SSEManager()
