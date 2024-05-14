from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Users, PlatformData
from .scraper import (
    fetch_codeforces_data,
    fetch_leetcode_data,
    fetch_geeksforgeeks_data,
    fetch_hackerrank_data,
    fetch_codechef_data,
)
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def user_detail(request, user_id):
    try:
        # Fetch user data
        user = Users.objects.get(user_id=user_id)
        return JsonResponse({'user': user.platforms})  # Return user
    except Users.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


@csrf_exempt
@require_POST
def update_scores(request, user_id):
    try:
        print('#' * 50)
        # Fetch user data or return 404 if user not found
        user = get_object_or_404(Users, user_id=user_id)
        platforms = PlatformData.objects.filter(user=user, verification_status='verified_true')

        if request.method == 'POST':
            # Extract data from the request body
            data = request.POST
            try:
                print("Updating scores for user " + user_id)
                # Fetch data from external APIs
                print('-' * 25, 'Codeforces', '-' * 25)
                codeforces_data = fetch_codeforces_data(user.platforms['codeforces']['platform_username'])
                print('-' * 25, 'LeetCode', '-' * 25)
                leetcode_data = fetch_leetcode_data(user.platforms['leetcode']['platform_username'])
                print('-' * 25, 'GeeksforGeeks', '-' * 25)
                geeksforgeeks_data = fetch_geeksforgeeks_data(user.platforms['geeksforgeeks']['platform_username'])
                print('-' * 25, 'HackerRank', '-' * 25)
                hackerrank_data = fetch_hackerrank_data(user.platforms['hackerrank']['platform_username'], user.year_of_passing)
                print('-' * 25, 'CodeChef', '-' * 25)
                codechef_data = fetch_codechef_data(user.platforms['codechef']['platform_username'])

                # Update user's platform data with fetched scores
                for platform in platforms:
                    if platform.platform_name == 'codeforces':
                        platform.score = codeforces_data.get('result', [{}])[0].get('rating')
                    elif platform.platform_name == 'leetcode':
                        platform.score = leetcode_data.get('contestRating', None)
                    elif platform.platform_name == 'geeksforgeeks':
                        platform.score = geeksforgeeks_data.get('info', {}).get('codingScore', None)
                    elif platform.platform_name == 'hackerrank':
                        platform.score = hackerrank_data
                    elif platform.platform_name == 'codechef':
                        platform.score = codechef_data
                    platform.save()

                return JsonResponse({'success': True})

            except Exception as e:
                # Handle any errors that occur during fetching or updating
                return JsonResponse({'success': False, 'error': str(e)})

    except Users.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)


def fetch_platform_score(request, user_id, platform):
    try:
        # Fetch user data or return 404 if user not found
        user = get_object_or_404(Users, user_id=user_id)
        platform_data = PlatformData.objects.filter(user=user, platform_name=platform, verification_status='verified_true').first()

        if platform_data:
            # Fetch score for the specified platform
            score = None
            if platform == 'codeforces':
                score = fetch_codeforces_data(platform_data.platform_username)['result'][0]['rating']
            elif platform == 'leetcode':
                score = int(fetch_leetcode_data(platform_data.platform_username)['contestRating'])
            elif platform == 'geeksforgeeks':
                score = fetch_geeksforgeeks_data(platform_data.platform_username)['info']['codingScore']
            elif platform == 'hackerrank':
                score = fetch_hackerrank_data(platform_data.platform_username, user.year_of_passing)
            elif platform == 'codechef':
                score = fetch_codechef_data(platform_data.platform_username)

            return JsonResponse({'platform': platform, 'platform_username': platform_data.platform_username, 'score': score})
        else:
            return JsonResponse({'error': 'Platform data not found or not verified'}, status=404)
    except Users.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
