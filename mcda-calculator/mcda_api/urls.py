
from django.urls import path, include
from rest_framework import routers
from .views import *

class BaseRouterRootView(routers.APIRootView):
    def get_view_name(self) -> str:
        return "Multiple Criteria Decision Analysis (MCDA) API"

class BaseRouter(routers.DefaultRouter):
    APIRootView = BaseRouterRootView

router = BaseRouter()
router.register(r'companies', CompaniesVieSet)
router.register(r'default-criteria', DefaultCriteriaViewSet)
router.register(r'cached-results', CachedResultsViewSet)
router.register(r'ahp-results', AhpResultViewSet)
router.register(r'topsis-results', TopsisResultViewSet)
router.register(r'fuzzy-topsis-results', FuzzyTopsisResultViewSet)
router.register(r'waspas-results', WaspasResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('calculation/', MCDAView.as_view(), name='mcda-calculation'),
]