# Python Language Reference

> Source: Context7 — Python 3.15 official documentation
> Library: /websites/python_3_15

---

## Async/Await and Asyncio

### Asynchronous Generators (PEP 525)

Combines `await` and `yield` in the same function body:

```python
async def ticker(delay, to):
    """Yield numbers from 0 to *to* every *delay* seconds."""
    for i in range(to):
        yield i
        await asyncio.sleep(delay)
```

### Async Context Managers

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_connection():
    conn = await acquire_db_connection()
    try:
        yield conn
    finally:
        await release_db_connection(conn)

async def get_all_users():
    async with get_connection() as conn:
        return conn.query('SELECT ...')
```

### Asyncio Patterns

```python
import asyncio

async def fetch(url: str) -> str:
    # Simulated async I/O
    await asyncio.sleep(1)
    return f"Response from {url}"

async def main():
    # Run concurrently
    results = await asyncio.gather(
        fetch("url1"),
        fetch("url2"),
        fetch("url3"),
    )

    # Create tasks
    task = asyncio.create_task(fetch("url4"))
    result = await task

    # Timeout
    try:
        result = await asyncio.wait_for(fetch("url5"), timeout=2.0)
    except asyncio.TimeoutError:
        print("Timed out")

    # Semaphore for concurrency limiting
    sem = asyncio.Semaphore(10)
    async with sem:
        await fetch("url6")

asyncio.run(main())
```

---

## Dataclasses

### Basic Dataclass

```python
from dataclasses import dataclass

@dataclass
class InventoryItem:
    """Class for keeping track of an item in inventory."""
    name: str
    unit_price: float
    quantity_on_hand: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand
```

### Simple Dataclass

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0

p = Point(1.5, 2.5)
print(p)   # produces "Point(x=1.5, y=2.5, z=0.0)"
```

### Advanced Dataclass Features

```python
from dataclasses import dataclass, field, asdict, astuple
from typing import ClassVar

@dataclass(frozen=True, slots=True, order=True)
class ImmutablePoint:
    sort_index: float = field(init=False, repr=False)
    x: float
    y: float

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.x + self.y)

@dataclass
class Config:
    name: str
    tags: list[str] = field(default_factory=list)
    _registry: ClassVar[dict] = {}

    def __post_init__(self):
        Config._registry[self.name] = self
```

---

## Type Hints and Typing

### Generator Type Annotations

```python
from typing import Generator

def echo_round() -> Generator[int, float, str]:
    sent = yield 0
    while sent >= 0:
        sent = yield round(sent)
    return 'Done'

# Simple generator (no send/return)
def infinite_stream(start: int) -> Generator[int]:
    while True:
        yield start
        start += 1
```

### Common Type Patterns

```python
from typing import (
    Any, Union, Optional, Literal, TypeVar, Generic,
    Protocol, TypeAlias, TypeGuard, Annotated,
    Callable, Sequence, Mapping, Iterator,
    ClassVar, Final, overload, runtime_checkable,
)
from collections.abc import Awaitable

# Type aliases
Vector: TypeAlias = list[float]

# TypeVar
T = TypeVar('T')
K = TypeVar('K', str, int)  # constrained

# Generic class
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# Protocol (structural subtyping)
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...

# Overloads
@overload
def process(x: int) -> int: ...
@overload
def process(x: str) -> str: ...
def process(x: int | str) -> int | str:
    if isinstance(x, int):
        return x * 2
    return x.upper()

# TypeGuard
def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

# Annotated
UserId = Annotated[int, "Must be positive"]
```

---

## Decorators

### Preserving Function Metadata with functools.wraps

```python
from functools import wraps

def my_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        print('Calling decorated function')
        return f(*args, **kwds)
    return wrapper

@my_decorator
def example():
    """Docstring"""
    print('Called example function')

example()
print(example.__name__)   # 'example'
print(example.__doc__)    # 'Docstring'
```

### Decorator Patterns

```python
from functools import wraps
import time

# Decorator with arguments
def repeat(n: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name: str) -> str:
    print(f"Hello, {name}!")
    return f"greeted {name}"

# Class-based decorator
class Timer:
    def __init__(self, func):
        wraps(func)(self)
        self.func = func

    def __call__(self, *args, **kwargs):
        start = time.perf_counter()
        result = self.func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{self.func.__name__} took {elapsed:.4f}s")
        return result

@Timer
def slow_function():
    time.sleep(1)

# Decorator that works with and without arguments
def decorator(func=None, *, arg1="default"):
    def actual_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(f"arg1={arg1}")
            return f(*args, **kwargs)
        return wrapper
    if func is not None:
        return actual_decorator(func)
    return actual_decorator
```

---

## Context Managers

### ContextDecorator (Class-Based)

```python
from contextlib import ContextDecorator
import logging

logging.basicConfig(level=logging.INFO)

class track_entry_and_exit(ContextDecorator):
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        logging.info('Entering: %s', self.name)

    def __exit__(self, exc_type, exc, exc_tb):
        logging.info('Exiting: %s', self.name)

# As context manager
with track_entry_and_exit('widget loader'):
    print('Some time consuming activity goes here')

# As decorator
@track_entry_and_exit('widget loader')
def activity():
    print('Some time consuming activity goes here')
```

