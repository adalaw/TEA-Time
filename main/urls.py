from django.urls import path

from . import views

urlpatterns = [
    # for all staff and customers
    path('', views.index, name='index'), # order page
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('checkout', views.checkout, name="checkout"),
    path('confirm', views.confirm, name="confirm"),

    # for staff only
    path('manage_products', views.manage_products, name="manage_products"),
    path('new_product', views.new_product, name="new_product"),
    path('edit_product/<str:pk>', views.edit_product, name="edit_product"),
    path('category', views.category, name="category"),
    path('edit_category/<str:pk>', views.edit_category, name="edit_category"),
    path('manage_orders', views.manage_orders, name="manage_orders"),
    path('report', views.report, name="report"),
    # js use
    path("cancel", views.cancel, name="cancel"),
    path("delivered", views.delivered, name="delivered"),
]