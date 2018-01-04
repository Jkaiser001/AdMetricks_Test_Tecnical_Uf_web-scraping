# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from ConnectorCentralBank import ConnectorCentralBank

from datetime import datetime
from models import Money
from serializers import MoneySerializer
from uf_Scraping.util import update_last_uf_central_bank, get_all_uf_central_bank
import logging


logger = logging.getLogger("central_bank")

#######################################################################
##  View list values UF historical                                   ##
##  INPUT:                                                           ##
##  OUTPUT: List historical of values in central bank web page       ##
#######################################################################
@api_view(["GET"])
def list_uf_view(request):

	moneys = Money.objects.all().order_by("date")
	list_moneys_output=[]
	logger.info("_______LIST UF REQUEST_____")
	# Verify if not empty database table
	if len(moneys) == 0:
		logger.info("Get all money central bank page....")
		list_moneys_output = get_all_uf_central_bank()
	else:
		last_date = moneys.last().date
		today = datetime.today().date()
		# Check if values UF is update
		if last_date < today:
			logger.info("Updating money central bank...")
			# Scraping web page of central bank and search new values
			update_last_uf_central_bank(last_date)
			moneys = Money.objects.all().order_by("date")
			logger.info("Formatting response...")
			for money in moneys:
				serializer = MoneySerializer(money)
				date = datetime.strptime(serializer.data["date"], "%Y-%m-%d").strftime("%Y%m%d")
				data = {"date": date, "value": serializer.data["value"]}
				list_moneys_output.append(data)
		else:
			# Return all values of table
			logger.info("Formatting response...")
			for money in moneys:
				serializer = MoneySerializer(money)
				date = datetime.strptime(serializer.data["date"], "%Y-%m-%d").strftime("%Y%m%d")
				list_moneys_output.append({"date": date, "value": serializer.data["value"]})
	logger.info("RESPONSE....")
	return Response(list_moneys_output, status=status.HTTP_200_OK)

#######################################################################
## View price uf                                                    ##
## #INPUT: value and date in guery string                           ##
## #OUPUT: convert value in UF to CLP in date required              ##
#######################################################################
@api_view(["GET"])
def price_uf_view(request):
	# Validate query string values
	if ("value" not in request.GET) or ("date" not in request.GET):
		return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)

	try:
		value = float(request.GET["value"])
	except ValueError:
		return Response({"error": "Invalid value: {0}".format(request.GET["value"])}, status=status.HTTP_400_BAD_REQUEST)

	date_request = datetime.strptime(request.GET["date"], "%Y%m%d")
	# Verify if not empty database table
	moneys = Money.objects.all().order_by("date")
	if len(moneys) > 0:
		last_date = moneys.last().date
		# Check if date_request is before the last date of the saved UF value
		if last_date > date_request.date():
			try:
				# Get value Money to database
				money = Money.objects.get(date=date_request)
				serializer = MoneySerializer(money)
				value_uf_day = serializer.data["value"]

			except Money.DoesNotExist:
				# Scraping web page of central bank and search value in the date_request
				connector = ConnectorCentralBank()
				data_money = connector.get_uf_date(date_request)
				serializer = MoneySerializer(data=data_money)
				if serializer.is_valid():
					serializer.save()
				else:
					return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

				value_uf_day = serializer.data["value"]
		else:
			# If value data request is after last date, updating the database with values in central bank web page
			update_last_uf_central_bank(last_date)
			try:
				money = Money.objects.get(date=date_request)
				serializer = MoneySerializer(money)
				value_uf_day = serializer.data["value"]
			except Money.DoesNotExist:
				return Response({"error": "there is no UF value for the date {0}".format(date_request.strftime("%Y%m%d"))}, status=status.HTTP_400_BAD_REQUEST)

	else:
		# Charger all data to database, scraping de central bank web page
		get_all_uf_central_bank()
		try:
			money = Money.objects.get(date=date_request)
			serializer = MoneySerializer(money)
			value_uf_day = serializer.data["value"]
		except Money.DoesNotExist:

			return Response({"error": "there is no UF value for the date {0}".format(date_request.strftime("%Y%m%d"))}, status=status.HTTP_400_BAD_REQUEST)
	logger.info("Calculating the result of converting the value from UF to CLP: {0}[UF]".format(value))
	logger.info("The value UF is {0}[CLP] in date {1}".format(value_uf_day, date_request.strftime("%Y%m%d")))
	result = round(float(value_uf_day) * value,2)
	logger.info("Result: {0}[CLP]".format(result) )
	data = {"date": date_request.strftime("%Y%m%d"), "result": result}

	return Response(data, status=status.HTTP_200_OK)
