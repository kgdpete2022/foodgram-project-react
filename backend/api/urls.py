from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet


router = DefaultRouter()
router.register("api/users", UserViewSet)


app_name = "api"

urlpatterns = [path("", include(router.urls))]
