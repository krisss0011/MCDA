import requests
from .models import DefaultCriteria
from pyDecision.algorithm import ahp_method, waspas_method, topsis_method, fuzzy_topsis_method
import numpy as np
import logging


def fetch_company_data():
    """
    Fetches companies from the API
    """
    companies_url = 'http://127.0.0.1:8000/api/companies/'
    response = requests.get(companies_url)
    return response.json()


def fetch_default_criteria():
    """
    Fetches default criteria from the API
    """
    criteria_url = 'http://127.0.0.1:8000/api/default-criteria/'
    response = requests.get(criteria_url)
    logging.debug(f"Response Status: {response.status_code}")
    logging.debug(f"Response Content: {response.text}")
    try:
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None


def calculate_mcdm(method, weights, companies_data, criterion_type=None):
    """
    Calculate the MCDA using the specified method
    """
    supported_methods = {
        'ahp': lambda: ahp_calculation(weights, companies_data),
        'topsis': lambda: topsis_calculation(weights, companies_data, criterion_type),
        'fuzzy_topsis': lambda: fuzzy_topsis_calculation(weights, companies_data, criterion_type),
        'waspas': lambda: wsm_calculation(weights, companies_data, criterion_type),
    }
    
    if method == 'all':
        return {m: f() for m, f in supported_methods.items()}
    
    try:
        calculation_function = supported_methods[method]
        return calculation_function()
    except KeyError:
        raise ValueError(f"Unsupported MCDA method. Supported methods are: {list(supported_methods.keys())}")


def clean_value(value):
    """
    Clean the value of a criterion
    """
    if isinstance(value, str):
        return float(value.replace(',', '').replace('$', '').replace('%', '').strip())
    return value


def prepare_dataset(companies_data, criteria_data):
    """
    Prepare the dataset for MCDA calculation
    """
    dataset = []
    for company in companies_data:
        data_row = []
        for criterion in criteria_data:
            raw_value = company.get(criterion['field'], 0)
            cleaned_value = clean_value(raw_value) if raw_value != '-' else 0
            data_row.append(cleaned_value)
        dataset.append(data_row)
    return np.array(dataset)


def prepare_fuzzy_dataset(companies_data, criteria_data):
    """
    Prepare fuzzy dataset by converting crisp values to triangular fuzzy numbers
    """
    dataset = []
    for company in companies_data:
        data_row = []
        for criterion in criteria_data:
            raw_value = company.get(criterion['field'], 0)
            if raw_value == '-':
                raw_value = 0
            cleaned_value = clean_value(raw_value)
            
            # Create triangular fuzzy number
            lower = cleaned_value * 0.9
            middle = cleaned_value
            upper = cleaned_value * 1.1
            
            data_row.append((lower, middle, upper))
        dataset.append(data_row)
    return dataset


def ahp_calculation(weights, companies_data):
    """
    Calculate the MCDA using the Ahp method
    """
    criteria_data = fetch_default_criteria()
    dataset = prepare_dataset(companies_data, criteria_data)
    
    weights_array = np.array(weights)
    
    comparison_matrix = np.outer(weights_array, 1 / weights_array)
    weights_from_ahp, consistency_ratio = ahp_method(comparison_matrix, wd='geometric')
    
    scores = []
    for company_data, company in zip(dataset, companies_data):
        score = 0
        for value, weight in zip(company_data, weights_from_ahp):
            score += value * weight
        company['score'] = score
        scores.append((company['name'], score))
    
    ranked_companies = sorted(scores, key=lambda x: x[1], reverse=True)
    
    criteria_info = []
    for criterion, weight in zip(criteria_data, weights):
        criteria_info.append((criterion['name'], weight))

    return {
        "criteria": criteria_info,
        "ranked_companies": ranked_companies
    }


def topsis_calculation(weights, companies_data, criterion_type):
    """
    Calculate the MCDA using the Topsis method
    """
    criteria_data = fetch_default_criteria()
    dataset = prepare_dataset(companies_data, criteria_data)
    normalized_weights = np.array(weights) / np.sum(weights)
    
    # Extract just the type values (-1 or 1) for the algorithm
    criterion_types_list = [ct['type'] for ct in criterion_type]

    scores = topsis_method(dataset, normalized_weights, criterion_types_list, graph=False, verbose=False)

    ranked_companies = sorted([(company['name'], score) for company, score in zip(companies_data, scores)], key=lambda x: x[1], reverse=True)

    criteria_info = []
    for criterion, weight in zip(criteria_data, weights):
        criteria_info.append((criterion['name'], weight))

    return {
        "criteria": criteria_info,
        "ranked_companies": ranked_companies
    }


def fuzzy_topsis_calculation(weights, companies_data, criterion_type):
    """
    Calculate the MCDA using the Fuzzy TOPSIS method
    """
    try:
        # Fetch and validate criteria data
        criteria_data = fetch_default_criteria()
        if not criteria_data:
            raise ValueError("Failed to fetch criteria data")
        
        # Extract criterion types as a list of 1 and -1
        criterion_types_list = [ct['type'] for ct in criterion_type]
        
        # Prepare fuzzy dataset
        dataset = prepare_fuzzy_dataset(companies_data, criteria_data)
        logging.debug(f"Fuzzy dataset prepared with shape: {len(dataset)}x{len(dataset[0])}")

        # Prepare fuzzy weights
        normalized_weights = np.array(weights) / np.sum(weights)
        fuzzy_weights = []
        for weight in normalized_weights:
            fuzzy_weights.append((weight * 0.95, weight, weight * 1.05))
        fuzzy_weights = np.array(fuzzy_weights, dtype=object)

        # Calculate Fuzzy TOPSIS scores
        fuzzy_topsis_scores = fuzzy_topsis_method(
            dataset=dataset,
            weights=fuzzy_weights,
            criterion_type=criterion_types_list,
            graph=False
        )

        # Prepare rankings
        ranked_companies = []
        for idx, (company, score) in enumerate(
            sorted(
                zip(companies_data, fuzzy_topsis_scores),
                key=lambda x: x[1],
                reverse=True
            )
        ):
            ranked_companies.append((company['name'], float(score)))

        # Prepare criteria info
        criteria_info = []
        for criterion, weight in zip(criteria_data, weights):
            criteria_info.append((criterion['name'], weight))

        return {
            "criteria": criteria_info,
            "ranked_companies": ranked_companies,
            "success": True
        }

    except Exception as e:
        logging.error(f"Error in fuzzy_topsis_calculation: {str(e)}")
        return {
            "error": str(e),
            "success": False
        }


def wsm_calculation(weights, companies_data, criterion_type):
    try:
        criteria_data = fetch_default_criteria()
        dataset = prepare_dataset(companies_data, criteria_data)
        normalized_weights = np.array(weights) / np.sum(weights)
        lambda_value = 0.5
        
        # Extract just the type values (-1 or 1) for the algorithm
        criterion_types_list = [ct['type'] for ct in criterion_type]
        
        wsm, wpm, waspas_scores = waspas_method(
            dataset, 
            criterion_types_list, 
            normalized_weights, 
            lambda_value, 
            graph=False
        )
        
        ranked_companies = sorted(
            [(company['name'], score) for company, score in zip(companies_data, waspas_scores)], 
            key=lambda x: x[1], 
            reverse=True
        )

        criteria_info = []
        for criterion, weight in zip(criteria_data, weights):
            criteria_info.append((criterion['name'], weight))

        return {
            "criteria": criteria_info,
            "ranked_companies": ranked_companies
        }

    except Exception as e:
        print(f"Error during WASPAS calculation: {str(e)}")
        return {"error": str(e), "success": False}