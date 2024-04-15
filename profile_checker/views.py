from django.shortcuts import render

# Create your views here.
# profile_checker/views.py
from django.http import JsonResponse, HttpResponseNotFound
import requests
from bs4 import BeautifulSoup


def construct_url(platform, username):
    if platform == "hackerrank":
        return f"https://www.hackerrank.com/profile/{username}/"
    elif platform == "codechef":
        return f"https://www.codechef.com/users/{username}/"
    elif platform == "codeforces":
        return f"https://codeforces.com/profile/{username}/"
    elif platform == "geeksforgeeks":
        return f"https://auth.geeksforgeeks.org/user/{username}/"
    else:
        return None


def check_geeksforgeeks_exists(url):
    header = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/121.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=header)
        return response.url != "https://auth.geeksforgeeks.org/?to=https://auth.geeksforgeeks.org/profile.php"
    except requests.exceptions.RequestException:
        print("RequestException")
        return False


def check_codeforces_exists(url):
    try:
        response = requests.get(url)
        return response.url != "https://codeforces.com/"
    except requests.exceptions.RequestException:
        return False


def check_codechef_exists(url):
    try:
        response = requests.get(url)
        return response.url != "https://www.codechef.com/"
    except requests.exceptions.RequestException:
        return False


def check_hackerrank_exists(url):
    header = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/121.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string
        return not ("Programming Problems and Competitions :: HackerRank" in title or title == " HackerRank ")
    except requests.exceptions.RequestException:
        return False


def check_url_platform(request):
    platform = request.GET.get('platform', '')
    username = request.GET.get('username', '')

    if not platform or not username:
        return JsonResponse({'error': 'Platform or username not provided'}, status=400)

    url = construct_url(platform, username)

    if not url:
        return JsonResponse({'error': 'Invalid platform'}, status=400)

    if platform == "hackerrank":
        exists = check_hackerrank_exists(url)
    elif platform == "codechef":
        exists = check_codechef_exists(url)
    elif platform == "codeforces":
        exists = check_codeforces_exists(url)
    elif platform == "geeksforgeeks":
        exists = check_geeksforgeeks_exists(url)
    else:
        return JsonResponse({'error': 'Invalid platform'}, status=400)

    if exists:
        return JsonResponse({'exists': True, 'url': url})
    else:
        return HttpResponseNotFound('Profile not found', status=404)
