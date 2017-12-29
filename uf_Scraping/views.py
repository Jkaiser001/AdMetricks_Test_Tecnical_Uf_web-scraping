# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from scraping_BCentral import connector_central_bank
from django.shortcuts import render

@api_view(["GET"])
def list_uf_view(request):
	return Response({"status":"OK"},status = status.HTTP_200_OK)


@api_view(["GET"])
def price_uf_view(request):

	if ("value" not in request.GET) or ("date" not in request.GET):
		return Response({"status" : "error"}, status=status.HTTP_400_BAD_REQUEST)
	connector = connector_central_bank()
	connector.get_uf_date
	return Response({"status": "OK"}, status=status.HTTP_200_OK)
