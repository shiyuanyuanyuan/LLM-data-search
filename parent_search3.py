import csv
import anthropic
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


def get_company_hierarchy(company: Company) -> None:
    print(f"Getting company hierarchy for {company.name}")
    client = anthropic.Anthropic()
    prompt = f"""You are tasked with identifying the direct parent company and the global ultimate parent company of a given company. This information is crucial for understanding corporate structures and ownership hierarchies.

The company you need to research is:
<company_name>
{company.name}
</company_name>

Please follow these steps:

1. Research the ownership structure of the company named above.
2. Identify the direct parent company, which is the immediate owner or controlling entity of the given company.
3. Determine the global ultimate parent company, which is the topmost entity in the corporate hierarchy that ultimately owns or controls the given company.
4. If you cannot find reliable information about either the direct parent or the global ultimate parent, indicate this by writing "Unknown" for that particular entity.

Provide your response in the following format:
<answer>
Direct parent: [Name of direct parent company or "Unknown"]
Global ultimate parent: [Name of global ultimate parent company or "Unknown"]
</answer>

Important: Only include information that you can verify from reliable sources. Do not speculate or guess. If you cannot find accurate information, it's better to state "Unknown" than to provide potentially incorrect data."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    response_content = message.content[0].text
    answer_match = re.search(r'<answer>(.*?)</answer>', response_content, re.DOTALL)
    if answer_match:
        answer = answer_match.group(1).strip()
        direct_parent_match = re.search(r'Direct parent: (.+)', answer)
        global_parent_match = re.search(r'Global ultimate parent: (.+)', answer)
        
        company.direct_parent = direct_parent_match.group(1) if direct_parent_match else "Unknown"
        company.global_parent = global_parent_match.group(1) if global_parent_match else "Unknown"
    else:
        print(f"Could not extract answer for company: {company.name}")
        company.direct_parent = "Unknown"
        company.global_parent = "Unknown"


def process_companies(companies: List[Company]):
    print(f"Processing {len(companies)} companies")
    for company in companies:
        get_company_hierarchy(company)
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
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"Error saving results: {e}")


def main():
    input_file = 'data/sampleAccount.csv'
    output_file = 'data/company_hierarchy3.csv'

    companies = load_companies(input_file)
    company_test_list = companies[:49]  # For testing, process only a subset
    process_companies(company_test_list)
    save_results(company_test_list, output_file)


if __name__ == '__main__':
    main()