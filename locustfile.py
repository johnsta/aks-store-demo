import os
import uuid
import logging
from locust import HttpUser, task, between
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ApiUser(HttpUser):
    wait_time = between(1, 3)
    host = os.getenv("HOST", "http://20.105.36.20")  # Default host from HTTP Request File
    timeout_duration = 90  # Timeout for all requests
    DEBUG_MODE = os.getenv("DEBUG_MODE", "True") == "True"

    @task
    def run_scenario(self):
        """Run the sequence of operations as defined in the HTTP Request File."""
        self.list_all_products()
        self.get_product_by_id()

    def list_all_products(self):
        """List all products."""
        url = f"{self.host}/products"
        headers = {
            "Accept": "application/json"
        }

        with self.client.get(
            url,
            headers=headers,
            name="List all products",
            catch_response=True,
            timeout=self.timeout_duration
        ) as response:
            if response.status_code == 200:
                response.success()
                if self.DEBUG_MODE:
                    logging.info("Successfully listed all products.")
            else:
                response.failure(f"Failed to list all products. Status: {response.status_code}, Response: {response.text}")
                if self.DEBUG_MODE:
                    logging.error(f"Request URL: {response.url}, Headers: {headers}")

    def get_product_by_id(self):
        """Get a single product by ID."""
        product_id = 1  # Static ID as per HTTP Request File
        url = f"{self.host}/products/{product_id}"
        headers = {
            "Accept": "application/json"
        }

        with self.client.get(
            url,
            headers=headers,
            name="Get product by ID",
            catch_response=True,
            timeout=self.timeout_duration
        ) as response:
            if response.status_code == 200:
                response.success()
                if self.DEBUG_MODE:
                    logging.info(f"Successfully retrieved product with ID {product_id}.")
            else:
                response.failure(f"Failed to retrieve product with ID {product_id}. Status: {response.status_code}, Response: {response.text}")
                if self.DEBUG_MODE:
                    logging.error(f"Request URL: {response.url}, Headers: {headers}")

    def on_stop(self):
        """Clean up resources if necessary."""
        if self.DEBUG_MODE:
            logging.info("Test completed. No resources to clean up.")