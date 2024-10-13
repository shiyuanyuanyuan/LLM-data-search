# Process

## Try 1
- Use the `parent_search.py` script to fetch the parent companies for the given list of companies.
- This script uses the OpenAI API to get the parent companies.
- This script uses the fetched data to change the company object one by one.
- The script is set to process 1 company at a time to avoid rate limiting.
- 10 companies take 17 seconds.
- 49 companies take 1 minute 10 seconds.
- Pros:
  - Relatively simple to implement.
- Cons:
  - Only able to process 1 company at a time, relatively slow.

## Try 2
- Use the `parent_search.py` script to fetch the parent companies for the given list of companies.
- This script uses the OpenAI API to get the parent companies.
- This script uses the plain text reply and cleans it to a dict.
- The script is set to process several companies at a time to avoid rate limiting.
- Pros:
  - Able to process multiple companies at a time.
- Cons:
  - More complex to implement.
  - The correctness of the results is not guaranteed.
  - 49 companies take 16 seconds.(batch size 10)
  - 49 companies take 30 seconds.(batch size 5)

## Try 3
- Use the `parent_search.py` script to fetch the parent companies for the given list of companies.
- This script uses the Anthropic API to get the parent companies.
- This script uses the plain text reply and cleans it to the class Company object.
- The script is set to process 1 company at a time.
- The script uses the `temperature` parameter to control the creativity of the model.
- The script differentiates the companies with no parent as unknown or None.
- 10 companies take 27 seconds.
- 49 companies take 2 minutes 20 seconds.
