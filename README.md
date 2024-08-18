# IndiaFinanceAPI
Internal APIs to enhance Finance Chatbot

## Setup

```bash
sudo apt install git python3 python3-pip python3-setuptools python3-venv
```

## Clone the repo

```bash
git clone git@github.com:xadnavyaai/IndiaFinanceAPI.git
cd IndianFinanceAPI/
```

### ENV setup

```bash
python3 -m venv pyfinmuni
```

### ENV Activate
```bash
source ./pyfinmuni/bin/activate # Same dir where you created venv
```

### Installation of lib

```bash
python3 -m pip install -e .
```

## Installation with Tests

```bash
python3 -m pip install -e .[dev] # To install test dependencies
```

### Run tests

```bash
python3 -m pytest tests/
```

#### Tests Output

```bash
=================================================== test session starts ===================================================
platform linux -- Python 3.12.3, pytest-8.3.2, pluggy-1.5.0
rootdir: /home/ubuntu/IndiaFinanceAPI
plugins: requests-mock-1.12.1
collected 16 items                                                                                                        

tests/test_IMFApi.py .......                                                                                        [ 43%]
tests/test_NSEApi.py .........                                                                                      [100%]

==================================================== warnings summary =====================================================
tests/test_IMFApi.py::test_get_mf_list
tests/test_IMFApi.py::test_create_fund_code_map
tests/test_IMFApi.py::test_is_valid_fund_code
tests/test_IMFApi.py::test_get_mf_price_latest
tests/test_IMFApi.py::test_get_mf_price_latest_invalid_code
tests/test_IMFApi.py::test_get_mf_price_hist
tests/test_IMFApi.py::test_get_mf_price_hist_invalid_code
  /home/ubuntu/venvs/finapi/lib/python3.12/site-packages/urllib3/connectionpool.py:1099: InsecureRequestWarning: Unverified HTTPS request is being made to host 'api.mfapi.in'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================= 16 passed, 7 warnings in 9.11s ==============================================
```

## Usage

### NSEApi
```python3
from pyfinmuni import NSEApi

nse = NSEApi()
print(nse.get_stock_codes())
print(nse.get_top_gainers())
print(nse.get_top_losers())
print(nse.get_all_indices())
print(nse.get_quote("RELIANCE"))
print(nse.get_historical_data("RELIANCE", "07-06-2024", "07-07-2024"))
```

### IndianMFApi

```python3
from pyfinmuni import IndianMFApi

mfapi = IndianMFApi()

print(mf.mutual_fund_list)

test_code = 152746  # Replace with the fund code you want to test

if mf.is_valid_fund_code(test_code):
    print(mf.get_mf_price_hist(test_code))
    print(mf.get_mf_price_latest(test_code))

```

### MF Fund Utils for name matching with ML embeddings

```python3
os.environ["mf_embeddings_path"] = "<Path to MF name embeddings numpy file!>"
from pyfinmuni.utils import mf_fund_utils

query_fund_name = "SBI Bluechip Fund"
top_matches = mf_fund_utils.find_top_fund_matches(query_fund_name)

query_fund_name = "Principal Emerging Bluechip Fund - Growth Option"
top_matches = mf_fund_utils.find_top_fund_matches(query_fund_name)
```