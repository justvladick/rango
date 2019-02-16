# from channels.auth import AuthMiddlewareStack
from django.urls import path, include
from django.views.generic import TemplateView
from booktime import views
from django.views.generic.detail import DetailView
from booktime import models
from django.contrib.auth import views as auth_views
from booktime import forms
from rest_framework import routers
from booktime import endpoints, admin
from rest_framework.authtoken import views as authtoken_views

router = routers.DefaultRouter()
router.register(r'orderlines', endpoints.PaidOrderLineViewSet)
router.register(r'orders', endpoints.PaidOrderViewSet)

app_name = 'booktime'
urlpatterns = [
    path('', views.home, name="home", ),
    path('about-us/', TemplateView.as_view(template_name="about_us.html"),
         name="about_us", ),
    path("contact-us/", views.ContactUsView.as_view(), name="contact_us", ),
    path(
        "products/<slug:tag>/",
        views.ProductListView.as_view(),
        name="products",
    ),
    path(
        "product/<slug:slug>/",
        DetailView.as_view(model=models.Product),
        name="product",
    ),
    # path('signup/', views.SignupView.as_view(), name="signup"),
    # path('logout/', views.logout_me, name="logout"),
    # path(
    #     "login/",
    #     auth_views.LoginView.as_view(
    #         template_name="login.html",
    #         form_class=forms.AuthenticationForm,
    #     ),
    #     name="login",
    # ),
    path(
        "address/",
        views.AddressListView.as_view(), name="address_list",
    ),
    path(
        "address/create/",
        views.AddressCreateView.as_view(), name="address_create",
    ),
    path(
        "address/<int:pk>/",
        views.AddressUpdateView.as_view(), name="address_update",
    ),
    path(
        "address/<int:pk>/delete/",
        views.AddressDeleteView.as_view(), name="address_delete",
    ),
    path("add_to_basket/", views.add_to_basket, name="add_to_basket", ),

    path('basket/', views.manage_basket, name="basket"),

    path("order/done/",
         TemplateView.as_view(template_name="order_done.html"),
         name="checkout_done",
         ),
    path("order/address_select/",
         views.AddressSelectionView.as_view(),
         name="address_select",
         ),
    path("order-dashboard/", views.OrderView.as_view(),
         name="order_dashboard",
         ),

    path('api/', include(router.urls)),
    # path("mobile-api/auth/", authtoken_views.obtain_auth_token, name="mobile_token", ),
    # path("mobile-api/my-orders/", endpoints.my_orders, name="mobile_my_orders", ),
    # path("mobile-api/my-orders/<int:order_id>/tracker/",
    #      AuthMiddlewareStack(consumers.OrderTrackerConsumer), ),

    # path("admin/", admin.main_admin.urls),
    # path("office-admin/", admin.central_office_admin.urls),
    # path("dispatch-admin/", admin.dispatchers_admin.urls),
    #
    # path("customer-service/<int:order_id>/", views.room, name="cs_chat", ),
    # # path("customer-service/", TemplateView.as_view(
    # #     template_name="customer_service.html"), name="cs_main", ),
    # path("customer-service/", views.rooms, name="cs_main", ),

]
