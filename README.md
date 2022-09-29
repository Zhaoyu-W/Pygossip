<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#folder-structure">Folder Structure</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
Pygossip is a `pull` model gossip protocol. This protocol will periodically select
a random live member from its knowledge, and try to set up a TCP/IP connection to the selected
node to attempt a gossip.

Pygossip key features:
* Maintained the live member table
* Maintained blacklist blocking failure nodes
* Gossip to a random member selected from table every 3 seconds
* Supported adversarial gossiping

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Folder Structure
```sh
├── README.md
├── communication
│   ├── __init__.py
│   ├── connection.py
│   ├── sender.py
│   └── server.py
├── controller
│   ├── __init__.py
│   ├── adversarial_controller.py
│   └── server_controller.py
├── gossip_main.py
└── util
    ├── __init__.py
    ├── constants.py
    └── gossip_msg.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage
1. Clone the repo
   ```sh
   git clone https://github.com/Zhaoyu-W/Pygossip
   ```
2. Run the main script
   ```sh
   python3 gossip_main.py {ip_address} {tcp_port} {initial_state}
   ```
3. Command input
   ```sh
    !: list all the connections in csv format
       e.g:
        128.84.213.13:5678,1630281124,1
        128.84.213.43:9876,1630282312,7
    ?: list all the connections in identifier --> state format
       e.g:
        128.84.213.13:5678 --> 1
        128.84.213.43:9876 --> 7
    +{ip_address}:{tcp_port}: connect to new node
    [0-9]: change the server state
    Y: turn on adversarial gossip
    N: turn off adversarial gossip
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact
Zhaoyu Wang - [@Zhaoyu_W](https://twitter.com/Zhaoyu_W) - zhaoyu.wang1999@gmail.com
Project Link: [ https://github.com/Zhaoyu-W/Pygossip]( https://github.com/Zhaoyu-W/Pygossip)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
