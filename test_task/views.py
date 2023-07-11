from drf_yasg import openapi
from rest_framework.views import APIView
from .serializers import provider_serializer, service_area_serializer, polygons_point_check_result_serializer, \
    polygons_point_check_input_serializer
from rest_framework.response import Response
from rest_framework import status
from .models import Provider, ServiceArea
from drf_yasg.utils import swagger_auto_schema
from django.contrib.gis.geos import Point


# Create your views here.

class add_provider(APIView):
    """
    Add a new Provider. \n
    Languages are taken from django.conf.global_settings.LANGUAGES. Not comprehensive but will do for now \n
    Currencies are taken from pycountry.currrencies \n
    """

    @swagger_auto_schema(request_body=provider_serializer)
    def post(self, request):
        s = provider_serializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class update_provider(APIView):
    """
    Update provider field. \n
    Languages are taken from django.conf.global_settings.LANGUAGES. Not comprehensive but will do for now \n
    Currencies are taken from pycountry.currrencies \n
    """

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, ),
            'email': openapi.Schema(type=openapi.TYPE_STRING, ),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, ),
            'language': openapi.Schema(type=openapi.TYPE_STRING, ),
            'currency': openapi.Schema(type=openapi.TYPE_STRING, ),
        },
    ),
        responses={'200': provider_serializer, '404': 'HTTP_404_NOT_FOUND', '400': 'HTTP_400_BAD_REQUEST'}
    )
    def put(self, request, pk):
        try:
            provider = Provider.objects.get(pk=pk)
        except Provider.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        s = provider_serializer(provider, data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_200_OK)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class get_provider(APIView):
    @swagger_auto_schema(responses={'200': provider_serializer, '404': 'HTTP_404_NOT_FOUND'},
                         operation_id='Get provider information')
    def get(self, request, pk):
        try:
            provider = Provider.objects.get(pk=pk)
        except Provider.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        s = provider_serializer(provider)
        return Response(s.data, status=status.HTTP_200_OK)


class delete_provider(APIView):
    @swagger_auto_schema(operation_id='Delete provider')
    def delete(self, request, pk):
        try:
            provider = Provider.objects.get(pk=pk)
        except Provider.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        provider.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class add_service_area(APIView):
    @swagger_auto_schema(request_body=service_area_serializer, operation_id='add new service area')
    def post(self, request):
        s = service_area_serializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class update_service_area(APIView):
    @swagger_auto_schema(operation_id='Update service area',
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'name': openapi.Schema(type=openapi.TYPE_STRING),
                                 'price': openapi.Schema(type=openapi.TYPE_STRING),
                                 'provider': openapi.Schema(type=openapi.TYPE_INTEGER),
                                 'currency': openapi.Schema(type=openapi.TYPE_OBJECT,
                                                            description='dont know how to put a PolygonField as a type'
                                                            ),
                             },
                         ),
                         responses={'200': service_area_serializer, '404': 'HTTP_404_NOT_FOUND',
                                    '400': 'HTTP_400_BAD_REQUEST'}
                         )
    def put(self, request, pk):
        try:
            sa = ServiceArea.objects.get(pk=pk)
        except ServiceArea.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        s = service_area_serializer(sa, data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_200_OK)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class get_service_area(APIView):
    @swagger_auto_schema(responses={'200': service_area_serializer, '404': 'HTTP_404_NOT_FOUND'},
                         operation_id='Get service area information')
    def get(self, request, pk):
        try:
            sa = ServiceArea.objects.get(pk=pk)
        except ServiceArea.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        s = service_area_serializer(sa)
        return Response(s.data, status=status.HTTP_200_OK)


class delete_service_area(APIView):
    @swagger_auto_schema(operation_id='Delete service area')
    def delete(self, request, pk):
        try:
            sa = ServiceArea.objects.get(pk=pk)
        except ServiceArea.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        sa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class polygons_with_point(APIView):
    """
    Returnsa list of polygons containing a point with a given long and lat
    """

    @swagger_auto_schema(request_body=polygons_point_check_input_serializer,
                         responses={'200': polygons_point_check_result_serializer(many=True), '400': 'HTTP_400_BAD_REQUEST'},
                         operation_id='Polygons by point search')
    def post(self, request):
        s = polygons_point_check_input_serializer(data=request.data)
        if not s.is_valid():
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
        point = Point(request.data['long'], request.data['lat'])
        polygons = ServiceArea.objects.filter(polygon__contains=point).select_related('provider')
        s = polygons_point_check_result_serializer(polygons, many=True)
        return Response(s.data, status=status.HTTP_200_OK)
