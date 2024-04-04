import asyncio
from api_payok import PayOk
def foo(a,b,c,d):
	return a+b+c+d

async def main():
	pay = PayOk(5701,
	            "9F0F81512FC63F60B984C0695A3EE43C-9FDC27AE78A6AEBCC2218060EC00CA70-9560C6EAE0E0EBC401C8A3C1E8DDE4B4")
	print(await pay.get_balance())


asyncio.run(main())



