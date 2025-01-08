from django.shortcuts import render
from rest_framework.views import APIView


class HomeView(APIView):
    def get(self, request):
        return render(request, 'home.html')
    

class AhpView(APIView):
    def get(self, request):
        return render(request, 'views/ahp.html')
    
    
class FuzzyTopsisView(APIView):
    def get(self, request):
        return render(request, 'views/fuzzy-topsis.html')
    

class TopsisView(APIView):
    def get(self, request):
        return render(request, 'views/topsis.html')
    

class WaspasView(APIView):
    def get(self, request):
        return render(request, 'views/waspas.html')