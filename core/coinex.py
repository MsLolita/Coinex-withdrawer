import ccxt.async_support as ccxt


class Coinex:
    def __init__(self, access_id: str, secret_key: str):
        self.exchange = ccxt.coinex({
            'enableRateLimit': True,
            'apiKey': access_id,
            'secret': secret_key,
        })

    async def withdraw(self, currency: str, amount: float, address: str, params=None):
        if params is None:
            params = {}
        return await self.exchange.withdraw(currency, amount, address, params=params)

