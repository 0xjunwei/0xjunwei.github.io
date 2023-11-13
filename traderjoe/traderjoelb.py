import requests
import pandas as pd

API_KEY = "5BUJZtczatTaFCxChjv6NTqz1mF3Kc0bwpLu"
chain = "arbitrum"
user_address = "0xC7fF86b58e62F217178990d5021e9998b93A9674"


def get_claimable_rewards():
    market = "0x60563686ca7b668e4a2d7d31448e5f10456ecaf8"
    URL = f"https://api.traderjoexyz.dev/v1/rewards/claimable/{chain}/{user_address}?market={market}"
    print(URL)
    headers = {
        'x-traderjoe-api-key': API_KEY
    }
    # Send a GET request to the URL
    response = requests.get(URL, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()

        # Create a DataFrame from the JSON data
        df = pd.DataFrame(data)
        
        # Display the DataFrame as a table
        print(df)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(response.json())


def get_vaults():
    URL = f"https://api.traderjoexyz.dev/v1/vaults/{chain}"
    print(URL)
    headers = {
        'x-traderjoe-api-key': API_KEY
    }
    # Send a GET request to the URL
    response = requests.get(URL, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()

        # Create a DataFrame from the JSON data
        df = pd.DataFrame(data)
        
        # Display the DataFrame as a table
        print(df)
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(response.json())


def get_vault_rewards(vaultAddress):
    URL = f"https://api.traderjoexyz.dev/v1/vaults/{chain}/{vaultAddress}"
    headers = {
        'x-traderjoe-api-key': API_KEY
    }
    # Send a GET request to the URL
    response = requests.get(URL, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()
        rewarder = data['farm']['rewarder']

        df = pd.DataFrame([rewarder])
        
        # Display the DataFrame as a table
        #print(df)
        return rewarder
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(response.json())


def get_user_vault_position(vaultAddress):
    URL = f"https://api.traderjoexyz.dev/v1/user/{chain}/{user_address}/farms/{vaultAddress}"
    headers = {
        'x-traderjoe-api-key': API_KEY
    }
    # Send a GET request to the URL
    response = requests.get(URL, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()
        return data["userPositionUsd"]
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(response.json())


def get_vault_tvl_and_fees(vaultAddress):
    URL = f"https://api.traderjoexyz.dev/v1/vaults/{chain}/{vaultAddress}"
    headers = {
        'x-traderjoe-api-key': API_KEY
    }
    # Send a GET request to the URL
    response = requests.get(URL, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()
        return data["tvlUsd"], data['feesUsd']
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(response.json())

if __name__ == "__main__":
    eth_usdc_apt = "0x5fb31318e9a82efcaa2cfefbacf63e85f4dff2f1"
    user_position = get_user_vault_position(eth_usdc_apt)
    tvl, fee = get_vault_tvl_and_fees(eth_usdc_apt)
    print("TVL: ", tvl, " , Fee: ", fee, " , user_pos: ", user_position)
    fees_from_user = (user_position/tvl) * fee
    print("Fee earned by user = ", fees_from_user)
    # retrieve fees per day
    management_fee_per_day = (user_position * (4.5 / 100)) / 365
    actual_fee_earned = fees_from_user - management_fee_per_day
    print("Management fee per day: ", management_fee_per_day)
    print("Actual Fee earned: ", actual_fee_earned)
    rewarder = get_vault_rewards(eth_usdc_apt)
    arb_apr = rewarder["rewarderApr1d"]
    est_arb_per_day = (user_position * arb_apr) / 365
    print("Est ARB $ Reward per day: ", est_arb_per_day)
