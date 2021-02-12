from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from django.http import QueryDict
from rest_framework import viewsets
import time
import datetime
from django.db.models import Avg, Max, Min
import json
import os
from django.conf import settings

class SensorDataAPI(APIView):

    def get(self, request, pk):
        """
          To get the particular user review
          URL Structure: api/users/user-reviews/<id>/
        """
        sensor_obj = get_object_or_404(SensorData, id=pk)
        serializer = SensorDataSerializer(sensor_obj)
        return Response(serializer.data, 200)

    def post(self, request, pk):
        """
          To create the user review
          URL Structure: api/users/user-reviews/
          Required Fields : {"reading":"20", "sensor_type":"temperature", "reading_date":"2020-09-09"}
        """
        json_data = open(settings.BASE_DIR+'/sensorapp/sensor_data.json').read()
        jsonData = json.loads(json_data)
        sdata = jsonData["sensor_data"]
        respose_data = []
        for data in sdata:
            data["reading_timestamp"] = time.mktime(datetime.datetime.strptime(data["reading_date"], "%Y-%m-%d").timetuple())
            serializer = SensorDataSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                respose_data.append(serializer.data)
        return Response(respose_data, 201)



    def put(self, request, pk):
        """
          To edit the user review
          URL Structure: api/users/user-reviews/<id>/
        """
        sensor_obj = get_object_or_404(SensorData, id=pk)
        serializer = SensorDataSerializer(sensor_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 200)
        return Response(serializer.errors, 400)

    def delete(self, request, pk):
        """
          To delete the user review
          URL Structure: api/users/user-reviews/<id>/
        """
        sensor_obj = get_object_or_404(SensorData, id=pk)
        sensor_obj.delete()
        return Response({'message': 'Deleted Successfully', "status":200})


class ListingAPIs(viewsets.ModelViewSet):

    def sensor_data_list(self,request):
        """
          To list sensor data list
          URL Structure: sensor-data-list/
          Method: GET
        """
        sensor_obj = SensorData.objects.all()
        serializer = SensorDataSerializer(sensor_obj, many=True)
        return Response(serializer.data, 200)

    def filter_sensor_data(self,request):
        """
          To filter sensor data list
          URL Structure: sensor-data-list/
          Method: POST
          Required Fields : {"start_date":"2020-09-14", "end_date":"2020-09-14", "value":"min"}
        """

        data = QueryDict.dict(request.data)
        if data["value"]=="min":
            sensor_obj = SensorData.objects.filter( reading_date__gte = data["start_date"],
                                                reading_date__lte = data["end_date"])
            data_value = sensor_obj.aggregate(Min('reading'))
            data_value = data_value["reading__min"]
        elif data["value"]=="max":
            sensor_obj = SensorData.objects.filter(reading_date__gte=data["start_date"],
                                                   reading_date__lte=data["end_date"])
            data_value = sensor_obj.aggregate(Max('reading'))
            data_value = data_value["reading__max"]
        elif data["value"]=="average":
            sensor_obj = SensorData.objects.filter(reading_date__gte=data["start_date"],
                                                   reading_date__lte=data["end_date"])
            data_value = sensor_obj.aggregate(Avg('reading'))
            data_value = data_value["reading__avg"]
        serializer = SensorDataSerializer(sensor_obj, many=True)
        context = {
            "value":data_value,
            "data_list":serializer.data
        }
        return Response(context, 200)



