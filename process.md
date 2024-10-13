# Process

##  Try 1
- Use the `parent_search.py` script to fetch the parent companies for the given list of companies.
- This script uses the OpenAI API to get the parent companies.
- This script uses the fetched data to change the company object one by one
- The script is set to process 1 companies at a time to avoid rate limiting.
- 10 companies takes 17 seconds
- 49 companies takes 1 minute 10 seconds
- pros:
  - relatively simple to implement
- cons:
  - Only able to process 1 company at a time, relatively slow

## Try 2
- Use the `parent_search.py` script to fetch the parent companies for the given list of companies.
- This script uses the OpenAI API to get the parent companies.
- This script uses the plain text reply and clean it to a dict
- The script is set to process 10 companies at a time to avoid rate limiting.
- pros:
  - able to process multiple companies at a time
- cons:
  - more complex to implement
  - the correctness of the results is not guaranteed
  - 10 companies takes 16 seconds


# Try 3
- Use the `parent_search.py` script to fetch the parent companies for the given list of companies.
- This script uses the Anthropic API to get the parent companies.
- This script uses the plain text reply and clean it to the class Company object
- The script is set to process 1 companies at a time.
- 27s for 10 companies
- 49 companies takes 2 minutes 20 seconds
