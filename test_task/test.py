from rest_framework.test import APITestCase
from rest_framework import status
from .models import Provider, ServiceArea
from .serializers import service_area_serializer


class ProviderAPITest(APITestCase):
    def setUp(self):
        self.data = {"name": "test testov", "email": "test@test.com", "phone_number": "+77777777777", "language": "az",
                     "currency": "UZS"}
        self.bad_language = {"name": "test testov", "email": "test@test.com", "phone_number": "+77777777777",
                             "language": "zzzz",
                             "currency": "UZS"}
        self.bad_currency = {"name": "test testov", "email": "test@test.com", "phone_number": "+77777777777",
                             "language": "az",
                             "currency": "UZSsss"}
        pass

    def test_create_obj(self):
        response = self.client.post('/provider/add', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Provider.objects.count(), 1)
        Provider.objects.all().delete()

    def test_update_obj(self):
        obj = Provider.objects.create(**self.data)
        data = {'language': 'en'}
        response = self.client.put(f'/provider/{obj.pk}/update', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj.refresh_from_db()
        self.assertEqual(obj.language, 'en')

    def test_delete_obj(self):
        obj = Provider.objects.create(**self.data)
        response = self.client.delete(f'/provider/{obj.pk}/delete')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Provider.objects.count(), 0)

    def test_create_obj_with_bad_language(self):
        response = self.client.post('/provider/add', self.bad_language)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_obj_with_bad_currency(self):
        response = self.client.post('/provider/add', self.bad_currency)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_obj(self):
        obj = Provider.objects.create(**self.data)
        response = self.client.get(f'/provider/{obj.pk}/get')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.data)


class ServiceAreaAPITest(APITestCase):
    def setUp(self):
        provider_data = {"name": "test testov", "email": "test@test.com", "phone_number": "+77777777777",
                         "language": "az",
                         "currency": "UZS"}
        obj = Provider.objects.create(**provider_data)
        self.data = {"name": "test", "price": 1, "provider": obj.pk, "polygon": {
            "type": "Polygon",
            "coordinates": [
                [
                    [12.34, 56.78],
                    [23.45, 67.89],
                    [34.56, 78.90],
                    [45.67, 89.01],
                    [12.34, 56.78]
                ]
            ]
        }
                     }

    def test_create_obj(self):
        response = self.client.post('/service-area/add', self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ServiceArea.objects.count(), 1)
        ServiceArea.objects.all().delete()

    def test_delete_obj(self):
        # obj = ServiceArea.objects.create(**self.data)
        s = service_area_serializer(data=self.data)
        if s.is_valid():
            s.save()
        response = self.client.delete(f'/service-area/{s.instance.pk}/delete')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ServiceArea.objects.count(), 0)

    def test_retrieve_obj(self):
        # obj = ServiceArea.objects.create(**self.data)
        s = service_area_serializer(data=self.data)
        if s.is_valid():
            s.save()
        response = self.client.get(f'/service-area/{s.instance.pk}/get')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.data)

    def test_update_obj(self):
        s = service_area_serializer(data=self.data)
        if s.is_valid():
            s.save()
        data = {'name': 'test2'}
        response = self.client.put(f'/service-area/{s.instance.pk}/update', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        obj = ServiceArea.objects.get(pk=s.instance.pk)
        self.assertEqual(obj.name, 'test2')


class PolygonsWithPointAPITest(APITestCase):
    def setUp(self):
        provider_data = {"name": "test testov", "email": "test@test.com", "phone_number": "+77777777777",
                         "language": "az",
                         "currency": "UZS"}
        obj = Provider.objects.create(**provider_data)
        polygon_data = {"name": "test", "price": 1, "provider": obj.pk, "polygon": {
            "type": "Polygon",
            "coordinates": [
                [
                    [0, 0],
                    [0, 10],
                    [10, 10],
                    [10, 0],
                    [0, 0]
                ]
            ]
        }
                        }
        s = service_area_serializer(data=polygon_data)
        if s.is_valid():
            s.save()

    def test_search(self):
        d = {"long": 5, "lat": 5}
        response = self.client.post('/polygons-with-point', d, format="json")
        self.assertEqual(len(response.json()), 1)
        d = {"long": 11, "lat": 11}
        response = self.client.post('/polygons-with-point', d, format="json")
        self.assertEqual(len(response.json()), 0)
