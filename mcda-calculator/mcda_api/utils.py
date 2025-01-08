import json
from pathlib import Path
import logging

from .models import *

logger = logging.getLogger(__name__)

def get_default_companies():
    """
    Fetches companies from the database. If there are no companies, pushes a hardcoded default list.
    """
    companies = list(Companies.objects.values('name', 'profit', 'profit_change', 'rank', 'rank_change', 'revenue', 'revenue_change', 'years_in_rank', 'assets', 'employees'))
    if not companies:
        logger.warning("No companies found in the database. Falling back to hardcoded defaults.")
        from .defaults.raw_companies import companies_data
        
        for company in companies_data:
            Companies.objects.create(
                name=company['name'],
                profit=float(company['profit'].replace('$', '').replace(',', '')),
                profit_change=float(company['profit_change'].replace('%', '')) if company['profit_change'] != '-' else 0,
                rank=int(company['rank']),
                rank_change=int(company['rank_change']) if company['rank_change'] != '-' else 0,
                revenue=float(company['revenue'].replace('$', '').replace(',', '')),
                revenue_change=float(company['revenue_change'].replace('%', '')) if company['revenue_change'] != '-' else 0,
                years_in_rank=int(company['years_in_rank']),
                assets=float(company['assets'].replace('$', '').replace(',', '')),
                employees=int(company['employees'].replace(',', ''))
            )
        
        companies = list(Companies.objects.all().values('name', 'profit', 'profit_change', 'rank', 'rank_change', 'revenue', 'revenue_change', 'years_in_rank', 'assets', 'employees'))
        logger.info(f"Inserted {len(companies)} default companies into the database.")
    else:
        logger.info(f"Fetched {len(companies)} companies from the database.")

    return companies


def get_default_criteria():
    """
    Fetches criteria from the database. If there is no criteria in the database, falls back to a hardcoded default list.
    """
    criteria = list(DefaultCriteria.objects.all().values('name', 'field', 'default_weight', 'type'))
    if not criteria:
        logger.warning("No criteria found in the database. Falling back to hardcoded defaults.")
        from .defaults.criteria import default_criteria

        for criterion in default_criteria:
            DefaultCriteria.objects.create(
                name=criterion['name'],
                field=criterion['field'],
                default_weight=criterion['default_weight'],
                type=criterion['type']
            )
        
        logger.info(f"Inserted {len(default_criteria)} default companies into the database.")
        return default_criteria
    else:
        logger.info(f"Fetched {len(criteria)} criteria from the database.")
    return criteria