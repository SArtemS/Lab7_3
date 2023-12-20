import asyncio


class EchoClientProtocol:

    def __init__(self, on_con_lost):
        self.message = input("Введите сообщение:\n")
        self.on_con_lost = on_con_lost
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print('Send:', self.message)
        self.transport.sendto(self.message.encode())

    def datagram_received(self, data, addr):
        print("Received:", data.decode())
        # При получении сообщения "Bye!" от сервера, его соединение с клиентом оборвётся
        if data.decode() == "Bye!":
            print("Close the socket")
            self.transport.close()
        # Иначе "диалог" будет продолжаться до зактрытия сервера
        else:
            self.message = input("Введите сообщение:\n")
            self.connection_made(self.transport)

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Connection closed")
        self.on_con_lost.set_result(True)


async def main():
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoClientProtocol(on_con_lost),
        remote_addr=('127.0.0.1', 9999))

    try:
        await on_con_lost
    finally:
        transport.close()


asyncio.run(main())
