from BeautifulSoup import BeautifulSoup
import requests
import dryscrape
from django.conf import settings
from django.core.cache import caches

from datetime import datetime, timedelta;



class ConnectorCentralBank(object):

	def __init__(self):

		self.session = requests.session()
		self.link = self.obtain_link_serie()

	def generate_payload(self, response):

		payload = {}

		page_indicators = BeautifulSoup(response.text)
		input_names_page = page_indicators.findAll("input", {"type": "hidden"})
		for input in input_names_page:
			# if input["name"] in PAYLOADS_KEY:
			payload[input["name"]] = input["value"]
		return payload

	def obtain_link_serie(self):
		cache = caches["default"]
		link = cache.get("link_serial")
		if link is not None:
			return link
		response = self.session.get(settings.URL_CENTRAL_BANK + "/Indicadoresdiarios.aspx")
		page_indicators = BeautifulSoup(response.text)
		link = page_indicators.find("a", {"id": "hypLnk1_1"})["href"]
		cache.set("link_serial",link)
		return link

	def obtain_years(self, response):

		years = []
		page_serial = BeautifulSoup(response)
		list_options = page_serial.find('select',{"name":"DrDwnFechas"}).findChildren()

		for option in list_options:
			years.append(option.get("value"))

		return years

	def get_uf_date(self, date):

		response = self.session.get(settings.URL_CENTRAL_BANK + "/Indicadoresdiarios.aspx")
		payload = self.generate_payload(response)
		payload["h_calendario"] = date.strftime("%Y.%m.%d") + ";" + (date.replace(day=1) - timedelta(days=1)).replace(day=1).strftime("%Y.%m.%d")

		print payload["h_calendario"]
		headers = {'content-type': "application/x-www-form-urlencoded"}

		response = requests.post(settings.URL_CENTRAL_BANK+"/Indicadoresdiarios.aspx", headers=headers, data=payload)
		page_indicators = BeautifulSoup(response.text)

		print (page_indicators.find("input", {"name": "txtDate"}))["value"]

		value = page_indicators.find("label", {"id": "lblValor1_1"}).text \
			.replace(".", "") \
			.replace(",", ".")
		return {"date": date.strftime("%Y%m%d"), "value": value}

	def get_uf_yearly(self, year):
		headers = {'content-type': "application/x-www-form-urlencoded"}
		session = dryscrape.Session()

		session.visit(settings.URL_CENTRAL_BANK + "/" + self.link)
		response = session.body()
		years = self.obtain_years(response)
		soup = BeautifulSoup(response)
		for i in range(1, len(years)+1):

			drFechas = session.at_xpath('//*[@id="DrDwnFechas"]/option['+str(i)+']')

			drFechas.select_option()

			soup = BeautifulSoup(session.body())
			serie_grid = soup.find('table','Grid').find("tbody").findAll("tr")

			serie_grid.pop(0)
			for row in range(len(serie_grid)):
				element_grid = serie_grid[row]
				list_col = element_grid.findAll("td")
				day = list_col.pop(0).text
				for col in range(0, len(list_col)):

					value = list_col[col].find("span").text
					if len(value) > 0:
						print day, col+1, years[i-1], value

		#payload = self.generate_payload(response)
		#print response.cookies
		#years = self.obtain_years(response)
		#payload["__EVENTTARGET"] = "DrDwnFechas"
		'''
		for year in years:
			print "___________________________" + str(year) + "___________________________"
			payload["DrDwnFechas"] = str(year)
			for (key, value) in payload.items():
				print key, ": ", value

			response = self.session.post(settings.URL_CENTRAL_BANK + "/" + self.link, data=payload, headers=headers)
			page_serial = BeautifulSoup(response.text).find("option", {"selected": "selected"})["value"]
			print response.text
			print "______________________________________________________"

		'''
		return {}

