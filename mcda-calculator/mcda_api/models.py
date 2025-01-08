from django.db import models

class Companies(models.Model):
    name = models.CharField(max_length=100)
    profit = models.FloatField()
    profit_change = models.FloatField()
    rank = models.IntegerField()
    rank_change = models.IntegerField(null=True)
    revenue = models.FloatField()
    revenue_change = models.FloatField()
    years_in_rank = models.IntegerField()
    assets = models.FloatField()
    employees = models.IntegerField()

    class Meta:
        db_table = "default_companies"
    
    def __str__(self):
            return self.name
    

class DefaultCriteria(models.Model):
    name = models.CharField(max_length=255, unique=True)
    field = models.CharField(max_length=255, unique=True)
    default_weight = models.FloatField()
    type = models.CharField(max_length=50, default='max')

    class Meta:
        db_table = "default_criteria"

    def __str__(self):
        return f"{self.name} - {self.default_weight} - {self.field}"
    

class CachedResults(models.Model):
    method = models.CharField(max_length=20)
    criteria_weights = models.TextField()
    result_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cached_results"

    def __str__(self):
        return f"{self.method} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class AhpResult(models.Model):
    criteria_weights = models.JSONField()
    ranked_companies = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ahp_method"

    def __str__(self):
        return f"{self.name}"
    

class TopsisResult(models.Model):
    criteria_weights = models.JSONField()
    ranked_companies = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "topsis_results"

    def __str__(self):
        return f"{self.name}"
    

class FuzzyTopsisResult(models.Model):
    criteria_weights = models.JSONField()
    ranked_companies = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "fuzzy_topsis_results"

    def __str__(self):
        return f"{self.name}"
    

class WaspasResult(models.Model):
    criteria_weights = models.JSONField()
    ranked_companies = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "waspas_results"

    def __str__(self):
        return f"{self.name}"