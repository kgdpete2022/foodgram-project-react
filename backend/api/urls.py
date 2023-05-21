from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

app_name = "api"

router = DefaultRouter()
router.register(r"ingredients", IngredientViewSet)
router.register(r"recipes", RecipeViewSet)
router.register(r"tags", TagViewSet)
router.register(r"users", UserViewSet)


urlpatterns = [path("", include(router.urls))]
