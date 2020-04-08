import aiohttp
import asyncio


            
if __name__ == '__main__':
    print('1')
    loop = asyncio.get_event_loop()
    print('2')
    async with aiohttp.ClientSession(loop=loop) as session:
        print(3)
        await session.close()

    
exit(1)
