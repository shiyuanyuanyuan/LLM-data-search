# LLM Data Clean

## Overview
LLM Data Clean is a Python project designed to facilitate the cleaning and preparation of data for use with OpenAI's language models. This project provides a command-line interface (CLI) for interacting with the OpenAI API, allowing users to perform various operations such as file management, model training, and more.

## Features
- Clean and preprocess data for training language models.
- Interact with the OpenAI API to manage files, models, and fine-tuning jobs.
- Command-line interface for easy usage.

## Requirements
- Python 3.12 or higher
- OpenAI Python library (version 0.28.0 or higher)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv myenv
   ```

3. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source myenv/bin/activate
     ```
   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Setting Up the OpenAI API Key
To use the OpenAI API, you need to set your API key. You can do this in one of the following ways:

### Option 1: Set as an Environment Variable

