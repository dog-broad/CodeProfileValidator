import requests
from .scrap import Scrap
from .models import SearchTokens


def fetch_codeforces_data(username):
    print('Fetching Codeforces data for', username, '...')
    try:
        response = requests.get(f'https://codeforces.com/api/user.info?handles={username}&checkHistoricHandles=false')
        response.raise_for_status()
        data = response.json()
        print(data)
        return data
    except requests.RequestException as e:
        print('Error fetching Codeforces data:', e)
        return None


def fetch_leetcode_data(username):
    print('Fetching LeetCode data for', username, '...')
    try:
        response = requests.get(f'https://alfa-leetcode-api.onrender.com/{username}/contest')
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print('Error fetching LeetCode data:', e)
        return None


def fetch_geeksforgeeks_data(username):
    print('Fetching GeeksforGeeks data for', username, '...')
    try:
        scraper = Scrap(username)
        data = scraper.fetchResponse()
        print(data)
        return data
    except requests.RequestException as e:
        print('Error fetching GeeksforGeeks data:', e)
        return None


def fetch_hackerrank_data(username, year_of_passing):
    print('Fetching HackerRank data for', username, '...')
    try:
        # Implement logic to fetch HackerRank data
        # Fetch the HackerRank urls' data with year_of_passing
        url_tokens = SearchTokens.objects.filter(year_of_passing=year_of_passing).values_list('urls', flat=True)
        print(url_tokens)
        score = 0
        for url_token in url_tokens[0]:
            print("Fetching HackerRank data for year " + str(year_of_passing) + " and URL token " + url_token)
            for i in range(0, 10000, 100):
                try:
                    print("Fetching HackerRank data for offset " + str(i))
                    url = "https://www.hackerrank.com/rest/contests/" + url_token + "/leaderboard?offset=" + str(
                        i) + "&limit=100"
                    # Set headers to avoid 403 error
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    data = response.json()
                    # Find the user's score if it exists
                    if data['models'] is None or data['models'] == []:
                        break
                    for item in data['models']:
                        # convert the username to lowercase to avoid case sensitivity
                        item['hacker'] = item['hacker'].lower()
                        # check if the username matches
                        if item['hacker'] == username:
                            score += item['score']
                            break
                    print(data)
                    print("Score for " + username + " so far is " + str(score))
                except requests.RequestException as e:
                    print('Error fetching HackerRank data:', e)
                    break
        print(score)
        return round(score)
    except Exception as e:
        print('Error fetching HackerRank data:', e)
        return None


def fetch_codechef_data(username):
    print('Fetching CodeChef data for', username, '...')
    try:
        response = requests.get(f'https://codechef-api.vercel.app/{username}')
        response.raise_for_status()
        data = response.json()
        return round(data['currentRating'])
    except requests.RequestException as e:
        print('Error fetching CodeChef data:', e)
        return None
