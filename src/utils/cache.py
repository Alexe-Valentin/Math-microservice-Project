import redis
from redis import Redis
from redis.exceptions import RedisError
from typing import Optional


class RedisCache:
    def __init__(self, url: str):
        self.url = url
        self._client: Optional[Redis] = None

    def _ensure_client(self) -> None:
        if self._client is None:
            try:
                client = redis.Redis.from_url(self.url)
                client.ping()
                self._client = client
            except RedisError:
                self._client = None

    def get(self, key: str) -> Optional[bytes]:
        self._ensure_client()
        if not self._client:
            return None
        try:
            return self._client.get(key)
        except RedisError:
            return None

    def set(self, key: str, value, ex: Optional[int] = None) -> None:
        self._ensure_client()
        if not self._client:
            return
        try:
            self._client.set(key, value, ex=ex)
        except RedisError:
            pass
