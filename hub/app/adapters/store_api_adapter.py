import logging
from typing import List


import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]) -> bool:
        """
        Make a POST request to the Store API endpoint with the processed data
        """
        if not isinstance(processed_agent_data_batch, list):
            logging.error("Processed agent data batch should be a list")
            return False

        try:
            response = requests.post(f"{self.api_base_url}/processed_agent_data/",
                                     json=[item.dict() for item in processed_agent_data_batch])
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Data not saved: {e}")
            return False

        return response.status_code == requests.codes.ok