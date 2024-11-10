from rest_framework import serializers

from products.models import Category, Gallery, Product, ProductComment, Variant


class ProductSerializers(serializers.ModelSerializer):
    
    image = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    default_variant = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = (
            'name',
            'image',
            'type',
            'in_stock',
            'url',
            'default_variant',
            'category',
        )
        
    def get_category(self, obj):
        return CategorySerializers(obj.category, many=True).data
        
    def get_image(self, obj):
        request = self.context.get('request')
        if image := obj.get_api_image:
            return request.build_absolute_uri(image)
        
    def  get_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())
    
    def get_default_variant(self, obj):
        request = self.context.get('request')
        return ProductVariantSerializers(obj.default_variant, context={'request': request}).data
    
    
    
class ProductVariantSerializers(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    discount_percent = serializers.SerializerMethodField()
    
    class Meta: 
        model = Variant
        fields = (
            'name',
            'reference_code',
            'sku',
            'price',
            'final_price',
            'discount_percent',
            'in_stock',
            'order_limit_max',
            'order_limit_min',
            'image',
        )
        
    def get_name(self, obj):
        return obj.variant_descriptor
        
    def get_final_price(self, obj):
        return obj.final_price
    
    def get_discount_percent(self, obj):
        return obj.discount_percent
    
    def get_image(self, obj):
        request = self.context.get('request')
        if image := obj.get_image :
            return request.build_absolute_uri(image)
        
        
        
        
class CategorySerializers(serializers.ModelSerializer):
    class Meta: 
            model = Category    
            fields = (
                'id',   
                'name' ,
            )
        
        
class CategoryListSerializers(serializers.ModelSerializer):
    
    image =serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'default_sorting',
            'image',
            'icon',
            'show_in_homepage',
            'consider_before_buying',
            'show_consider_before_buying_in_category_page',
            'children',
            
        )       
        
    def get_image(self, obj):
        request = self.context.get('request')
        if image := obj.get_api_image:
            return request.build_absolute_uri(image)
        
    def get_icon(self, obj):
        request = self.context.get('request')
        if image := obj.get_api_icon:
            return request.build_absolute_uri(image)
        
    def get_children(self, obj):
        # ایجاد یک لیست از دسته‌بندی‌های فرزند
        children = Category.objects.filter(parent=obj)
        if children:
            return CategoryListSerializers(children, many=True, context=self.context).data




class ProductDetailSerializers(serializers.ModelSerializer):
    
    category = serializers.SerializerMethodField()
    related_products = serializers.SerializerMethodField()
    structured_data = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    variants = serializers.SerializerMethodField()
    gallery = serializers.SerializerMethodField()
    # attributes = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Product
        fields = (
            'category',
            'name',
            'extra_detail',
            'image',
            'type',
            'attributes',
            'brand',
            'badge',
            'unit',
            'gallery',
            'variants',
            'inventory_management',
            'in_stock',
            'related_products',
            'related_items_display_status',
            'autofill_related_items',
            'consider_before_buying',
            'structured_data',
        )
        
    def get_category(self, obj):
        return CategorySerializers(obj.category, many=True).data
    
    def get_related_products(self, obj):
        return ProductSerializers(obj.get_related_products(), many=True, context=self.context).data
        
    def get_structured_data(self, obj):
        return obj.structured_data
    
    def get_image(self, obj):
        return obj.get_api_image
    
    def get_gallery(self, obj):
        return ProductGallerySerializers(obj.gallery.all(), many=True).data

    def get_variants(self, obj):
        return ProductVariantSerializers(obj.variant_set.all(), many=True).data


class ProductGallerySerializers(serializers.ModelSerializer):
    
    image = serializers.SerializerMethodField()
    alt = serializers.SerializerMethodField()
    
    class Meta:
        model = Gallery
        fields = (
            'image',
            'alt',
        )
        
    def get_image(self, obj):
        return obj.get_api_image
    
    def get_alt(self, obj):
        return obj.get_alt()
    
    
    
    
    

class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductComment
        fields = (
            'id',
            'parent',
            'user',
            'name',
            'email',
            'review',
            'status',
            'comment_type',
        )
        
    def to_representation(self, instance):
        # If you need custom representation
        representation = super().to_representation(instance)
        representation['is_admin_comment'] = instance.is_admin_comment
        return representation