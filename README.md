# Customer Data Analysis Agent

A production-ready application that leverages LLMs to analyze customer and sales data.

## Project Structure

```
project_root/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── prompt.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── data_tools.py
│   │   └── python_tools.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── data/
│   └── csv_files/
│       ├── customer_profiles.csv
│       └── sales_transactions.csv
├── config/
│   └── settings.py
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Ensure your CSV files are in the appropriate directory:
   ```
   data/csv_files/customer_profiles.csv
   data/csv_files/sales_transactions.csv
   ```

## Usage

```
    streamlit run main.py
```

## Features

- Entity verification with exact and partial matching
- Interactive Python REPL for data analysis
- LangGraph ReAct agent for reasoning about data
- Support for multiple dataframes
- Clean, modular design for easy maintenance and extension

## Customization

You can customize the application by:

1. Modifying the system prompt in `app/agent/prompt.py`
2. Adding new tools in the `app/tools/` directory
3. Adjusting LLM parameters in `config/settings.py`
4. Adding more CSV files to analyze in `app/utils/helpers.py`
