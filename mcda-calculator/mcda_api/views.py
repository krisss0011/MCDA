import json
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from .services import *
from .db_utils import *
from django.http import JsonResponse
from rest_framework import status


class CompaniesVieSet(viewsets.ModelViewSet):
    queryset = Companies.objects.all()
    serializer_class = CompaniesSerializer


class DefaultCriteriaViewSet(viewsets.ModelViewSet):
    queryset = DefaultCriteria.objects.all()
    serializer_class = DefaultCriteriaSerializer


class MCDAView(APIView):
    """
    API view to calculate the MCDA and save the results
    """
    def get(self, request):
        """
        Calculate the MCDA using the specified method and weights
        """
        method = request.query_params.get('method', 'all')
        weights_param = request.query_params.get('weights')

        criteria_data = fetch_default_criteria()
        if not criteria_data:
            return Response({"error": "Failed to fetch criteria, cannot proceed with MCDA calculation."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        default_weights = [criterion['default_weight'] for criterion in criteria_data]
        
        try:
            custom_weights = list(map(float, weights_param.split(','))) if weights_param else default_weights
        except ValueError:
            return Response({"error": "Invalid weights format"}, status=status.HTTP_400_BAD_REQUEST)

        companies_data = fetch_company_data()
        criterion_type = [{'field': crit['field'], 'type': crit['type']} for crit in criteria_data]

        results_to_save = []
        result_response = {} 

        methods_to_process = ['ahp', 'topsis', 'fuzzy_topsis', 'waspas'] if method == 'all' else [method]
        for meth in methods_to_process:
            result = calculate_mcdm(meth, custom_weights, companies_data, criterion_type if meth != 'ahp' else None)
            results_to_save.append((meth, result))
            result_response[meth] = result 
            self.save_result(meth, custom_weights, result, criterion_type if meth != 'ahp' else None)

        for meth, res in results_to_save:
            self.save_to_cached_results(meth, custom_weights, res, criterion_type)

        if method == 'all':
            return Response(result_response)
        elif method in result_response:
            return Response({method: result_response[method]})
        else:
            return Response({"error": f"Method {method} is not processed or invalid."}, status=status.HTTP_400_BAD_REQUEST)


    def save_result(self, method, weights, result, criterion_type=None):
        """
        Save the result of the MCDA calculation to the database
        """
        model = {
            'ahp': AhpResult,
            'topsis': TopsisResult,
            'fuzzy_topsis': FuzzyTopsisResult,
            'waspas': WaspasResult
        }.get(method, None)
        
        if model:
            truncate_table(model)
            # model.objects.all().delete()

            if model == AhpResult:
                weights_json = ','.join(map(str, weights))
                model.objects.create(
                    criteria_weights=weights_json,
                    ranked_companies=result
                )

            if model == TopsisResult:
                weights_json = ','.join(map(str, weights))
                model.objects.create(
                    criteria_weights=weights_json,
                    ranked_companies=result
                )

            if model == FuzzyTopsisResult:
                weights_json = ','.join(map(str, weights))
                model.objects.create(
                    criteria_weights=weights_json,
                    ranked_companies=result
                )

            if model == WaspasResult:
                weights_json = ','.join(map(str, weights))
                model.objects.create(
                    criteria_weights=weights_json,
                    ranked_companies=result
                )

        self.save_to_cached_results(method, weights, result, criterion_type)


    def save_to_cached_results(self, method, weights, result, criterion_type=None):
        """
        Save the result of the MCDA calculation to the CachedResults table
        """
        criteria_weights_str = ','.join(map(str, weights))
        criteria_types_str = ','.join([f"{ct['field']}:{ct['type']}" for ct in criterion_type]) if criterion_type else ""

        # Leave this for now as it is ... rapid growing of id's because of the double insert / tried with truncate_table but it didn't work (only one method was saved in the db)
        CachedResults.objects.filter(method=method).delete()
        # reset_auto_increment(CachedResults)
        # truncate_table(CachedResults) 

        CachedResults.objects.create(
            method=method,
            criteria_weights=criteria_weights_str + (f", types: {criteria_types_str}" if criteria_types_str else ""),
            result_data=result
        )

    # ONLY AHP IS WORKING FOR POST REQUESTS
    # def post(self, request):
    #     method = request.query_params.get('method')
    #     weights_string = request.data.get('weights')

    #     if not method:
    #         return Response({"error": "Method parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
    #     if method not in ['all', 'ahp', 'topsis', 'fuzzy_topsis', 'waspas']:
    #         return Response({"error": "Unsupported MCDM method"}, status=status.HTTP_400_BAD_REQUEST)

    #     if not weights_string:
    #         return Response({"error": "Weights parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         weights = list(map(float, weights_string.split(',')))
    #     except ValueError:
    #         return Response({"error": "Invalid weights format"}, status=status.HTTP_400_BAD_REQUEST)

    #     companies_data = fetch_company_data()
    #     if companies_data is None:
    #         return Response({"error": "Failed to fetch company data"}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         result = calculate_mcdm(method, weights, companies_data)
    #         if result is None:
    #             return Response({"error": "Error in calculating MCDM, result was None"}, status=status.HTTP_400_BAD_REQUEST)
    #         return Response(result)
    #     except ValueError as e:
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CachedResultsViewSet(viewsets.ModelViewSet):
    """
    Cached results viewset, used to fetch the cached results from the database
    """
    queryset = CachedResults.objects.all()
    serializer_class = CachedResultsSerializer


class AhpResultViewSet(viewsets.ModelViewSet):
    """
    AHP results viewset, used to fetch the AHP results from the database
    """
    queryset = AhpResult.objects.all()
    serializer_class = AhpResultSerializer


class TopsisResultViewSet(viewsets.ModelViewSet):
    """
    TOPSIS results viewset, used to fetch the TOPSIS results from the database
    """
    queryset = TopsisResult.objects.all()
    serializer_class = TopsisResultSerializer


class FuzzyTopsisResultViewSet(viewsets.ModelViewSet):
    """
    Fuzzy TOPSIS results viewset, used to fetch the Fuzzy TOPSIS results from the database
    """
    queryset = FuzzyTopsisResult.objects.all()
    serializer_class = FuzzyTopsisResultSerializer


class WaspasResultViewSet(viewsets.ModelViewSet):
    """
    WASPAS results viewset, used to fetch the WASPAS results from the database
    """
    queryset = WaspasResult.objects.all()
    serializer_class = WaspasResultSerializer