# EOSNodeSyncStatus
A tool for checking the status of EOS nodes. Originally for checking the sync status

<img width="660" alt="Screen Shot 2019-03-24 at 2 12 20 PM" src="https://user-images.githubusercontent.com/2269864/54883705-e6491980-4e3e-11e9-8f60-5041e987c1e2.png">

## Installation
For running this tool you have to use `Python3` and `requests` module.
```python
pip3 install requests
```

## Usage
Config file has the following parameters:
```bash
# The timeout for checking node
TIMEOUT=10
# The pause between requests
PAUSE=5
# The main node
MAIN_NODE=http://35.183.49.71:8888
# Standard node for checking with
STANDARD_NODE=https://api.eostitan.com,https://rpc.eosys.io,https://api.main.alohaeos.com:443,https://api.cypherglass.com:443
```
Then tun the tool by command: `python3 app.py`
