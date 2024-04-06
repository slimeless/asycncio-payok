import asyncio
from aiohttp import ClientSession
from enum import Enum as enum
from payok_enums import Method, Ty
import functools
import logging
import time


class APIRequestLogger:
	def __init__(selff, logger=None, log_level=logging.INFO):
		selff.logger = logger or logging.getLogger(__name__)
		selff.log_level = log_level

	def __call__(selff, func):
		@functools.wraps(func)
		async def wrapper(self, *args, **kwargs):
			if self.logging_enabled:
				start_time = time.time()
				selff.logger.log(selff.log_level, f"Вызов {func.__name__} с аргументами={args} и kwargs={kwargs}")
				try:
					result = await func(self, *args, **kwargs)
				except Exception as e:
					end_time = time.time()
					selff.logger.error(f"Ошибка в {func.__name__}: {str(e)}, заняло {end_time - start_time:.6f} секунд")
					raise e
				end_time = time.time()
				selff.logger.log(selff.log_level,
				                 f"{func.__name__} вернул {result}, заняло {end_time - start_time:.6f} секунд")
				return result
			else:
				return await func(self, *args, **kwargs)

		return wrapper


class BaseSession:
	STATIC_URL = 'https://payok.io/'

	def __init__(self, logging_enabled=False):
		self.logging_enabled = logging_enabled

	@staticmethod
	async def _check_response(response: dict) -> dict:
		"""
        A static method to check the response dictionary for errors and raise an exception if 'status' is 'error'.

        Parameters:
            response (dict): The response dictionary to be checked.

        Returns:
            dict: The input response dictionary.
            :param response:
            :return:
        """
		if response.get('status') == 'error':
			raise Exception(response.get('error_text'))
		return response

	async def _send_req(self, method: enum, url: enum, **kwargs) -> dict:
		"""
        An asynchronous function to send a request using the specified method, URL, and additional keyword arguments.
        :param method: The HTTP method to be used for the request
        :param url: The URL to which the request will be sent
        :param kwargs: Additional keyword arguments to be passed to the request
        :return: The result of checking the response after sending the request
        """
		url = f'{self.STATIC_URL}{url.value}'
		async with ClientSession() as session:
			async with session.request(method.value, url, **kwargs) as response:
				response = await response.json(content_type="text/plain")
				return await self._check_response(response)
