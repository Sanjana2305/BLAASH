from django.db import models

# Create your models here.
class Product(models.Model):
    id= models.IntegerField().primary_key=True;
    product_name=models.CharField(max_length=255);
    product_image=models.TextField();
    SKU=models.CharField(max_length=255);

class EngagementPost(models.Model):
    tenant_id=models.IntegerField();
    thumbnail_title=models.CharField(max_length=100,default="Default Title");
    views=models.IntegerField(default=0);
    created_on=models.DateTimeField(auto_now_add=True);

class Collection(models.Model):
    id=models.IntegerField.primary_key=True;
    posts=models.ManyToManyField(EngagementPost, related_name='collections');
    collection_name=models.CharField(max_length=255);
    created_at=models.DateTimeField(auto_now_add=True);

class EngagementPostContent(models.Model):
    post=models.ForeignKey(EngagementPost, related_name='contents', on_delete=models.CASCADE);
    url = models.CharField(max_length=200);

class EngagementPostProductMapping(models.Model):
    post=models.ForeignKey(EngagementPost,related_name='products', on_delete=models.CASCADE);
    product=models.ForeignKey(Product, on_delete=models.CASCADE);