<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Pygossip is a `pull` model gossip protocol. This protocol will periodically select
a random live member from its map, and try to set up a TCP/IP connection to the selected
node to attempt a gossip.

Pygossip features:
* Maintained latest 3 live members
* Maintained blacklist blocking failure nodes
* Gossip to a random member every 3 seconds
* Supported adversarial gossiping


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage
1. Clone the repo
   ```sh
   git clone https://github.com/Zhaoyu-W/Pygossip
   ```
2. Run main script
   ```sh
   python3 gossip_main.py {ip_address} {tcp_port} {initial_state}
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Zhaoyu Wang - [@Zhaoyu_W](https://twitter.com/Zhaoyu_W) - zhaoyu.wang1999@gmail.com

Project Link: [ https://github.com/Zhaoyu-W/Pygossip]( https://github.com/Zhaoyu-W/Pygossip)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
