import websockets
import asyncio
import html
import json

#Websocket'e bağlanan kullanıcıyı client listesine ekler. İstemciye odada kaç kişi olduğunu bildirir.
async def register(websocket):
    clients.add(websocket)
    data = {"user_count": len(clients)}
    for client in clients:
        await client.send(json.dumps(data))

#İstemcinin bağlantısı kesildiğinde mevcut kullanıcılar listesinden çıkarır. İstemciye odada kaç kişi olduğunu bildirir.
async def unregister(websocket):
    clients.remove(websocket)
    data = {"user_count": len(clients)}
    for client in clients:
        await client.send(json.dumps(data))

#Websocket bağlantısını yöneten ana fonksiyon
async def communication_handler(websocket, path):

    await register(websocket)

    try:
        # Websocket üzerinden gelen her bir mesaj için işlem yapıyoruz.
        async for message in websocket:
            #print(message, websocket)

            data = json.loads(message)#Gelen veri dict objesine dönüştürülür.

            #print(data)
            if ("message" not in data): #Yeni kullanıcı katıldığında diğer kullanıcılara kullanıcı katıldı mesajı.
                data['user_join'] = "joined the chat."
            for client in clients:
                await client.send(json.dumps(data))

    finally:
        await unregister(websocket)

if __name__ == "__main__":
    clients = set()
    start_server = websockets.serve(communication_handler, '0.0.0.0', 5678) #Bağlantı yapılan IP adresi ve port numarası
    asyncio.get_event_loop().run_until_complete(start_server) #
    asyncio.get_event_loop().run_forever()