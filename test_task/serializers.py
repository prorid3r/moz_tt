from .models import Provider, ServiceArea
from rest_framework import serializers
from django.conf.global_settings import LANGUAGES
from pycountry import currencies as CURRENCIES


class provider_serializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['name', 'email', 'phone_number', 'language', 'currency','id']

    def validate(self, data):
        """
        Check that the language code is valid
        """
        if "language" in data and data['language'] not in [code[0] for code in LANGUAGES]:
            raise serializers.ValidationError("Unknown language code")
        if "currency" in data and data['currency'] not in [code.alpha_3 for code in list(CURRENCIES)]:
            raise serializers.ValidationError("Unknown currency code")
        return data


class service_area_serializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = ['name', 'price', 'provider', 'polygon','id']

        # def create(self, validated_data):
        #    # Perform any necessary validations on validated_data


#
#    # Use bulk_create() to insert multiple records at once
#    return ServiceArea.objects.bulk_create(
#        [ServiceArea(**data) for data in validated_data],
#        batch_size=1000
#    )


class polygons_point_check_result_serializer(serializers.ModelSerializer):
    provider_name = serializers.SerializerMethodField()

    class Meta:
        model = ServiceArea
        fields = ['name', 'price', 'provider', 'id', 'provider_name']

    def get_provider_name(self, obj):
        return obj.provider.name


class polygons_point_check_input_serializer(serializers.Serializer):
    long = serializers.FloatField()
    lat = serializers.FloatField()
