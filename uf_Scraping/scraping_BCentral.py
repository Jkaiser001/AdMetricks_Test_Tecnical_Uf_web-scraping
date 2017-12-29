from BeautifulSoup import BeautifulSoup
import requests
from django.conf import settings
class connector_central_bank(object):

	@property
	def get_uf_date(self):

		response= requests.get(settings.URL_CENTRAL_BANK)
		print response.status_code
		page_indicators = BeautifulSoup(response.text)
		valor = page_indicators.findAll("label",{"id":"lblValor1_1"})[0].text\
				.replace(".", "")\
				.replace(",", ".")
		print valor
		#url_serie= page_indicators.findAll("a", {"id": "hypLnk1_1"})[0]["href"]
		return {"date": "", "value": ""}