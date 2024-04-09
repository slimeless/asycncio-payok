from asyncio_payok.payok_base import BaseSession
from typing import Optional, Union
from asyncio_payok.const import *
from urllib.parse import urlencode
from urllib.parse import quote
from hashlib import md5


class PayOk(BaseSession):
	def __init__(
			self,
			api_id: int,
			api_key: str,
			secret_key: Optional[str] = None,
			shop: Optional[int] = None,
			*args, **kwargs
	) -> None:
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
		req = await self._send_req(method, Ty.BALANCE, data=data)
		return Balance(**req)

	async def get_transactions(self, payment_id: Optional[int] = None, offset: Optional[int] = None) -> Union[
		Transaction, list[Transaction]]:
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

		res = list((await self._send_req(method, Ty.TRANSACTIONS, data=data)).values())
		transactions = [Transaction(**x) for x in res if isinstance(x, dict)]
		return transactions[0] if len(transactions) == 1 else transactions

	async def __sign(self, params: list) -> str:
		sign = '|'.join(map(str, params)).encode('utf-8')
		return md5(sign).hexdigest()

	async def create_pay(
			self,
			amount: float,
			payment: Union[int, str],
			currency: Optional[str] = Currencies.RUB.value,
			desc: Optional[str] = 'Description',
			email: Optional[str] = None,
			success_url: Optional[str] = None,
			method: Optional[str] = None,
			lang: Optional[str] = None,
			custom: Optional[str] = None,
			zip_url: bool = False
	) -> str:
		url = self.STATIC_URL + Ty.PAY.value + '?'
		if self.__secret_key:
			data = {
				'amount': amount,
				'payment': payment,
				'shop': self.__shop,
				'currency': currency,
				'desc': desc,
				'email': email,
				'success_url': success_url,
				'method': method,
				'lang': lang,
				'custom': custom
			}
			for key, value in list(data.items()):
				if value is None:
					del data[key]
			data['sign'] = await self.__sign([*list(data.values())[:5], self.__secret_key])
		else:
			raise Exception('Secret key is required')

		if zip_url:
			return quote(url + urlencode(data), safe='')
		return url + urlencode(data)

	async def get_payout(self,
	                     payout: Optional[int] = None,
	                     offset: Optional[int] = None):
		method = Method.POST
		data = {
			'API_ID': self.__api_id,
			'API_KEY': self.__api_key,
		}
		if payout:
			data['payout'] = payout
		if offset:
			data['offset'] = offset
		res = list((await self._send_req(method, Ty.PAYOUT, data=data)).values())
		payouts = [Payout(**x) for x in res if isinstance(x, dict)]
		return payouts[0] if len(payouts) == 1 else payouts

	async def create_payout(
			self,
			amount: float,
			receiver: str,
			sbp_bank: Optional[str] = None,
			commission_type: str = 'balance',
			webhook_url: Optional[str] = None,
			method: str = 'card',
	) -> CreatedPayout:

		method_http = Method.POST
		data = {
			'API_ID': self.__api_id,
			'API_KEY': self.__api_key,
			'amount': amount,
			'receiver': receiver,
			'sbp_bank': sbp_bank if sbp_bank else None,
			'commission_type': commission_type,
			'webhook_url': webhook_url if webhook_url else None,
			'method': method
		}
		data = {key: value for key, value in data.items() if value is not None}

		req = await self._send_req(method_http, Ty.PAYOUT_CREATE, data=data)

		return CreatedPayout(**req)
