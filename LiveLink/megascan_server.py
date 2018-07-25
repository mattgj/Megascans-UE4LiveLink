import unreal_engine as ue
import asyncio
import ue_asyncio

# cleanup previous tasks
for task in asyncio.Task.all_tasks():
    task.cancel()

# this is called whenever a new client connects
async def new_client_connected(reader, writer):
    name = writer.get_extra_info('peername')
    ue.log('new client connection from {0}'.format(name))
    # whole_data will contain the whole stream of bytes
    whole_data = b''
    # continue reading until the client does not close the connection
    while True:
        # tune 4096 to something more suitable
        data = await reader.read(4096)
        # connection closed
        if not data:
            break
        # append data until the connection is closed
        whole_data += data

    # check if the client sent something (whole_data.decode() will transform the byte stream to a string)
    if len(whole_data) > 0:
        ue.log('client {0} issued: {1}'.format(name, whole_data.decode()))
        # do something with the whole_data stuff
    ue.log('client {0} disconnected'.format(name))

# this spawns the server
# the try/finally trick allows for gentle shutdown of the server
# see https://github.com/20tab/UnrealEnginePython/blob/master/tutorials/AsyncIOAndUnrealEngine.md
# for more infos about exception management
async def spawn_server(host, port):
    try:
        # reuse_address will allow to rebind multiple times
        coro = await asyncio.start_server(new_client_connected, host, port, reuse_address=True)
        ue.log('tcp server spawned on {0}:{1}'.format(host, port))
        # continue until the server is not closed (should never happens)
        await coro.wait_closed()
    finally:
        coro.close()
        ue.log('tcp server ended')
    
# spawn the server coroutine (no need for timers or sleeps)
asyncio.ensure_future(spawn_server('127.0.0.1', 16384))