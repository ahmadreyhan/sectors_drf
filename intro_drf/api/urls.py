from django.urls import path
from .views import InstitutionsView, MetadataView, ReportsView

urlpatterns = [
    path('get-institution-trade', InstitutionsView.as_view(), name='get-institution-trade'),
    path('get-metadata', MetadataView.as_view(), name='get-metadata'),
    path('get-sub-sector-performances', ReportsView.as_view(), name='get-sub-sector-performances'),
]
