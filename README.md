# Cosmos Hub(4) mainnet Ansible role

This repo includes Ansible role that deploys the full Cosmos hub 4 mainnet node. It fetches the binaries from Cosmos Github repo instead of compiling it locally or remotely on the target server. 

However, it also checks the sha256 hashes of the binaries and also sha1 of the genesis.json file for an extra security reasons. 

All variables can be found in `roles/cosmos/defaults/defaults.yml` including the checksums(which I kept there just for testing purposes, they are being fetched with `get_url` module instead directly from the [Cosmos mainnet repo](https://github.com/cosmos/mainnet)) 

The Cosmos role follows the [Quickstart](https://github.com/cosmos/mainnet#quickstart) from Cosmos README.md, where for a fresh node it is **first needed** to run the *gaiad-v4.2.0* and **wait until** it **PANICs** and then **swap** the **binaries** for *gaiad-v5.0.2*. 
Rest of the instructions from the README.md are also followed - for example the changes in `config.toml`.

Make sure you change the **moniker** and **password** in `defaults.yml`.

For this role to work properly, you should use `--tags` and `--skip-tags` simply because I haven't found a way how to automate the binary swap (it takes just way too long to sync the node and I did not have time neither storage for that).

You may find the tags with some brief description in the next section.

**NOTE:** This role does extensive checks so it would not overwrite any of your critical files, including the binary swapping - which does not proceed if the process is still running but nevertheless I am not responsible for any damage done to your node. 

## Using this role (complete deployment of Cosmos mainnet hub 4 node)

### Prerequisites:

- Python 3.6+
- pip
- Ansible 2.10+ (tested with Ansible 2.11.2 but it should work on earlier versions as well.)

#### Install ansible & dependencies:

    `pip install -r requirements.txt`

#### Add the IP of the remote server to the inventory:

    `echo 1.2.3.4 > config/inventory.ini` 

#### Run your playbook:

    `bin/provision --list-tags --list-tasks`

### Tags:
Some tags are duplicate or non-essential, it is a bit chaotic still, so use with caution until I manage to find some time to improve this repo. 
You can find the main tags in `tasks/main.yml` but here is also a brief description what each tag does(or should do).

#### to see all tasks and tags in detail, please run the main playbook like this:
`bin/provision --list-tasks --list-tag`
```
download: needed to download binaries and checksums as well as creating gaia user and group. 
  additional tags for download:
    bin_swap - moves the v5.0.2 binaries from /tmp to /usr/local/bin
    binaries - same as the bin_swap (but used in the tasks/main.yml)
    checksums - parses the release notes for checksums 
fresh_node:
  full init, adding admin user account, using moniker and password from default.yml file,  config edits and p2p seeds, genesis file downlaod. 
  
  additional tags for fresh_node:
    create_admin - add admin user
    genesis_download - downlaod, unzip genesis to target config dir and check shasum
init: edits config and adds admin user
  additional tags:
    config_edit - edits config.toml according to the Cosmos mainnet README.md
    
run: installs systemd service script and starts gaiad
service_check: checks if systemd gaiad.service works
logging: installs the python monitoring script and runs it as a systemd service
```
## Basic monitoring script to get the latest_block_height
Simple monitoring script in Python that retrieves the latest block height from local json-rcp endpoint (pst, [check this out](https://docs.tendermint.com/master/rpc/)) and reports it as a gauge to the local StatsD server (UDP 8125) every 10 seconds. 

For it to work in the current state of the repo, you will need to have StatsD server on the machine preinstalled or you can uncomment the task from the `tasks/main.yml` or you can use `--skip-tags "logging"` 
