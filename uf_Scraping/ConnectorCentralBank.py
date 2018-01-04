from BeautifulSoup import BeautifulSoup
import requests
import dryscrape
from django.conf import settings
from django.core.cache import caches

from datetime import datetime, timedelta;

import logging



class ConnectorCentralBank(object):

	def __init__(self):

		self.link = self.obtain_link_serie()
		self.logger = logging.getLogger("central_bank")

	########################################################################
	##  Scrape the page searched name to payload need to send a post call ##
	##  INPUT:  Response html to page to scrape                           ##
	##  OUTPUT: List hiostorical of values in central bank web page       ##
	########################################################################
	def generate_payload(self, response):

		payload = {}

		page_indicators = BeautifulSoup(response.text)
		input_names_page = page_indicators.findAll("input", {"type": "hidden"})
		for input in input_names_page:
			# if input["name"] in PAYLOADS_KEY:
			payload[input["name"]] = input["value"]
		return payload

	#######################################################################
	##  Scrape the page in search de link for access to serie values     ##
	##  INPUT:                                                           ##
	##  OUTPUT: link to access serie information                         ##
	#######################################################################
	def obtain_link_serie(self):
		cache = caches["default"]
		link = cache.get("link_serial")
		if link is not None:
			return link
		session = requests.session()
		response = session.get(settings.URL_CENTRAL_BANK + "/Indicadoresdiarios.aspx")
		page_indicators = BeautifulSoup(response.text)
		link = page_indicators.find("a", {"id": "hypLnk1_1"})["href"]
		cache.set("link_serial",link)
		return link

	#######################################################################
	##  scrape the page searched all years avalibles in  web page        ##
	##  INPUT: response html to page to scrape                           ##
	##  OUTPUT: List with de years in the web page                       ##
	#######################################################################
	def obtain_years(self, response):

		years = []
		page_serial = BeautifulSoup(response)
		list_options = page_serial.find('select',{"name":"DrDwnFechas"}).findChildren()

		for option in list_options:
			years.append(option.get("value"))

		return years

	#######################################################################
	##  scrape the page searched once value UF in a date determinated    ##
	##  INPUT: date when search UF value                                 ##
	##  OUTPUT: List hiostorical of values in central bank web page      ##
	#######################################################################
	def get_uf_date(self, date):

		response = self.session.get(settings.URL_CENTRAL_BANK + "/Indicadoresdiarios.aspx")
		payload = self.generate_payload(response)
		payload["h_calendario"] = date.strftime("%Y.%m.%d") + ";" + (date.replace(day=1) - timedelta(days=1)).replace(day=1).strftime("%Y.%m.%d")

		# print payload["h_calendario"]
		headers = {'content-type': "application/x-www-form-urlencoded"}

		response = requests.post(settings.URL_CENTRAL_BANK+"/Indicadoresdiarios.aspx", headers=headers, data=payload)
		page_indicators = BeautifulSoup(response.text)

		# print (page_indicators.find("input", {"name": "txtDate"}))["value"]

		value = page_indicators.find("label", {"id": "lblValor1_1"}).text \
			.replace(".", "") \
			.replace(",", ".")
		return {"date": date.strftime("%Y%m%d"), "value": value}

	#######################################################################
	##  Scrape the page searched for the all known values of the UF     ##
	##  INPUT:                                                           ##
	##  OUTPUT: List historical of values in central bank web page       ##
	#######################################################################
	def get_all_uf(self):
		session = dryscrape.Session()
		self.logger.info("SEARCH ALL UFs VALUES CENTRAL BANK")
		list_money = []
		self.logger.info("Connecting to Central Bank....")
		session.visit(settings.URL_CENTRAL_BANK + "/" + self.link)
		response = session.body()
		years = self.obtain_years(response)
		for i in range(1, len(years)+1):
			self.logger.info("Visiting  year {0}.....".format(years[i-1]))
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
						month= str(col+1)
						if len(month)==1:
							month = "0" + month
						if len(day)==1:
							day = "0" + day
						date = datetime.strptime("{0}{1}{2}".format(years[i-1], month, day), "%Y%m%d").date()
						data = {"date": date.strftime("%Y%m%d"), "value": float(value.replace(".", "").replace(",", "."))}
						self.logger.info("Getting date {0} and the value: {1} [UF".format(data["date"], data["value"]))
						list_money.append(data)
		return list_money

	#######################################################################
	##  scrape the page searched for the last known values of the UF that##
	#   are not in the database                                          ##
	##  INPUT: last date of money saving in database                     ##
	##  OUTPUT: List value to update database                            ##
	#######################################################################
	def get_last_uf(self, last_date):
		session = dryscrape.Session()
		self.logger.info("SEARCH LAST UFs VALUES CENTRAL BANK")
		list_money = []
		self.logger.info("Connecting to Central Bank....")
		session.visit(settings.URL_CENTRAL_BANK + "/" + self.link)
		self.logger.info("Visiting the page {0}".format(settings.URL_CENTRAL_BANK + "/" + self.link))
		years = self.obtain_years( session.body())
		range_list_years = range(years.index(str(last_date.year)), len(years))
		for i in range_list_years:
			year = years[i]
			self.logger.info("Visiting  year {0}.....".format(year))
			if len(range_list_years) !=1:
				drFechas = session.at_xpath('//*[@id="DrDwnFechas"]/option[' + str(i+1) + ']')
				# print '//*[@id="DrDwnFechas"]/option[' + str(i+1) + ']'
				drFechas.select_option()
			soup = BeautifulSoup(session.body())
			# print soup
			serie_grid = soup.find('table','Grid').find("tbody").findAll("tr")
			serie_grid.pop(0)
			for row in range(len(serie_grid)):
				element_grid = serie_grid[row]
				list_col = element_grid.findAll("td")
				day = list_col.pop(0).text
				for col in range(0, len(list_col)):

					value = list_col[col].find("span").text
					if len(value) > 0:
						month= str(col+1)
						if len(month)==1:
							month = "0" + month
						if len(day)==1:
							day = "0" + day
						date = datetime.strptime("{0}{1}{2}".format(year, month, day), "%Y%m%d").date()
						if date > last_date:
							data= {"date":date.strftime("%Y%m%d"), "value": float(value.replace(".", "").replace(",", "."))}
							self.logger.info("Getting date {0} and the value: {1} [UF]".format(data["date"], data["value"]))
							list_money.append(data)
		return list_money

