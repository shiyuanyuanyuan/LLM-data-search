import csv
import openai
import json
import os
import re
from typing import List, Dict, Optional


class Company:
    def __init__(self, id: str, name: str, domain: str):
        self.id = id
        self.name = name
        self.domain = domain
        self.direct_parent: Optional[str] = None
        self.global_parent: Optional[str] = None


# Caching dictionary to store results and avoid duplicate API calls
cache = {}


def load_companies(file_path: str) -> List[Company]:
    companies = []
    try:
        print(f"Loading companies from {file_path}")
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                companies.append(Company(
                    id=row['Id'],
                    name=row['Name'],
                    domain=row['TracHier__Domain__c']
                ))
        print(f"Loaded {len(companies)} companies")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    return companies


def get_company_hierarchy(company: Company) -> Company:
    # Check cache before making API request
    if company.name in cache:
        print(f"Using cached result for {company.name}")
        cached_result = cache[company.name]
        company.direct_parent = cached_result['direct_parent']
        company.global_parent = cached_result['global_parent']
        return company

    messages = [
        {
            "role": "system",
            "content": "You are an expert in company hierarchy and parent companies. Provide accurate information even if the data is publicly available."
        },
        {
            "role": "user",
            "content": f"What is the direct parent company and global ultimate parent company of {company.name}? Respond in the format: 'Direct parent: [direct parent], Global ultimate parent: [global ultimate parent].'"
        }
    ]

    try:    
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use the latest chat model
            messages=messages,
            max_tokens=100,
            temperature=0.2
        )

        if response and 'choices' in response and len(response.choices) > 0:
            content = response.choices[0].message['content'].strip()
            print("Processed response:", content)

            # Use regular expressions to extract parent company names
            direct_parent_match = re.search(r"Direct parent:\s*(.*?)(,|$)", content, re.IGNORECASE)
            global_parent_match = re.search(r"Global ultimate parent:\s*(.*?)(,|$)", content, re.IGNORECASE)

            if direct_parent_match:
                company.direct_parent = direct_parent_match.group(1).strip()
            else:
                company.direct_parent = "Not found"

            if global_parent_match:
                company.global_parent = global_parent_match.group(1).strip()
            else:
                company.global_parent = "Not found"

            # Store the result in the cache
            cache[company.name] = {
                'direct_parent': company.direct_parent,
                'global_parent': company.global_parent
            }

    except Exception as e:
        print(f"Error with API request: {e}")
        company.direct_parent = "Not found"
        company.global_parent = "Not found"

    return company


def process_companies(companies: List[Company]):
    print(f"Processing {len(companies)} companies")
    for company in companies:
        get_company_hierarchy(company)  # Update directly
    print(f"Processed {len(companies)} companies")


def save_results(companies: List[Company], output_file: str):
    try:
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['Id', 'Name', 'Domain', 'Direct Parent', 'Global Parent']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company in companies:
                writer.writerow({
                    'Id': company.id,
                    'Name': company.name,
                    'Domain': company.domain,
                    'Direct Parent': company.direct_parent,
                    'Global Parent': company.global_parent
                })
    except Exception as e:
        print(f"Error saving results: {e}")


def main():
    input_file = 'data/sampleAccount.csv'
    output_file = 'data/company_hierarchy(0.1).csv'
    
    openai.api_key = os.getenv('OPENAI_API_KEY')

    companies = load_companies(input_file)
    company_test_list = companies[:49]  # For testing, process only a subset
    process_companies(company_test_list)
    save_results(company_test_list, output_file)


if __name__ == '__main__':
    main()
