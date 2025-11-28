import aiohttp

async def send_prediction_request_async(endpoint, arr):
    if type(arr) != list:
        arr = arr.tolist()

    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, json={"input": arr}) as resp:
            return await resp.json()
