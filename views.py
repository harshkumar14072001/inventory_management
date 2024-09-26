from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework_simplejwt.authentication import JWTAuthentication

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated]  

    @method_decorator(cache_page(60 * 60), name='dispatch') 
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
