import requests
import logging
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from retrying import retry
from typing import Any, Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class IndianMFApi:
    """
    A class to interact with the Mutual Fund API to retrieve mutual fund information.
    """

    def __init__(self):
        """
        Initializes the MFApi instance and retrieves the list of mutual funds.
        """
        self.mutual_fund_list = self.get_mf_list()
        self.fund_code_map = self.create_fund_code_map(self.mutual_fund_list)

    @retry(stop_max_attempt_number=3, wait_fixed=2000, retry_on_exception=lambda x: isinstance(x, HTTPError) and x.response.status_code in {502, 503, 504})
    def __parse_response(self, url: str) -> Any:
        """
        Sends a GET request to the specified URL and returns the JSON response.

        Args:
            url (str): The URL to send the GET request to.

        Returns:
            Any: The JSON response from the server.

        Raises:
            HTTPError: An HTTP error occurred.
            ConnectionError: A network problem occurred.
            Timeout: The request timed out.
            RequestException: A request error occurred.
        """
        try:
            response = requests.get(url, verify=False, timeout=10)
            response.raise_for_status()
            logging.info(f"Successfully fetched data from {url}")
            return response.json()
        except HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            if http_err.response.status_code in {502, 503, 504}:
                logging.info(f"Retrying due to status code: {http_err.response.status_code}")
            raise
        except ConnectionError as conn_err:
            logging.error(f"Connection error occurred: {conn_err}")
            raise
        except Timeout as timeout_err:
            logging.error(f"Timeout error occurred: {timeout_err}")
            raise
        except RequestException as req_err:
            logging.error(f"Request error occurred: {req_err}")
            raise

    def get_mf_list(self) -> List[Dict[str, Any]]:
        """
        Retrieves the list of all mutual funds.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing mutual fund information.
        """
        url = "https://api.mfapi.in/mf"
        return self.__parse_response(url)

    def create_fund_code_map(self, fund_list: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Creates a mapping of fund names to their codes from the mutual fund list.

        Args:
            fund_list (List[Dict[str, Any]]): A list of mutual fund information.

        Returns:
            Dict[str, int]: A dictionary mapping fund names to their codes.
        """
        return {fund['schemeName']: fund['schemeCode'] for fund in fund_list}

    def is_valid_fund_code(self, mf_code: int) -> bool:
        """
        Checks if the provided mutual fund code is valid.

        Args:
            mf_code (int): The mutual fund code to verify.

        Returns:
            bool: True if the fund code is valid, False otherwise.
        """
        return mf_code in self.fund_code_map.values()

    def get_mf_price_latest(self, mf_code: int) -> Dict[str, Any]:
        """
        Retrieves the latest price for a specified mutual fund.

        Args:
            mf_code (int): The mutual fund code.

        Returns:
            Dict[str, Any]: A dictionary containing the latest mutual fund price information.
        """
        if not self.is_valid_fund_code(mf_code):
            logging.error(f"Invalid mutual fund code: {mf_code}")
            return {}
        
        url = f"https://api.mfapi.in/mf/{mf_code}/latest"
        return self.__parse_response(url)
    
    def get_mf_price_hist(self, mf_code: int) -> Dict[str, Any]:
        """
        Retrieves the historical price data for a specified mutual fund.

        Args:
            mf_code (int): The mutual fund code.

        Returns:
            Dict[str, Any]: A dictionary containing the historical mutual fund price information.
        """
        if not self.is_valid_fund_code(mf_code):
            logging.error(f"Invalid mutual fund code: {mf_code}")
            return {}
        
        url = f"https://api.mfapi.in/mf/{mf_code}"
        return self.__parse_response(url)

if __name__ == "__main__":
    mf = IndianMFApi()
    try:
        logging.info("Fetching mutual fund list")
        print(mf.mutual_fund_list)
        
        test_code = 152746  # Replace with the fund code you want to test
        if mf.is_valid_fund_code(test_code):
            logging.info(f"Fetching mutual fund price history for code {test_code}")
            print(mf.get_mf_price_hist(test_code))
            logging.info(f"Fetching latest mutual fund price for code {test_code}")
            print(mf.get_mf_price_latest(test_code))
        else:
            logging.error(f"Invalid mutual fund code: {test_code}")
    except Exception as e:
        logging.error(f"An error occurred during API operations: {e}")
