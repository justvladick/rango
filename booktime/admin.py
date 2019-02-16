from django.contrib import admin
from django.utils.html import format_html
from . import models

import logging


logger = logging.getLogger(__name__)


def make_active(self, request, queryset):
    queryset.update(active=True)


make_active.short_description = "Mark selected items as active"


def make_inactive(self, request, queryset):
    queryset.update(active=False)


make_inactive.short_description = (
    "Mark selected items as inactive"
)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'in_stock', 'price')
    list_filter = ('active', 'in_stock', 'date_updated', 'tags')
    list_editable = ('in_stock',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ('tags',)
    actions = [make_active, make_inactive]

    # slug is an important field for our site, it is used in
    # all the product URLs. We want to limit the ability to
    # change this only to the owners of the company.
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return list(self.readonly_fields) + ["slug", "name"]

    # This is required for get_readonly_fields to work
    def get_prepopulated_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.prepopulated_fields
        else:
            return {}


class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('active',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

    # tag slugs also appear in urls, therefore it is a
    # property only owners can change
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return list(self.readonly_fields) + ["slug", "name"]

    def get_prepopulated_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.prepopulated_fields
        else:
            return {}


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_tag', 'product_name')
    list_filter = ('product',)
    readonly_fields = ('thumbnail',)
    search_fields = ('product__name',)

    # this function returns HTML for the first column defined
    # in the list_display property above
    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html('<img src="%s"/>' % obj.thumbnail.url)
        return "-"

    # this defines the column name for the list_display
    thumbnail_tag.short_description = "Thumbnail"

    def product_name(self, obj):
        return obj.product.name


class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "address1",
                    "address2", "city", "country",)
    readonly_fields = ("user",)


# instances of ModelAdmin that are nested inside
# other instances (via the inlines attribute).
class BasketLineInline(admin.TabularInline):
    model = models.BasketLine
    raw_id_fields = ("product",)


class BasketAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "count")
    list_editable = ("status",)
    list_filter = ("status",)
    inlines = (BasketLineInline,)


class OrderLineInline(admin.TabularInline):
    model = models.OrderLine
    raw_id_fields = ("product",)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", 'date_added')
    list_editable = ("status",)
    list_filter = ("status", "shipping_country", "date_added")
    inlines = (OrderLineInline,)
    fieldsets = (
        (None, {"fields": ("user", "status")}),
        (
            "Billing info",
            {
                "fields": (
                    "billing_name",
                    "billing_address1",
                    "billing_address2",
                    "billing_zip_code",
                    "billing_city",
                    "billing_country",
                )
            },
        ),
        (
            "Shipping info",
            {
                "fields": (
                    "shipping_name",
                    "shipping_address1",
                    "shipping_address2",
                    "shipping_zip_code",
                    "shipping_city",
                    "shipping_country",
                )
            },
        ),
    )


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductTag, ProductTagAdmin)
admin.site.register(models.ProductImage, ProductImageAdmin)
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.Basket, BasketAdmin)
admin.site.register(models.Order, OrderAdmin)
