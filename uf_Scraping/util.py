from datetime import datetime

from uf_Scraping.ConnectorCentralBank import ConnectorCentralBank
from uf_Scraping.serializers import MoneySerializer
import logging

logger = logging.getLogger("central_bank")
#######################################################################
##  Get new values known and save in database                        ##
##  INPUT: value of last value know in the database                  ##
##  OUTPUT:                                                          ##
#######################################################################
def update_last_uf_central_bank(last_date):
	connection = ConnectorCentralBank()
	list_moneys = connection.get_last_uf(last_date)
	for money_for_add in list_moneys:
		logger.info("Saving money: {0}".format(money_for_add))
		serializer = MoneySerializer(data=money_for_add)
		if serializer.is_valid():
			serializer.save()
		else:
			logger.error("Error to saving money: {0}".format(serializer.errors))
			pass

#######################################################################
##  Get all kwown in the webpage and save in database                ##
##  INPUT:                                                           ##
##  OUTPUT: List historical of values in database                    ##
#######################################################################
def get_all_uf_central_bank():
	connection = ConnectorCentralBank()
	list_moneys=[]
	list_moneys_central_bank = connection.get_all_uf()
	for money in list_moneys_central_bank:
		serializer = MoneySerializer(data=money)
		logger.info("Saving money: {0}".format(money))
		if serializer.is_valid():
			serializer.save()
			logger.info("Formatting money {0}".format(serializer.data))
			date = datetime.strptime(serializer.data["date"], "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d")
			list_moneys.append({"date": date, "value": serializer.data["value"]})
		else:
			logger.error("Error to saving money: {0}".format(serializer.errors))
			pass
	return list_moneys
