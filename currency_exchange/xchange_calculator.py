import requests

class GetXchange():
    def process(self, currency):
        try:
            url = "https://api.exchangeratesapi.io/latest?base="+currency
            payload = {}
            headers = {}

            response = requests.get(url, headers=headers, data = payload)
            
            return response

        except Exception as ex:
            return False