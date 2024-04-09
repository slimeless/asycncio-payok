import asyncio
from logging import info


class Timer:
	def __init__(self):
		self.loop = asyncio.get_event_loop()

	async def __aenter__(self):
		self.start = self.loop.time()

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		self.end = self.loop.time()
		self.interval = self.end - self.start
		info(f"Elapsed time: {self.interval} seconds")


class TimeMeasuringMeta(type):

	def __new__(cls, name, bases, dct):
		# Обертывание каждого асинхронного метода класса
		for attr_name, attr_value in dct.items():
			if callable(attr_value) and asyncio.iscoroutinefunction(attr_value) and not attr_name.startswith('_'):
				dct[attr_name] = cls.wrap_method(attr_value)
		return super().__new__(cls, name, bases, dct)

	@staticmethod
	def wrap_method(method):

		async def wrapper(*args, **kwargs):
			async with Timer():
				return await method(*args, **kwargs)

		return wrapper
