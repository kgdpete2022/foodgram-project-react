from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FollowViewSet,
    IngredientViewSet,
    RecipeIngredientsViewSet,
    RecipeViewSet,
    TagViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register("api/users", UserViewSet)
router.register("api/recipes", RecipeViewSet)
router.register("api/recipeingredients", RecipeIngredientsViewSet)
router.register("api/users", UserViewSet)
router.register("api/users", UserViewSet)
router.register("api/users", UserViewSet)


app_name = "api"

urlpatterns = [path("", include(router.urls))]
