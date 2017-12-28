# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date
# Create your models here.


class Money( models.Model ):

	value = models.integerField(null=False, max_length=10)
	date = models.DateField(default=date.today())
