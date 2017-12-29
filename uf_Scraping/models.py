# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import date
# Create your models here.

class Money( models.Model ):

	value = models.DecimalField(null=False,decimal_places=2,max_digits=12)
	date = models.DateField(default=timezone.now())
