# This project

- Python API to analyze NTFS driver differences through Black-box testing 
- Implements a proof-of-concept detection technique given the fingerprints

## Installation
- Install VirtualBox
- Install VirtualBox CLI
- Install VirtualBox guest additions on the guest machine
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages.
```bash
pip install -r requirements.txt
```
- Install [TSK](https://www.sleuthkit.org/)
- Install [dfir_ntfs](https://github.com/msuhanov/dfir_ntfs): 
```bash
pip3 install https://github.com/msuhanov/dfir_ntfs/archive/1.1.18.tar.gz
```


## Run (unit & integration) tests

```bash
cd src
python3 -m pytest test
```

## Usage (black-box testing)

```bash
python3 -m experiment.py
```

## Usage (fingerprint detection)

```bash
python3 -m detect.py
```

## Troubleshooting
- If Virtualbox machines fail to start, shut down other virtualization software (e.g. Docker)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
