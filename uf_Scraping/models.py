# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import date
# Create your models here.

9
class Money( models.Model ):

	value = models.IntegerField(null=False)
	date = models.DateField(default=timezone.now())
