# Django Built-in modules
from django import forms
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
# Local Apps
from .models import (
    Product,
    CategoryGeneralAttributes,
    AttributeValue,
    Brand,
    Category,
    ProductList,
    ProductListFilter,
)
# Third Party Packages
from django_filters import FilterSet
from django_filters.filters import ModelMultipleChoiceFilter, BooleanFilter, RangeFilter, CharFilter
from django_filters.widgets import RangeWidget


class CustomRangeWidget(RangeWidget):

    def __init__(self, from_attrs=None, to_attrs=None, attrs=None):
        super(CustomRangeWidget, self).__init__(attrs)
        if from_attrs:
            self.widgets[0].attrs.update(from_attrs)
        if to_attrs:
            self.widgets[1].attrs.update(to_attrs)


class CategoryMultipleChoiceFilter(ModelMultipleChoiceFilter):
    empty_value = '-'

    def filter(self, qs, value):
        if not value:
            return qs
        qs = qs.filter(category__in=value)
        return qs


class PriceFilter(RangeFilter):
    empty_value = '-'

    def filter(self, qs, value):
        if value:
            if value.start is not None and value.stop is not None:
                qs = qs.filter(in_stock=True, variant__price__range=[value.start, value.stop]).distinct()
            elif value.start is not None:
                qs = qs.filter(in_stock=True, variant__price__gte=value.start).distinct().order_by('-variant__price')
            elif value.stop is not None:
                qs = qs.filter(in_stock=True, variant__price__lte=value.stop).distinct()
        return qs


class InStockBooleanFilter(BooleanFilter):
    empty_value = '-'

    def filter(self, qs, value):
        if not value:
            return qs
        qs = qs.filter(in_stock=True)
        return qs


class SearchNameFilter(CharFilter):
    empty_value = '-'

    def filter(self, qs, value):
        if not value:
            return qs
        qs = qs.filter(name__contains=value)
        return qs


class BrandMultipleChoiceFilterFilter(ModelMultipleChoiceFilter):
    empty_value = '-'

    def filter(self, qs, value):
        if not value:
            return qs
        qs = qs.filter(brand__in=value)
        return qs


class CustomMultipleChoiceField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return str(obj.name)


class AttributeMultipleChoiceFilterFilter(ModelMultipleChoiceFilter):
    field_class = CustomMultipleChoiceField
    empty_value = '-'

    def filter(self, qs, value):
        if not value:
            return qs
        # Filter by product specification
        # qs = qs.filter(productspecification__attribute_value__in=value)

        # Filter by variant
        value_id = value.values_list('id', flat=True)
        qs = qs.filter(variant__attribute_values__in=value_id).distinct()
        return qs


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = ()

    @property
    def active_filters(self):
        if self.form.is_valid():
            return [key for key, value in self.form.cleaned_data.items() if value]
        return []

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None, category=None, brand=None):
        super().__init__(data, queryset, request=request, prefix=prefix)

        if category:
            # Category Filter
            children_of_category = category.get_children()
            if children_of_category:
                self.filters['category'] = CategoryMultipleChoiceFilter(
                    label=_('دسته بندی'),
                    widget=forms.CheckboxSelectMultiple,
                    queryset=children_of_category,
                )

            # Category Attribute
            category_general_attributes = CategoryGeneralAttributes.objects.filter(
                category=category,
                filterable=True,
            ).select_related('attribute', )

            for category_general_attribute in category_general_attributes:
                self.filters[f'attr_{category_general_attribute.attribute_id}'] = AttributeMultipleChoiceFilterFilter(
                    label=f'{category_general_attribute.attribute.name}',
                    widget=forms.CheckboxSelectMultiple,
                    queryset=AttributeValue.objects.filter(
                        attribute=category_general_attribute.attribute,
                        variant__product_id__in=queryset.values_list('id', flat=True)
                    ).order_by('name', ).distinct()
                )
        else:
            available_categories = Category.objects.filter(
                product__id__in=queryset.values_list('id', flat=True)).distinct()

            self.filters['category'] = CategoryMultipleChoiceFilter(
                label=_('دسته بندی'),
                widget=forms.CheckboxSelectMultiple,
                queryset=available_categories,
            )

        # Price Filter
        self.filters['price'] = PriceFilter(
            label=_('قیمت'),
            widget=CustomRangeWidget(
                from_attrs={'placeholder': _('از (تومان)')},
                to_attrs={'placeholder': _('تا (تومان)')},
            )
        )

        # InStock Filter
        self.filters['in_stock'] = InStockBooleanFilter(
            label=_('فقط کالا های موجود'),
            field_name='in_stock',
            widget=forms.CheckboxInput,
        )
        # Search Filter
        self.filters['name'] = SearchNameFilter(
            label=_('جستجو'),
            field_name='name',
            widget=forms.TextInput,
        )

        if brand is None:
            # Brand Filter
            available_brands = Brand.objects.filter(product__id__in=queryset.values_list('id', flat=True)).distinct()

            if available_brands:
                self.filters['brand'] = BrandMultipleChoiceFilterFilter(
                    label=_('برند'),
                    widget=forms.CheckboxSelectMultiple,
                    queryset=available_brands,
                )


class ProductListPageFilter(FilterSet):
    class Meta:
        model = Product
        fields = ()

    @property
    def active_filters(self):
        if self.form.is_valid():
            return [key for key, value in self.form.cleaned_data.items() if value]
        return []

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None, category=None, brand=None,
                 product_list_page=None):
        super().__init__(data, queryset, request=request, prefix=prefix)

        if category and product_list_page and product_list_page.show_category_filter:
            # Category Filter
            children_of_category = category.get_children()
            if children_of_category:
                self.filters['category'] = CategoryMultipleChoiceFilter(
                    label=_('دسته بندی'),
                    widget=forms.CheckboxSelectMultiple,
                    queryset=children_of_category,
                )

        if product_list_page:
            # Product List Page Attribute
            try:
                product_list = ProductList.objects.get(pk=product_list_page.pk)
                general_attributes = product_list.productlistfilter_set.filter(filterable=True)
                for general_attribute in general_attributes:
                    self.filters[f'attr_{general_attribute.attribute.id}'] = AttributeMultipleChoiceFilterFilter(
                        label=f'{general_attribute.attribute.name}',
                        widget=forms.CheckboxSelectMultiple,
                        queryset=general_attribute.attribute_values.all()
                    )
            except ProductList.DoesNotExist:
                pass

        # Price Filter
        self.filters['price'] = PriceFilter(
            label=_('قیمت'),
            widget=CustomRangeWidget(
                from_attrs={'placeholder': _('از (تومان)')},
                to_attrs={'placeholder': _('تا (تومان)')},
            )
        )

        # InStock Filter
        self.filters['in_stock'] = InStockBooleanFilter(
            label=_('فقط کالا های موجود'),
            field_name='in_stock',
            widget=forms.CheckboxInput,
        )
        # Search Filter
        self.filters['name'] = SearchNameFilter(
            label=_('جستجو'),
            field_name='name',
            widget=forms.TextInput,
        )

        if brand is None:
            # Brand Filter
            available_brands = Brand.objects.filter(product__id__in=queryset.values_list('id', flat=True)).distinct()

            if available_brands:
                self.filters['brand'] = BrandMultipleChoiceFilterFilter(
                    label=_('برند'),
                    widget=forms.CheckboxSelectMultiple,
                    queryset=available_brands,
                )
