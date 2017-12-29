# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from scraping_BCentral import connector_central_bank
from django.shortcuts import render

from datetime import datetime
from models import Money
from serializers import MoneySerializer

@api_view(["GET"])
def list_uf_view(request):
	return Response({"status":"OK"},status = status.HTTP_200_OK)


@api_view(["GET"])
def price_uf_view(request):

	if ("value" not in request.GET) or ("date" not in request.GET):
		return Response({"status" : "error"}, status=status.HTTP_400_BAD_REQUEST)
	date_request= datetime.strptime(request.GET["date"], "%Y%m%d")
	print date_request.strftime("%Y/%m/%d")

	try:
		money = Money.objects.get(date=date_request)
		serializer = MoneySerializer(money)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except:
		connector = connector_central_bank()
		money = connector.get_uf_date(date_request)
		serializer=MoneySerializer(data=money)
		if serializer.is_valid():
			serializer.save()
		else:
			return Response(serializer.errors , status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		return Response(serializer.data, status=status.HTTP_200_OK)
