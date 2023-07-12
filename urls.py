from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('productos',ProductoViewset)

urlpatterns = [
    # API
    path('api/', include(router.urls)),




    path('', index, name = "index"),
    path('indexapi/', indexapi, name = "indexapi"),
    path('blog/', blog, name = "blog"),
    path('blogapi/', blogapi, name = "blogapi"),
    path('cart/', cart, name = "cart"),
    path('cartUser/', cartUser, name = "cartUser"),
    path('category/', category, name = "category"),
    path('checkout/', checkout, name = "checkout"),
    path('confirmation/', confirmation, name = "confirmation"),
    path('contact/', contact,name = "contact"),
    path('historial_compras/', historial_compras,name = "historial_compras"),
    path('indexUser/', indexUser,name = "indexUser"),
    path('indexUserSubscito/', indexUserSubscito, name = "indexUserSubscito"),
    path('login/', login,name = "login"),
    path('perfil/', perfil,name = "perfil"),
    path('register/', register,name = "register"),
    path('registro/', registro,name = "registro"),
    path('singleblog/', singleblog, name="singleblog"),
    path('singleproduct/', singleproduct,name = "singleproduct"),
    path('subsForm/', subsForm,name = "subsForm"),
    path('trackingorder/', trackingorder,name = "tracking-order"),


    #CRUD
    path('add/', add,name = "add"),
    path('update/<id>/', update,name = "update"),
    path('delete/<id>/', delete, name= "delete"),
    path('cartadd/<id>/', cartadd, name="cartadd"),
    path('cart/cartdel/<id>/', cartdel, name="cartdel"),
    path('cart/cartadd/<id>',cartadd, name="cartaddd"),
    path('cart/cartdelete/<id>',cartdelete, name="cartdelete"),
    path('add_compra/', add_compra, name="add_compra"),
    


    
]