### @contextmanager Decorator

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(*args, **kwds):
    resource = acquire_resource(*args, **kwds)
    try:
        yield resource
    finally:
        release_resource(resource)

with managed_resource(timeout=3600) as resource:
    # Resource is released at the end of this block
    ...
```

### Dual-Purpose Context Manager/Decorator

```python
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO)

@contextmanager
def track_entry_and_exit(name):
    logging.info('Entering: %s', name)
    yield
    logging.info('Exiting: %s', name)

# As decorator
@track_entry_and_exit('widget loader')
def activity():
    print('Some time consuming activity goes here')

# As context manager
with track_entry_and_exit('widget loader'):
    print('Some time consuming activity goes here')
```

---

## Abstract Base Classes

### ABC with Abstract Methods and Properties

```python
class C(ABC):
    @abstractmethod
    def my_abstract_method(self, arg1):
        ...

    @classmethod
    @abstractmethod
    def my_abstract_classmethod(cls, arg2):
        ...

    @staticmethod
    @abstractmethod
    def my_abstract_staticmethod(arg3):
        ...

    @property
    @abstractmethod
    def my_abstract_property(self):
        ...

    @my_abstract_property.setter
    @abstractmethod
    def my_abstract_property(self, val):
        ...

    @abstractmethod
    def _get_x(self):
        ...
    @abstractmethod
    def _set_x(self, val):
        ...
    x = property(_get_x, _set_x)
```

---

## Generators and Iterators

```python
from typing import Generator, Iterator

# Basic generator
def fibonacci() -> Generator[int, None, None]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Generator with send
def accumulator() -> Generator[float, float, str]:
    total = 0.0
    while True:
        value = yield total
        if value is None:
            break
        total += value
    return f"Final total: {total}"

# Generator expression
squares = (x ** 2 for x in range(10))

# yield from (delegation)
def chain(*iterables):
    for it in iterables:
        yield from it

# Custom iterator
class Countdown:
    def __init__(self, start: int):
        self.start = start

    def __iter__(self) -> Iterator[int]:
        n = self.start
        while n > 0:
            yield n
            n -= 1
```

---

## Pathlib

```python
from pathlib import Path

# Path construction
p = Path("/home/user/documents")
config = Path.home() / ".config" / "myapp" / "settings.toml"

# Common operations
p.exists()
p.is_file()
p.is_dir()
p.name          # "file.txt"
p.stem          # "file"
p.suffix        # ".txt"
p.parent        # parent directory
p.resolve()     # absolute path

# Reading/Writing
content = Path("file.txt").read_text(encoding="utf-8")
Path("output.txt").write_text("hello", encoding="utf-8")
data = Path("binary.dat").read_bytes()

# Globbing
for py_file in Path(".").rglob("*.py"):
    print(py_file)

# Directory operations
Path("new_dir").mkdir(parents=True, exist_ok=True)
for item in Path(".").iterdir():
    print(item)
```

---

## Testing with pytest

```python
import pytest

# Basic test
def test_addition():
    assert 1 + 1 == 2

# Parametrized tests
@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("world", 5),
])
def test_length(input: str, expected: int):
    assert len(input) == expected

# Fixtures
@pytest.fixture
def sample_data():
    return {"key": "value", "numbers": [1, 2, 3]}

def test_with_fixture(sample_data):
    assert "key" in sample_data

# Exception testing
def test_raises():
    with pytest.raises(ValueError, match="invalid"):
        int("not_a_number")

# Async tests (with pytest-asyncio)
@pytest.mark.asyncio
async def test_async():
    result = await some_async_function()
    assert result == expected

# Fixtures with cleanup
@pytest.fixture
def temp_file(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("content")
    yield f
    # Cleanup happens automatically with tmp_path

# Conftest for shared fixtures
# conftest.py
@pytest.fixture(scope="session")
def database():
    db = create_test_db()
    yield db
    db.close()
```

---

## Packaging and Virtual Environments

```bash
# Virtual environments
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# pip
pip install package_name
pip install -r requirements.txt
pip freeze > requirements.txt

# pyproject.toml (modern)
```

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "my-package"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.28",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]
```

---

## Useful Standard Library Modules

### functools

```python
from functools import lru_cache, cached_property, partial, reduce

@lru_cache(maxsize=128)
def expensive(n: int) -> int:
    return sum(range(n))

class MyClass:
    @cached_property
    def data(self) -> list:
        return load_expensive_data()

add_five = partial(add, 5)
total = reduce(lambda a, b: a + b, [1, 2, 3, 4])
```

### itertools

```python
from itertools import chain, islice, groupby, product, combinations, count

# Chain iterables
for item in chain([1, 2], [3, 4]):
    print(item)

# Slice iterator
first_10 = list(islice(count(), 10))

# Groupby
data = sorted(items, key=lambda x: x.category)
for key, group in groupby(data, key=lambda x: x.category):
    print(key, list(group))

# Cartesian product
for a, b in product("AB", range(3)):
    print(a, b)
```

### collections

```python
from collections import defaultdict, Counter, deque, namedtuple, OrderedDict

# defaultdict
word_count = defaultdict(int)
for word in words:
    word_count[word] += 1

# Counter
c = Counter("abracadabra")
c.most_common(3)  # [('a', 5), ('b', 2), ('r', 2)]

# deque
d = deque(maxlen=10)
d.append(1)
d.appendleft(0)

# namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
```
