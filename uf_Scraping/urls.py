from django.conf.urls import url
from views import price_uf_view, list_uf_view

urlpatterns = [
	url(r'^price/$', price_uf_view, name='price_uf'),
	url(r'^list/$', list_uf_view, name='list_uf'),
]
