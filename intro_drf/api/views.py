from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import Institutions, Metadata, Reports
from .serializers import InstitutionsSerializer, MetadataSerializer, ReportsSerializer, SubsectorTotalCompaniesSerializer
from django.core.cache import cache
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

class InstitutionsView(ListAPIView):
    queryset = Institutions.objects.all()
    serializer_class = InstitutionsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        institution_name = self.request.query_params.get('name', None)
        if institution_name:
            queryset = queryset.filter(
                Q(top_sellers__contains=[{'name': institution_name}]) | Q(top_buyers__contains=[{'name': institution_name}]))
        return queryset
    
    def list(self, request):
        cache_key = f"institution-trade: {request.GET.get('name')}" # Define a unique cache key for this data
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
    
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            #print(result.values())  # Log the retrieved data (for debugging purposes)
        
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
        
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
    
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        #print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response

class MetadataView(ListAPIView):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        queryset = super().get_queryset()
        sector = self.request.query_params.get('sector', None)
        sub_sector = self.request.query_params.get('sub_sector', None)
        if sector and sub_sector:
            queryset = queryset.filter(
                Q(sector__contains=sector) & Q(sub_sector__contains=sub_sector))
        elif sector:
            queryset = queryset.filter(
                sector__contains=sector
            )
        elif sub_sector:
            queryset = queryset.filter(
                sub_sector__contains=sub_sector
            )
        return queryset
    
    def list(self, request):
        # Define a unique cache key for this data
        sector = self.request.query_params.get('sector', None)
        sub_sector = self.request.query_params.get('sub_sector', None)
        if sector and sub_sector:
            cache_key = f"metadata: {request.GET.get('sector')+'-'+request.GET.get('sub_sector')}"
        elif sector:
            cache_key = f"metadata: {request.GET.get('sector')}"
        elif sub_sector:
            cache_key = f"metadata: {request.GET.get('sub_sector')}"
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
    
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            #print(result.values())  # Log the retrieved data (for debugging purposes)
        
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
        
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
    
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        #print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response
    
class ReportsView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = ReportsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        sub_sector = self.request.query_params.get('sub_sector', None)
        if sub_sector:
            queryset = queryset.filter(
                sub_sector__contains=sub_sector)
        return queryset
    
    def list(self, request):
        cache_key = f"sub-sector-performances: {request.GET.get('sub_sector')}" # Define a unique cache key for this data
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            #print(result.values())  # Log the retrieved data (for debugging purposes)
        
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
        
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
    
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        #print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response
    
class SubSectorTotalCompaniesView(ListAPIView):
    queryset = Reports.objects.all()
    serializer_class = SubsectorTotalCompaniesSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        sub_sector = self.request.query_params.get('sub_sector', None)
        if sub_sector:
            queryset = queryset.filter(
               sub_sector__contains=sub_sector)
        return queryset
    
    def list(self, request):
        cache_key = f"sub-sector-total-companies: {request.GET.get('sub_sector')}" # Define a unique cache key for this data
        result = cache.get(cache_key)  # Attempt to retrieve cached data using the cache key
        
        if not result:  # If no cache is found
            print('Hitting DB')  # Log to indicate a database query is being made
            result = self.get_queryset()  # Query the database for the data
            #print(result.values())  # Log the retrieved data (for debugging purposes)
        
            # Optional: Adjust the data before caching (e.g., filtering or transforming)
            # result = result.values_list('symbol')
        
            cache.set(cache_key, result, 60)  # Cache the result for 60 seconds
        else:
            print('Cache retrieved!')  # Log to indicate that cached data was retrieved
    
        # Serialize the result to prepare it for the response
        result = self.serializer_class(result, many=True)
        #print(result.data)  # Log the serialized data (for debugging purposes)

        return Response(result.data)  # Return the serialized data as a response