from django.urls import include, path
from rest_framework import routers
from myapi import views
from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'register', views.UserViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'product', views.ProductViewSet)
router.register(r'shipping', views.ShippingViewSet)
router.register(r'saved', views.SavedViewSet)
router.register(r'cart', views.CartViewSet)
router.register(r'sale', views.SaleViewSet)
router.register(r'payment', views.PaymentViewSet)
router.register(r'messages', views.MessagesViewSet)
router.register(r'banks-account', views.BankAccountViewSet)
# router.register(r'banks-details', views.BankViewSet)
router.register(r'withdraw', views.WithdrawalViewSet)
router.register(r'installment', views.Installmental_SaleViewSet)
router.register(r'commission', views.CommissionViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('login/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='auth_logout'),
    path(r'list_bank', views.ListOfBankAPIView.as_view()),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]