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
router.register("api/follow", FollowViewSet)
router.register("api/ingredients", IngredientViewSet)
router.register("api/tags", TagViewSet)


app_name = "api"

urlpatterns = [path("", include(router.urls))]
