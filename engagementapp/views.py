from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product,EngagementPost,Collection,EngagementPostContent,EngagementPostProductMapping
from .serializer import ProductSerializer,CollectionSerializer,TopViewedPostSerializer,EngagementPostSerializer,EngagementPostContentSerializer

# Create your views here.
@api_view(['POST'])
def createNewProduct(request):
    serializer = ProductSerializer(data=request.data);
    if serializer.is_valid():
        serializer.save();
        return Response(status=status.HTTP_201_CREATED);
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST);

@api_view(['POST'])
def createNewCollection(request,*args,**kwargs):
    serializer = CollectionSerializer(data=request.data);
    if serializer.is_valid():
        serializer.save();
        return Response(status=status.HTTP_201_CREATED);
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST);

@api_view(['GET'])
def topViewedPost(request):
    tenant_id=request.query_params.get('tenant_id');
    if not tenant_id:
        return Response(status=status.HTTP_400_BAD_REQUEST);
    posts = EngagementPost.objects.filter(tenant_id=tenant_id).order_by('-views')[:5];
    serializer = TopViewedPostSerializer(posts, many=True);
    return Response(serializer.data, status=status.HTTP_200_OK);

@api_view(['GET'])
def postWithContentAndProduct(request):
    tenant_id=request.query_params.get('tenant_id');
    if not tenant_id:
        return Response(status=status.HTTP_400_BAD_REQUEST);
    posts=EngagementPost.objects.filter(tenant_id=tenant_id).prefetch_related('contents', 'products__product');
    serializer=EngagementPostSerializer(posts, many=True);
    return Response(serializer.data, status=status.HTTP_200_OK);