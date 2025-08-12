from .utils.cache import RedisCache
from typing import Union
from .config import Config
from .utils.kafka_logger import KafkaLogger
from .models import RequestLog
from .database import db

# ——— Initialize Redis & Kafka ———
# cache = redis.Redis.from_url(Config.REDIS_URL)
cache = RedisCache(Config.REDIS_URL)
kafka = KafkaLogger(bootstrap_servers=Config.KAFKA_BOOTSTRAP)


# ——— Helper: log to DB + Kafka ———
def _log_request(endpoint: str, inp: str, result: Union[int, str]):
    # Persist to SQL
    log = RequestLog(endpoint=endpoint, input_value=inp, result=str(result))
    db.session.add(log)
    db.session.commit()
    # Stream to Kafka
    kafka.send(
        "request_logs", {"endpoint": endpoint, "input": inp, "result": str(result)}
    )


# ——— Power function ———
def pow_service(base: int, exp: int) -> int:
    key = f"pow:{base}:{exp}"
    # 1) Try cache
    # if (cached := cache.get(key)) is not None:
    # return int(cached)

    if (cached := cache.get(key)) is not None:
        return int(cached)
    # 2) Compute
    result = base**exp
    # 3) Cache & log
    cache.set(key, result)
    _log_request("pow", f"{base},{exp}", result)
    return result


# ——— Nth Fibonacci (iterative) ———
def fib_service(n: int) -> int:
    key = f"fib:{n}"
    if (cached := cache.get(key)) is not None:
        return int(cached)
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    result = a
    cache.set(key, result)
    _log_request("fib", str(n), result)
    return result


# ——— Factorial ———
def fact_service(n: int) -> int:
    key = f"fact:{n}"
    if (cached := cache.get(key)) is not None:
        return int(cached)
    result = 1
    for i in range(2, n + 1):
        result *= i
    cache.set(key, result)
    _log_request("factorial", str(n), result)
    return result
