# Vouched Jobs Deletion Script

A Python script that bulk deletes jobs from the Vouched API by reading job IDs from a CSV file. The script processes each job ID, makes DELETE requests to the Vouched API, and logs the results to a CSV file for tracking.

## Features

- Reads job IDs from any CSV file with configurable column names
- Makes authenticated DELETE requests to the Vouched API
- Logs all deletion attempts with status codes and responses
- Supports command-line arguments or interactive input for CSV path and column name
- Gracefully handles API responses (both JSON and non-JSON)
- Provides progress feedback and summary statistics

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your Vouched API key:
   ```
   VOUCHED_API_KEY=your_api_key_here
   ```

## Usage

### Command Line Arguments
```bash
python main.py --csv jobs.csv --column job_id
```

### Interactive Mode
```bash
python main.py
```
The script will prompt you to enter:
- Path to the CSV file containing job IDs
- Name of the column containing the job IDs

## Input Format

Your CSV file should contain a column with job IDs. For example:
```csv
row_num,job_id,name
1,N8JhkLW0c,Tom Walsh
2,vn5adMACL,Crosscheck-TW
```

## Output

The script generates a `deletion_log.csv` file that logs:
- `job_id`: The ID of the job that was processed
- `status_code`: HTTP status code from the API response
- `response`: The API response data

## API Endpoint

The script targets the Vouched API at: `https://verify.vouched.id/api/jobs/{job_id}`

## Requirements

- Python 3.6+
- Valid Vouched API key
- CSV file with job IDs to delete

## Dependencies

- `pandas` - For CSV file processing
- `requests` - For HTTP API calls
- `python-dotenv` - For environment variable management