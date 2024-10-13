import csv
import openai
import json
import os
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


def get_company_hierarchy(companies: List[Company]) -> List[Dict[str, str]]:
    results = []
    batch_size = 10  # Process 10 companies at a time

    for i in range(0, len(companies), batch_size):
        batch = companies[i:i + batch_size]
        company_data = [{"name": company.name, "domain": company.domain} for company in batch]
        messages = [
            {"role": "user", "content": f"Here are the companies: {json.dumps(company_data)}. "
                                         "Please respond with their direct parent and global parent in JSON format."}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=700,  # Adjust this as needed
                temperature=0.5
            )

            # Print the raw response for debugging
            print("Raw API response:", response)

            # Extract the response content and convert it to a list of dictionaries
            content = response.choices[0].message['content'].strip()
            # Ensure the content is parsed correctly
            if content.startswith('{'):
                # If the content is a JSON object, convert it to a list of dictionaries
                results.append(json.loads(content))
            else:
                # If the content is a JSON array, load it directly
                results.extend(json.loads(content))

        except json.JSONDecodeError as json_err:
            print(f"JSON decode error: {json_err}")
            results.extend([{"direct_parent": None, "global_parent": None} for _ in batch])
        except Exception as e:
            print(f"Error with API request: {e}")
            results.extend([{"direct_parent": None, "global_parent": None} for _ in batch])

    return results


def process_companies(companies: List[Company]):
    print(f"Processing {len(companies)} companies")
    hierarchies = get_company_hierarchy(companies)
    for company, hierarchy in zip(companies, hierarchies):
        company.direct_parent = hierarchy.get('direct_parent')
        company.global_parent = hierarchy.get('global_parent')
    print("Process finished")


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
    output_file = 'data/company_hierarchy.csv'
    
    openai.api_key = os.getenv('OPENAI_API_KEY')
    companies = load_companies(input_file)
    process_companies(companies)
    save_results(companies, output_file)


if __name__ == '__main__':
    main()
