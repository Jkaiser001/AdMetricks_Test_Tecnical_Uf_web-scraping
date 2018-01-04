# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from ConnectorCentralBank import ConnectorCentralBank
from django.shortcuts import render

from datetime import datetime
from models import Money
from serializers import MoneySerializer


@api_view(["GET"])
def list_uf_view(request):
	moneys = Money.objects.all().order_by("date")
	list_moneys = []
	print moneys.last().date
	connection = ConnectorCentralBank()
	today = datetime.now()
	connection.get_uf_yearly(today.year)

	return Response(list_moneys, status=status.HTTP_200_OK)


@api_view(["GET"])
def price_uf_view(request):
	if ("value" not in request.GET) or ("date" not in request.GET):
		return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)
	value = float(request.GET["value"])
	date_request = datetime.strptime(request.GET["date"], "%Y%m%d")

	try:
		money = Money.objects.get(date=date_request)
		serializer = MoneySerializer(money)
		value_uf_day = serializer.data["value"]
	# return Response(serializer.data, status=status.HTTP_200_OK)

	except:
		connector = ConnectorCentralBank()
		data_money = connector.get_uf_date(date_request)
		serializer = MoneySerializer(data=data_money)
		if serializer.is_valid():
			serializer.save()
		else:
			return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		value_uf_day = serializer.data["value"]

	return Response({"date": date_request.strftime("%Y%m%d"), "result": float(value_uf_day) * value},
	                status=status.HTTP_200_OK)
