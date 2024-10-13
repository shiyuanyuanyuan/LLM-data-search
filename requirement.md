# Help Complete with some exploratory research of LLM capabilities

## Standardization of Data
- Improve match rates
- Use LLMs to standardize common data points that customers or Sales Reps fill out

### Data Points to Standardize
- **Company name**: 
  - Remove common prefixes and suffices, special characters and spaces, expand acronyms
- **Address**: 
  - Standardize and expand abbreviations
- **Job title**: 
  - Standardize, expand acronyms
- **Industry**: 
  - Standardize, expand acronyms
- **Phone Number**: 
  - Strip typical formatting data (parentheses, dashes, country codes, etc.) and leave only numbers

## Outcomes
- Create prompts that reliably produce standardized outputs for the data points above
- Feel free to explore outcomes with any LLM, you can use:
  - @ZachGPT Bot
  - Anthropic
  - Ollama, etc.

## Scripts
- Develop scripts to run standardization on large volumes of records for testing
- We will share a sample data set with you to get started, though you can also generate sample data for this research
- We will provide an existing script for Google Sheets that we used to fetch account parents

## Final Outcome
- A script to validate if LLMs can clean up and standardize record data at scale and is easy to use for quick iteration
