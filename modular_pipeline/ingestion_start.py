"""

Modular Data Pipeline - Ingestion Component - COMPLETE SOLUTION
Course: Open source Data Engineering with Spark, dbt & Airflow
Module 1: Create modular pipeline stages - Foundation

"""

import requests

import json

import logging

import os

from datetime import datetime

from typing import Dict, List, Optional, Any

# Configure logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# PROVIDED CODE - DO NOT MODIFY

TEST_API_ENDPOINT = "https://jsonplaceholder.typicode.com/posts"

class IngestionConfig:

    """Configuration management for ingestion module"""

    

    def __init__(self, environment: str = 'development'):

        self.environment = environment

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

        # ____________________________________

        # SOLUTION CODE

        for attempt in range(self.config.config['max_retries'] + 1):

            try:

                logger.info(f"Attempting to extract orders (attempt {attempt + 1})")

                

                response = self.session.get(

                    self.config.config['api_endpoint'],

                    timeout=self.config.config['timeout']

                )

                

                if response.status_code == 200:

                    data = response.json()

                    

                    # For demo API, transform posts to look like orders

                    orders = []

                    for post in data[:10]:  # Limit to 10 records for demo

                        order = {

                            'order_id': post['id'],

                            'customer_id': post['userId'],

                            'order_date': datetime.now().isoformat(),

                            'title': post['title'],

                            'body': post['body']

                        }

                        orders.append(order)

                    

                    # Validate required fields

                    valid_orders = []

                    required_fields = ['order_id', 'customer_id', 'order_date']

                    

                    for order in orders:

                        if all(field in order and order[field] is not None for field in required_fields):

                            valid_orders.append(order)

                        else:

                            logger.warning(f"Skipping invalid order record: {order.get('order_id', 'unknown')}")

                    

                    logger.info(f"Successfully extracted {len(valid_orders)} valid orders")

                    return valid_orders

                

                else:

                    logger.error(f"API request failed with status {response.status_code}")

                    if attempt == self.config.config['max_retries']:

                        raise requests.exceptions.HTTPError(f"API request failed: {response.status_code}")

            

            except requests.exceptions.Timeout:

                logger.warning(f"Request timeout (attempt {attempt + 1})")

                if attempt == self.config.config['max_retries']:

                    raise

            

            except requests.exceptions.ConnectionError:

                logger.warning(f"Connection error (attempt {attempt + 1})")

                if attempt == self.config.config['max_retries']:

                    raise

        

        return []

        # END SOLUTION CODE

        # ____________________________________

    

    def store_data(self, data: List[Dict[str, Any]], metadata: Dict[str, Any]) -> str:

        """

        Store extracted data with metadata

        

        PRACTICE CHALLENGE 2

        TASK: Implement data storage with atomic operations and proper error handling

        YOUR CODE HERE

        """

        # ____________________________________

        # SOLUTION CODE

        if not data:

            logger.warning("No data to store")

            return ""

        

        # Create output directory if it doesn't exist

        output_dir = self.config.config['output_directory']

        os.makedirs(output_dir, exist_ok=True)

        

        # Generate filename with timestamp

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        filename = f"orders_{timestamp}.{self.config.config['output_format']}"

        filepath = os.path.join(output_dir, filename)

        

        # Prepare data with metadata

        output_data = {

            'metadata': metadata,

            'data': data

        }

        

        try:

            # Atomic write operation - write to temp file first

            temp_filepath = f"{filepath}.tmp"

            

            with open(temp_filepath, 'w') as f:

                json.dump(output_data, f, indent=2, default=str)

            

            # Rename temp file to final filename (atomic operation)

            os.rename(temp_filepath, filepath)

            

            logger.info(f"Successfully stored {len(data)} records to {filepath}")

            return filepath

        

        except Exception as e:

            logger.error(f"Failed to store data: {str(e)}")

            # Clean up temp file if it exists

            if os.path.exists(temp_filepath):

                os.remove(temp_filepath)

            raise

        # END SOLUTION CODE

        # ____________________________________

    

    def run_ingestion(self, since_timestamp: Optional[str] = None) -> Dict[str, Any]:

        """

        Main orchestration function for ingestion process

        

        PRACTICE CHALLENGE 3

        TASK: Implement incremental extraction with timestamp tracking

        YOUR CODE HERE

        """

        # ____________________________________

        # SOLUTION CODE

        start_time = datetime.now()

        

        try:

            # Load last extraction timestamp if not provided

            if since_timestamp is None:

                since_timestamp = self._get_last_extraction_timestamp()

            

            # Extract data

            orders = self.extract_orders(since_timestamp)

            

            if not orders:

                logger.info("No new orders to process")

                return {

                    'status': 'success',

                    'records_processed': 0,

                    'execution_time': (datetime.now() - start_time).total_seconds()

                }

            

            # Prepare metadata

            metadata = {

                'extraction_timestamp': start_time.isoformat(),

                'record_count': len(orders),

                'environment': self.config.environment,

                'api_endpoint': self.config.config['api_endpoint'],

                'since_timestamp': since_timestamp

            }

            

            # Store data

            filepath = self.store_data(orders, metadata)

            

            # Update last extraction timestamp

            self._update_last_extraction_timestamp(start_time.isoformat())

            

            end_time = datetime.now()

            execution_time = (end_time - start_time).total_seconds()

            

            result = {

                'status': 'success',

                'records_processed': len(orders),

                'output_file': filepath,

                'execution_time': execution_time,

                'metadata': metadata

            }

            

            logger.info(f"Ingestion completed successfully: {len(orders)} records in {execution_time:.2f} seconds")

            return result

        

        except Exception as e:

            logger.error(f"Ingestion failed: {str(e)}")

            return {

                'status': 'error',

                'error_message': str(e),

                'execution_time': (datetime.now() - start_time).total_seconds()

            }

        # END SOLUTION CODE

        # ____________________________________

    

    def _get_last_extraction_timestamp(self) -> Optional[str]:

        """Get timestamp of last successful extraction"""

        timestamp_file = os.path.join(self.config.config['output_directory'], '.last_extraction')

        

        try:

            if os.path.exists(timestamp_file):

                with open(timestamp_file, 'r') as f:

                    return f.read().strip()

        except Exception as e:

            logger.warning(f"Could not read last extraction timestamp: {e}")

        

        return None

    

    def _update_last_extraction_timestamp(self, timestamp: str) -> None:

        """Update timestamp of last successful extraction"""

        timestamp_file = os.path.join(self.config.config['output_directory'], '.last_extraction')

        

        try:

            os.makedirs(os.path.dirname(timestamp_file), exist_ok=True)

            with open(timestamp_file, 'w') as f:

                f.write(timestamp)

        except Exception as e:

            logger.warning(f"Could not update last extraction timestamp: {e}")

# Example usage and testing

if __name__ == "__main__":

    config = IngestionConfig('development')

    ingestion = OrderIngestion(config)

    

    # Run ingestion

    result = ingestion.run_ingestion()

    print(f"Ingestion result: {result}")

