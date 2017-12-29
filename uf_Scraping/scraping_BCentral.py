from BeautifulSoup import BeautifulSoup
import requests
from django.conf import settings
PAYLOADS_KEY=["h_calendario","__EVENTVALIDATION"]
class connector_central_bank(object):



	def generate_payload(self):
		response = requests.get(settings.URL_CENTRAL_BANK)
		payload = {}
		page_indicators = BeautifulSoup(response.text)
		input_names_page = page_indicators.findAll("input", {"type": "hidden"})
		for input in input_names_page:
			if input["name"] in PAYLOADS_KEY:
				payload[input["name"]] = input["value"]
		return payload

	def get_uf_date(self, date):

		payload = self.generate_payload()
		payload["h_calendario"] = date.strftime("%Y.%m.%d") + ";" + date.strftime("%Y.%m.%d")
		headers = {'content-type': "application/x-www-form-urlencoded"}
		response = requests.post(settings.URL_CENTRAL_BANK, headers=headers, data=payload)
		page_indicators = BeautifulSoup(response.text)

		value = page_indicators.find("label", {"id": "lblValor1_1"}).text\
			.replace(".", "")\
			.replace(",", ".")
		return {"date": date.strftime("%Y/%m/%d"), "value": value}

	def get_uf_list(self):

		response = requests.get(settings.URL_CENTRAL_BANK)
		#url_serie= page_indicators.findAll("a", {"id": "hypLnk1_1"})[0]["href"]
		return []