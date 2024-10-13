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
    prompt = f"""Identify the direct parent company and global ultimate parent company of {company.name}.
Format your response exactly as follows:
Direct parent: [Name or "None" if the company has no parent, or "Unknown" if you can't find the information]
Global ultimate parent: [Name or "None" if the company has no global parent, or "Unknown" if you can't find the information]
Explanation: [Brief explanation of your findings or why you couldn't find the information]

Only include verified information. If you're unsure or can't find information, use "Unknown" and explain why in the Explanation section."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=300,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    response_content = message.content[0].text
    direct_parent_match = re.search(r'Direct parent: (.+)', response_content)
    global_parent_match = re.search(r'Global ultimate parent: (.+)', response_content)
    explanation_match = re.search(r'Explanation: (.+)', response_content, re.DOTALL)
    
    if direct_parent_match and global_parent_match:
        company.direct_parent = direct_parent_match.group(1).strip()
        company.global_parent = global_parent_match.group(1).strip()
        explanation = explanation_match.group(1).strip() if explanation_match else "No explanation provided."
    else:
        print(f"Could not extract answer for company: {company.name}")
        company.direct_parent = "Error"
        company.global_parent = "Error"
        explanation = "Error in parsing the response."

    print(f"Hierarchy for {company.name}:")
    print(f"  Direct Parent: {company.direct_parent}")
    print(f"  Global Parent: {company.global_parent}")
    print(f"  Explanation: {explanation}")


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