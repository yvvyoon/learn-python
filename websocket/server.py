import asyncio
import websockets


entered_clients = set()


async def echo(websocket):
    print(f'websocket: {websocket}')
    print(f'type of websocket: {type(websocket)}')

    entered_clients.add(websocket)

    try:
        async for message in websocket:
            print(f'Received message: {message}')

            for client in entered_clients:
                await client.send(message)
    except websocket.exception.ConnectionClosed as error:
        print(f'Error: {error}')
    finally:
        entered_clients.remove(websocket)


async def main():
    server = await websockets.serve(echo, 'localhost', 8765)

    await server.wait_closed()


asyncio.run(main())
