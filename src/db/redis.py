from redis import asyncio as aioredis
from src.config import Config

JTI_EXPIRY = 3600
token_block_list = aioredis.StrictRedis(
    host=Config.redis_host, port=Config.redis_port, db=0
)


async def add_jti_to_block_list(jti: str):
    await token_block_list.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_block_list(jti: str):
    jti = await token_block_list.get(jti)
    return jti is not None
