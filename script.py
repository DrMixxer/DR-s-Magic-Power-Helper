import requests

def get_all_ah_data(api_key):
    url = 'https://api.hypixel.net/skyblock/auctions'
    page = 0
    all_auctions = []

    try:
        while True:
            response = requests.get(url, params={'key': api_key, 'page': page})
            response.raise_for_status()
            data = response.json()

            all_auctions.extend(data['auctions'])
            print(f"Fetched page {page + 1}/{data['totalPages']}")

            if page >= data['totalPages'] - 1:
                break

            page += 1

        return all_auctions
    except requests.exceptions.RequestException as e:
        print(f"Error fetching AH data: {e}")
        return None

def get_talisman_prices(auctions):
    talismans = {}
    for auction in auctions:
        if 'talisman' in auction['item_name'].lower() and auction.get('bin', False):
            item_name = auction['item_name']
            price = auction['starting_bid']
            if item_name not in talismans or price < talismans[item_name]:
                talismans[item_name] = price
    return talismans

def main():
    try:
        username = input("Username: ")
        profile = input("Profile: ")
        budget = float(input("Budget (in millions): ")) * 1_000_000
        current_mp = int(input("Current MP: "))
        mp_goal = int(input("MP Goal (total MP you want to achieve): "))

        additional_mp_needed = mp_goal - current_mp

        api_key = 'YOUR_HYPIXEL_API_KEY'  # Replace with your Hypixel API key
        auctions = get_all_ah_data(api_key)
        if not auctions:
            print("Failed to retrieve AH data. Please try again later.")
            input("Press Enter to exit...")
            return

        talismans = get_talisman_prices(auctions)

        sorted_talismans = sorted(talismans.items(), key=lambda x: x[1])

        print(f"Recommended talismans for {username} with a budget of {budget / 1_000_000}M to achieve an additional {additional_mp_needed} MP:")
        total_cost = 0
        total_mp = current_mp
        for name, price in sorted_talismans:
            if total_cost + price <= budget and total_mp < mp_goal:
                total_cost += price
                total_mp += 1  # Assuming each talisman gives 1 MP, adjust this as needed
                print(f"{name}: {price / 1_000_000}M")
            if total_cost >= budget or total_mp >= mp_goal:
                break

        if total_mp >= mp_goal:
            print(f"Success! You have reached your MP goal of {mp_goal}.")
        else:
            print(f"You have reached {total_mp} MP, which is less than your goal of {mp_goal} MP.")
        
        input("Press Enter to exit...")
    except ValueError:
        print("Invalid input. Please enter numbers for budget and MP goal.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
