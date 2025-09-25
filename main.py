#!/usr/bin/env python3
"""
Delete Jobs Script - Main Module
"""
import pandas as pd
import requests as rq
import os
from dotenv import load_dotenv
import sys
import argparse

load_dotenv()
BASE_URL = "https://verify.vouched.id/api/jobs/"
VOUCHED_API_KEY = os.getenv("VOUCHED_API_KEY")

def get_csv_path():
    """Get the CSV file path and column name from command line arguments or user input."""
    parser = argparse.ArgumentParser(description='Process CSV file path and column name')
    parser.add_argument('--csv', help='Path to CSV file', default=None)
    parser.add_argument('--column', help='Name of Job ID column', default=None)
    args = parser.parse_args()

    csv_path = args.csv if args.csv else input("Please enter the path to the CSV file: ")
    column_name = args.column if args.column else input("Please enter the name of the Job ID column: ")
    return csv_path, column_name


def load_csv():
    """Load the csv file."""
    csv_path, column_name = get_csv_path()
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows from CSV")
    return df, column_name


def delete_job(id):
    """Delete the job and log the result."""
    url = BASE_URL + id
    headers = {
        'X-API-Key': VOUCHED_API_KEY,
        'Accept': 'application/json',
        'charset': 'utf-8'
    }
    response = rq.delete(url, headers=headers)
    
    # Handle non-JSON responses gracefully
    try:
        response_data = response.json()
    except (ValueError, rq.exceptions.JSONDecodeError):
        # If response is not JSON, store the text content or status info
        response_data = {
            'text': response.text,
            'content_type': response.headers.get('content-type', 'unknown')
        }
    
    result = {
        'job_id': id,
        'status_code': response.status_code,
        'response': str(response_data)  # Convert to string for CSV storage
    }
    
    output_file = 'deletion_log.csv'
    file_exists = os.path.exists(output_file)
    
    df = pd.DataFrame([result])
    df.to_csv(output_file, mode='a', header=not file_exists, index=False)
    
    print(f"Job {id}: Status {response.status_code}")

    return result


def main():
    """Main function to run the script."""
    print("Delete Jobs Script initialized")
    load_dotenv()
    df, column_name = load_csv()
    print(f"Loaded {len(df)} rows from CSV")
    print(f"Job ID column name: {column_name}")
    
    deletion_results = []
    for index, row in df.iterrows():
        result = delete_job(row[column_name])
        deletion_results.append(result)

    successful_deletions = sum(1 for result in deletion_results if result['status_code'] == 200)
    print(f"Successfully deleted {successful_deletions} jobs")
    print("Script completed")


if __name__ == "__main__":
    main()