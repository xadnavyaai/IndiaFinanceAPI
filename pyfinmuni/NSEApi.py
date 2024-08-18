import re
import six
import ast
import json
import requests
import logging

from abc import ABCMeta, abstractmethod
from typing import Optional, Dict, Union
from datetime import datetime as dt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AbstractBaseExchange(six.with_metaclass(ABCMeta, object)):

    @abstractmethod
    def get_stock_codes(self):
        """
        :return: list of tuples with stock code and stock name
        """
        raise NotImplementedError

    @abstractmethod
    def is_valid_code(self, code):
        """
        :return: True, if it is a valid stock code, else False
        """
        raise NotImplementedError

    @abstractmethod
    def get_quote(self, code):
        """
        :param code: a stock code
        :return: a dictionary which contain detailed stock code.
        """
        raise NotImplementedError

    @abstractmethod
    def get_top_gainers(self):
        """
        :return: a sorted list of codes of top gainers
        """
        raise NotImplementedError

    @abstractmethod
    def get_top_losers(self):
        """
        :return: a sorted list of codes of top losers
        """
        raise NotImplementedError

    @abstractmethod
    def __str__(self):
        """
        :return: market name
        """
        raise NotImplementedError


class NSEApi(AbstractBaseExchange):
    """
    Class that implements functionality for the National Stock Exchange
    """
    __CODECACHE__ = None

    def __init__(self, verify: bool = True, session_refresh_interval: int = 300):
        # URLs
        self.session_refresh_interval = session_refresh_interval 
        self.nse_home_url = "https://nseindia.com"
        self.session = self.create_session(verify=verify)

        self.historical_data_url = "https://www.nseindia.com/api/historical/cm/equity?symbol={code}&series=[%22EQ%22]&from={from_date}&to={to_date}&json=true"
        self.get_quote_url = "https://www.nseindia.com/api/quote-equity?symbol={code}"
        self.stocks_csv_url = 'https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv'
        self.top_gainer_url = 'https://www.nseindia.com/api/live-analysis-variations?index=gainers&type=NIFTY&json=true'
        self.top_loser_url = 'https://www.nseindia.com/api/live-analysis-variations?index=loosers&type=NIFTY&json=true'
        self.all_indices_url = "https://www.nseindia.com/api/allIndices?json=true"

    def create_session(self, verify=True):
        self._session = requests.Session()
        self._session.verify = verify
        self._session.headers.update(self.nse_headers())
        try:
            self._session.get(self.nse_home_url)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error creating session: {e}")
            raise
        self._session_init_time = dt.now()
        return self._session

    def fetch(self, url):
        time_diff = dt.now() - self._session_init_time
        if time_diff.seconds < self.session_refresh_interval:
            try:
                return self._session.get(url)
            except requests.exceptions.RequestException as e:
                logging.error(f"Error fetching URL {url}: {e}")
                raise
        else:
            self.create_session(self._session.verify)
            return self.fetch(url)

    def __fetch_json(self, url):
        try:
            res = self.session.get(url)
            res.raise_for_status()
            data = res.json()
            return self.render_response(data)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching JSON data from URL {url}: {e}")
            return {}

    def get_top_gainers(self) -> Dict:
        return self.__fetch_json(self.top_gainer_url)

    def get_top_losers(self) -> Dict:
        return self.__fetch_json(self.top_loser_url)

    def get_all_indices(self) -> Dict:
        return self.__fetch_json(self.all_indices_url)
    
    def get_stock_codes(self) -> Dict:
        url = self.stocks_csv_url
        res_dict = {}
        try:
            res = self.session.get(url)
            res.raise_for_status()
            data = res.text
            for line in data.split('\n'):
                if line and re.search(',', line):
                    code, name = line.split(',')[0:2]
                    res_dict[code] = name
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching stock codes: {e}")
        return self.render_response(res_dict, True)

    def get_historical_data(self, code, from_date, to_date):
        """
        Gets historical data for a given stock code
        :param code: stock code
        :param from_date: start date in dd-mm-yyyy format
        :param to_date: end date in dd-mm-yyyy format
        :return: dict
        :raises: HTTPError
        """
        url = self.historical_data_url.format(code=code, from_date=from_date, to_date=to_date)
        try:
            res = self.fetch(url)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching historical data for {code}: {e}")
            return {}

    def get_quote(self, code, all_data=False):
        """
        Gets the quote for a given stock code
        :param code: stock code
        :return: dict or None
        :raises: HTTPError
        """
        code = code.upper()
        try:
            res = self.fetch(self.get_quote_url.format(code=code))
            res.raise_for_status()
            return res.json()['priceInfo'] if not all_data else res.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching quote for {code}: {e}")
            return {}

    def is_valid_code(self, code):
        """
        Validates if a given stock code is valid
        :param code: a string stock code
        :return: Boolean
        """
        if code:
            stock_codes = self.get_stock_codes()
            return code.upper() in stock_codes.keys()
        return False
    
    def get_index_list(self):
        """ 
        Get list of indices and codes
        :returns: a list | json of index codes
        """
        try:
            return [i['indexSymbol'] for i in self.get_all_indices()]
        except Exception as e:
            logging.error(f"Error fetching index list: {e}")
            return []

    def get_index_quote(self, code):
        """
        Get quote for a given index code
        :param code: string index code
        :returns: dict
        """
        try:
            all_index_quote = self.get_all_indices()
            index_list = [i['indexSymbol'] for i in all_index_quote]
            code = code.upper()
            if code in index_list:
                return list(filter(lambda idx: idx['indexSymbol'] == code, all_index_quote))[0]
            else:
                logging.error('Wrong index code')
                return {}
        except Exception as e:
            logging.error(f"Error fetching index quote for {code}: {e}")
            return {}

    def nse_headers(self):
        """
        Builds the right set of headers for requesting http://nseindia.com
        :return: a dict with http headers
        """
        return {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

    def render_response(self, data: dict, as_json=True) -> Union[str, Dict]:
        return json.dumps(data) if as_json else data

    def __str__(self) -> str:
        """
        String representation of object
        :return: string
        """
        return 'Driver Class for National Stock Exchange (NSE)'

if __name__ == "__main__":
    nse = NSEApi()
    print(nse.get_stock_codes())
    print(nse.get_top_gainers())
    print(nse.get_top_losers())
    print(nse.get_all_indices())
    print(nse.get_quote("RELIANCE"))
    print(nse.get_historical_data("RELIANCE", "07-06-2024", "07-07-2024"))
