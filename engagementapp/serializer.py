from rest_framework import serializers
from .models import Product,EngagementPost,Collection,EngagementPostContent,EngagementPostProductMapping

class  ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product;
        fields = ['product_name', 'product_image','SKU'];

    def validate_sku(self,value):
        if Product.objects.filter(SKU=value).exists():
            raise serializers.ValidationError("This SKU already exists.");
        return value;

class CollectionSerializer(serializers.ModelSerializer):
    engagement_post_ids = serializers.ListField(child=serializers.IntegerField(),write_only=True);
    class Meta:
        model = Collection;
        fields = ['collection_name', 'engagement_post_ids'];

    def createCollection(self, validated_data):
        engagement_post_ids = validated_data.pop('engagement_post_ids',[]);
        collection = Collection.objects.create(**validated_data);
        for post_id in engagement_post_ids:
            post = EngagementPost.objects.get(id=post_id);
            collection.posts.add(post);
        return collection;

class TopViewedPostSerializer(serializers.ModelSerializer):
    content_url=serializers.CharField(source='engagement_post_content_set.first.url');

    class Meta:
        model=EngagementPost;
        fields=['thumbnail_title','content_url'];

class EngagementPostContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngagementPostContent;
        fields = ['url'];

class EngagementPostSerializer(serializers.ModelSerializer):
    contents=EngagementPostContentSerializer(many=True);
    products=ProductSerializer(many=True, source='products.product');

    class Meta:
        model = EngagementPost;
        fields= ['thumbnail_title', 'contents', 'products'];