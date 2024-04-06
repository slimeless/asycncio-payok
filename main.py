import asyncio
from api_payok import PayOk
import logging



async def main():
	pay = PayOk(5701,
	            "9F0F81512FC63F60B984C0695A3EE43C-9FDC27AE78A6AEBCC2218060EC00CA70-9560C6EAE0E0EBC401C8A3C1E8DDE4B4",
	            logging_enabled=True)
	data = await pay.get_balance()


if __name__ == "__main__":
	logger = logging.getLogger(__name__)
	logging.basicConfig(level=logging.INFO)
	asyncio.run(main())
