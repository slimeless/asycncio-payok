from base import BaseSession
from payok_enums import Ty, Method
from typing import Optional, Union
import asyncio
from models import Transaction


class PayOk(BaseSession):
	def __init__(
			self,
			api_id: int,
			api_key: str,
			secret_key: Optional[str] = None,
			shop: Optional[int] = None,
	) -> None:
		super().__init__()
		self.__api_id = api_id
		self.__api_key = api_key
		self.__secret_key = secret_key
		self.__shop = shop

	async def get_balance(self):
		method = Method.POST
		data = {
			'API_ID': self.__api_id,
			'API_KEY': self.__api_key,
		}
		return await self._send_req(method, Ty.BALANCE, data=data)

	async def get_transactions(self, payment_id: Optional[int] = None, offset: Optional[int] = None) -> Union[Transaction, list[Transaction]]:
		method = Method.POST
		data = {
			'API_ID': self.__api_id,
			'API_KEY': self.__api_key,
			'shop': self.__shop,
		}
		if payment_id:
			data['payment_id'] = payment_id
		if offset:
			data['offset'] = offset

		res = await self._send_req(method, Ty.TRANSACTIONS, data=data)
		for transaction in res['transactions']:
			transaction['shop'] = self.__shop
		if len(res['transactions']) == 1:
			return Transaction(**res['transactions'][0])
		return [Transaction(**transaction) for transaction in res['transactions']]
