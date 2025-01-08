"""
Signals for the mcda_api app
"""
def run_on_post_migrate(sender, **kwargs):        
    from .utils import get_default_companies, get_default_criteria    
    get_default_companies()
    get_default_criteria()
