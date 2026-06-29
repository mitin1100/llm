"""

Modular Data Pipeline - Ingestion Component

Course: Open source Data Engineering with Spark, dbt & Airflow

Module 1: Create modular pipeline stages - Foundation

This starter code provides the foundation for building a modular ingestion component

that extracts e-commerce order data from a REST API.

"""

import requests

import json

import logging

from datetime import datetime

from typing import Dict, List, Optional, Any

# Configure basic logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# PROVIDED CODE - DO NOT MODIFY

# Test API endpoint for demonstration purposes

TEST_API_ENDPOINT = "https://jsonplaceholder.typicode.com/posts"  # Simulates order data

class IngestionConfig:

    """Configuration management for ingestion module"""

    

    def __init__(self, environment: str = 'development'):

        self.environment = environment

        # TODO: Implement configuration loading logic

        self.config = {

            'api_endpoint': TEST_API_ENDPOINT,

            'timeout': 30,

            'max_retries': 3,

            'output_format': 'json',

            'output_directory': './data/raw'

        }

class OrderIngestion:

    """Modular ingestion component for e-commerce order data"""

    

    def __init__(self, config: IngestionConfig):

        self.config = config

        self.session = requests.Session()

    

    def extract_orders(self, since_timestamp: Optional[str] = None) -> List[Dict[str, Any]]:

        """

        Extract order data from API with proper error handling

        

        PRACTICE CHALLENGE 1

        TASK: Implement API data extraction with validation for required fields (order_id, customer_id, order_date)

        YOUR CODE HERE

        """

        # TODO: Implement API call with error handling

        # TODO: Add retry logic for failed requests

        # TODO: Validate required fields in response data

        # TODO: Return list of valid order records

        pass

    

    def store_data(self, data: List[Dict[str, Any]], metadata: Dict[str, Any]) -> str:

        """

        Store extracted data with metadata

        

        PRACTICE CHALLENGE 2

        TASK: Implement data storage with atomic operations and proper error handling

        YOUR CODE HERE

        """

        # TODO: Create output directory if needed

        # TODO: Generate appropriate filename with timestamp

        # TODO: Implement atomic write operation (temp file -> rename)

        # TODO: Handle storage errors gracefully

        # TODO: Return filepath of stored data

        pass

    

    def run_ingestion(self, since_timestamp: Optional[str] = None) -> Dict[str, Any]:

        """

        Main orchestration function for ingestion process

        

        PRACTICE CHALLENGE 3

        TASK: Implement incremental extraction with timestamp tracking

        YOUR CODE HERE

        """

        # TODO: Load last extraction timestamp if not provided

        # TODO: Extract data using extract_orders()

        # TODO: Prepare metadata for storage

        # TODO: Store data using store_data()

        # TODO: Update last extraction timestamp

        # TODO: Return execution results

        pass

# Example usage for testing

if __name__ == "__main__":

    # Test your implementation

    config = IngestionConfig('development')

    ingestion = OrderIngestion(config)

    

    # Test basic extraction

    print("Testing ingestion component...")

    # TODO: Add your test code here
