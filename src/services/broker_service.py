import redis.asyncio as redis
import asyncio 
from config import settings
from time import sleep
from .redis_service import RedisManager
from abc import ABC, abstractmethod
from typing import Callable




class Broker:
    
    __singletone = None


    def __new__(cls, RedisConnection, *args, **kwargs):
        if cls.__singletone is None:
            cls.__singletone = super().__new__(cls, *args, **kwargs)
        return cls.__singletone

    def __init__(self, RedisConnection):
        self.redis = RedisConnection
        self.pubsub = self.redis.pubsub()
        self.channels_counter = 0
        
            
    async def publish(self, channel: str, message: str):
        try: 
            await self.redis.publish(channel, message)
        except Exception:
            print("Я не знаю пока что не так, но что-то не так") 
    
    async def subscribe(self, channel: str, handler: Callable = None):
        async with self.pubsub as pubsub:
            if handler:
                await pubsub.subscribe(**{channel: handler})
            else:
                await pubsub.subscribe(channel)
                
            if self.channels_counter == 0:
                asyncio.create_task(self.__listener(pubsub))
            
        self.channels_counter += 1
            
    
    async def __listener(self, channel: redis.client.PubSub):
        while True:
            message = await channel.get_message(ignore_subscribe_messages=True)
            if message is not None:
                if message["data"].decode() == "GOVNO":
                    print("(Reader) STOP")
                    break
                
                

broker = Broker(RedisManager.get_connection())

    

        
