from rest_framework import serializers
from models import Money
from datetime import datetime
class MoneySerializer(serializers.ModelSerializer):
	date = serializers.CharField()
	class Meta:
		model = Money
		fields = ["date","value"]
	def create(self, validated_data):
		date_str = validated_data.pop("date")
		date= datetime.strptime(date_str,"%Y/%m/%d")
		validated_data["date"] = date
		money = Money.objects.create(**validated_data)
		money.save()
		return money