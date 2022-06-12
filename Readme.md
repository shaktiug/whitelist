<!-- GETTING STARTED -->
## Getting Started with "Whitelistyourself" tool

These are the instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

Things you need to use the software and how to install them.
* Python 3
  https://www.python.org/downloads/

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/shaktiug/whitelist
   ```

2. Cd to the script directory
   ```sh
   cd devops\python-scripts\whitelist_yourself
   ```

3. Set env variables for windows in cmd
   ```sh
   setx CLIENT_ID ""
   setx CLIENT_SECRET ""
  
   Reopen the CMD or run "refreshenv" to refresh the env variables"
   ```

4. Set env variables for mac
   ```sh
   export CLIENT_ID="" >> ~/.zshrc
   export CLIENT_SECRET="" >> ~/.zshrc

   source ~/.zshrc
   ```

5. Install python packages
   ```sh
   pip3 install -r requirements.txt
   ```
6. Execute the script
   ```python
   python whitelist_yourself.py --env dev --name <your-first-name-only>
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

