from enum import Enum


class Ty(Enum):
	PAY = 'pay'
	BALANCE = 'api/balance'
	TRANSACTIONS = 'api/transactions'
	PAYOUT = 'api/payout'
	PAYOUT_CREATE = 'api/payout_create'


class Method(Enum):
	GET = 'GET'
	POST = 'POST'
	ANY = 'ANY'