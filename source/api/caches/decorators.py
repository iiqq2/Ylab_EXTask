import json
from functools import wraps

from fastapi.responses import JSONResponse
from starlette import status

from source.api.caches.cache import create_cache_data, get_cache_data


def cache_list_response(cache_key_prefix: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            skip, limit = kwargs['skip'], kwargs['limit']
            cache_key = f'{cache_key_prefix}_skip:{skip}_limit:{limit}'
            cache_data = await get_cache_data(cache_key)
            if cache_data:
                return JSONResponse(content=json.loads(cache_data), status_code=status.HTTP_200_OK)
            response = await func(*args, **kwargs)
            content = response.body.decode('utf-8')
            await create_cache_data(key=cache_key, object=content)
            return response
        return wrapper
    return decorator


def cache_item_response(cache_key_prefix: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f'{cache_key_prefix}_{str(kwargs.get('menu_id'))}'
            cache_data = await get_cache_data(cache_key)
            if cache_data:
                return JSONResponse(content=json.loads(cache_data), status_code=status.HTTP_200_OK)
            response = await func(*args, **kwargs)
            await create_cache_data(key=cache_key, object=response.body.decode('utf-8'))
            return response
        return wrapper
    return decorator
