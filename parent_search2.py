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


def get_company_hierarchy(companies: List[Company]) -> Dict[str, Dict[str, str]]:
    results = {}
    batch_size = 10

    for i in range(0, len(companies), batch_size):
        batch = companies[i:i + batch_size]
        company_data = [{"name": company.name, "domain": company.domain} for company in batch]
        messages = [
            {"role": "user", "content": f"Here are the companies: {json.dumps(company_data)}. "
                                         "Please respond with their direct parent and global parent in the following JSON format: "
                                         "{\"Company Name\": {\"direct_parent\": \"Parent Name\", \"global_parent\": \"Global Parent Name\"}}. "
                                         "Make sure to include all companies listed."}
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=700,
                temperature=0.5
            )

            content = response.choices[0].message['content'].strip()
            print("Raw API response:", content)

            # Validate and parse the response
            try:
                # Parse the content as JSON
                parsed_content = json.loads(content)
                if isinstance(parsed_content, dict):
                    results.update(parsed_content)  # Update the results dictionary
                else:
                    print(f"Unexpected response format: {content}")
                    for company in batch:
                        results[company['name']] = {"direct_parent": None, "global_parent": None}
            except json.JSONDecodeError:
                print(f"Failed to decode JSON: {content}")
                for company in batch:
                    results[company['name']] = {"direct_parent": None, "global_parent": None}

        except Exception as e:
            print(f"Error with API request: {e}")
            for company in batch:
                results[company['name']] = {"direct_parent": None, "global_parent": None}

    return results  # Return the dictionary


def process_companies(companies: List[Company]):
    print(f"Processing {len(companies)} companies")
    hierarchies = get_company_hierarchy(companies)

    print(f"Type of hierarchies: {type(hierarchies)}")

    for company in companies:
        hierarchy = hierarchies.get(company.name)
        if hierarchy:
            company.direct_parent = hierarchy.get('direct_parent', "Not Found")
            company.global_parent = hierarchy.get('global_parent', "Not Found")
        else:
            company.direct_parent = "Not Found"
            company.global_parent = "Not Found"

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
    output_file = 'data/company_hierarchy2.csv'
    
    openai.api_key = os.getenv('OPENAI_API_KEY')
    companies = load_companies(input_file)
    process_companies(companies)
    save_results(companies, output_file)


if __name__ == '__main__':
    main()
