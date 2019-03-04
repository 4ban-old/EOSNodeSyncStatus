# EOSNodeSyncStatus
A tool for checking the status of EOS nodes. Originally for checking the sync status

<img width="711" alt="screen shot 2019-03-03 at 9 50 18 pm" src="https://user-images.githubusercontent.com/2269864/53707914-fac96180-3dfe-11e9-8bf1-06ee72d7e3d1.png">

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
STANDARD_NODE=https://api.eostitan.com
```
Then tun the tool by command: `python3 app.py`
