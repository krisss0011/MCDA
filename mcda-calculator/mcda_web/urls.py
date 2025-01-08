from django.urls import path, include
from rest_framework import routers
from .views import *

class BaseRouterRootView(routers.APIRootView):
    def get_view_name(self) -> str:
        return "MCDA WEB"

class BaseRouter(routers.DefaultRouter):
    APIRootView = BaseRouterRootView

router = BaseRouter()

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('ahp/', AhpView.as_view(), name='ahp-view'),
    path('fuzzy-topsis/', FuzzyTopsisView.as_view(), name='fuzzytopsis-view'),
    path('topsis/', TopsisView.as_view(), name='topsis-view'),
    path('waspas/', WaspasView.as_view(), name='waspas-view'),
]