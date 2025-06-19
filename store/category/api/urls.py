from django.urls import path
from store.category.api.views import CategoryModelViewSet, SubCategoryModelViewSet, SubSubCategoryModelViewSet, CategoryListView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register(r'category', CategoryModelViewSet)
router.register(r'sub-category', SubCategoryModelViewSet)
router.register(r'sub-sub-category', SubSubCategoryModelViewSet)


urlpatterns = router.urls
urlpatterns += [
    path('category-list/', CategoryListView.as_view())
]
