# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from django.shortcuts import render

@api_view(["GET"])
def list_uf_view(request):

	return Response({"status":"OK"},status = status.HTTP_200_OK)


@api_view(["GET"])
def price_uf_view(request):

	if ("value" not in request.GET) or ("date" not in request.GET):
		return Response({"status" : "error"}, status=status.HTTP_400_BAD_REQUEST)

	return Response({"status": "OK"}, status=status.HTTP_200_OK)
