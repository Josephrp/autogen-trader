# autogen-trader
AutoQuant is an AI-agent driven hedge fund that executes swift trades using the latest financial news for maximum investment yield.

## requirements
miniconda: https://docs.conda.io/projects/miniconda/en/latest/

## environment setup
1. setup environment
```sh
conda env create --name autoquant-env --file=environments.yml
```
2. activate environment
```sh
conda activate autoquant-env
```
3. make a copy on .env.example and rename it to env
4. get the following api keys and fill out the .env file
   - https://www.marketaux.com/
     - MARKETAUX_API_TOKEN 
   - https://alpaca.markets/
     - ALPACA_API_KEY
     - ALPACA_API_SECRET
   - https://www.openai.com
     - 

## run autoquant
1. open autoquant.py.
2. change your message at line 186
   ```python
     await user_proxy.a_initiate_chat(manager, message="Do research on MSFT, AAPL and AMZN to determine how to action on the trades it today")
   ```
3. open terminal and run the following command:
   ```sh
     python autoquant.py
   ```
