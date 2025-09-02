import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import urllib.parse
import random
import argparse
import asyncio
import aiohttp
from bs4 import BeautifulSoup

TextColors = {
    "RED" : '\033[91m',
    "DARK_RED": '\033[31m',
    "GREEN" :'\033[92m',
    "DARK_GREEN": '\033[32m',
    "MINT" :'\033[96m',
    "OLIVE" : '\033[33m',
    "DARK_BLUE" : '\033[34m',
    "CYAN" : '\033[36m',
    "PURPLE" : '\033[35m',
    "DARK_PURPLE" : '\033[95m',
    "WHITE" : '\033[97m',
}
random_color = random.choice(list(TextColors.values()))

BANNER = r"""
 __   __         _____                    ___             
 \ \ / /__  _   |_   _| __ __ _  ___ ___ / _ \ _ __   ___ 
  \ V / _ \| | | || || '__/ _` |/ __/ _ \ | | | '_ \ / _ \
   | | (_) | |_| || || | | (_| | (_|  __/ |_| | | | |  __/
   |_|\___/ \__,_||_||_|  \__,_|\___\___|\___/|_| |_|\___|
                                                          
"""

PLATFORMS = [
    {
        'name': 'Instagram',
        'url': 'https://www.instagram.com/{username}/',
        'check_method': 'html',
        'exists_code': 200,
        'not_exists_code': 200,
        'error_text': "The link you followed may be broken" 
    },
    {
        'name': 'GitHub',
        'url': 'https://api.github.com/users/{username}',
        'check_method': 'status',
        'exists_code': 200,
        'not_exists_code': 404,
        'error_text': None
    },
    {
        'name': 'Reddit',
        'url': 'https://www.reddit.com/user/{username}',
        'check_method': 'html',  
        'exists_code': 200,
        'not_exists_code': 200,
        'error_text': "Sorry, nobody on Reddit goes by that name"
    },
    {
        'name': 'Facebook',
        'url': 'https://www.facebook.com/{username}',
        'check_method': 'html',
        'exists_code': 200,
        'not_exists_code': 200,
        'error_text': "This content isn't available right now" 
    },
    {
        'name': 'LinkedIn',
        'url': 'https://www.linkedin.com/in/{username}',
        'check_method': 'status', 
        'exists_code': 200,
        'not_exists_code': 404,
        'error_text': "This page doesn't exist"  
    },
    {
        'name': 'YouTube',
        'url': 'https://www.youtube.com/@{username}',
        'check_method': 'html',
        'exists_code': 200,
        'not_exists_code': 200,
        'error_text': "404 Not Found"
    },
    {
        'name': 'Pinterest',
        'url': 'https://www.pinterest.com/{username}/',
        'check_method': 'html',
        'exists_code': 200,
        'not_exists_code': 200,
        'error_text': "Couldn't find this account"
    }
]

async def check_platform(session, platform, username):
    url = platform['url'].format(username=username)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        async with session.get(url, headers=headers, timeout=10) as response:
            if platform['check_method'] == 'status':
                return {
                    'platform': platform['name'],
                    'url': url,
                    'exists': response.status == platform['exists_code'],
                    'status': response.status
                }
            elif platform['check_method'] == 'html':
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                exists = platform.get('error_text') not in text
                return {
                    'platform': platform['name'],
                    'url': url,
                    'exists': exists,
                    'status': response.status
                }
    except Exception as e:
        return {
            'platform': platform['name'],
            'url': url,
            'exists': False,
            'error': str(e)
        }

async def search_username(username):
    async with aiohttp.ClientSession() as session:
        tasks = [check_platform(session, platform, username) for platform in PLATFORMS]
        results = await asyncio.gather(*tasks)
        return {res['platform']: res for res in results if res['exists']}

def phone_lookup(number: str):
    try:
        parsed = phonenumbers.parse(number, None)
        if not phonenumbers.is_valid_number(parsed):
            return {f"{TextColors["DARK_RED"]}Phone Input Error": "Not a valid number."}

        region_code = phonenumbers.region_code_for_number(parsed)
        formatted_number = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        encoded_number = urllib.parse.quote(f"\"{formatted_number}\"")
        national_format = urllib.parse.quote(f"\"{phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)}\"")
    
        dorks = {
            "Exact Match": f"https://www.google.com/search?q={encoded_number}",
            "Site Search (Facebook)": f"https://www.google.com/search?q=site:facebook.com+{encoded_number}",
            "Documents (PDF/DOC)": f"https://www.google.com/search?q=filetype:pdf+OR+filetype:doc+{encoded_number}",
            "Country Domain Search": f"https://www.google.com/search?q=site:.{region_code}+{encoded_number}+OR+{national_format}"
        }

        return {
            "Input number": number,
            "National_format": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
            "Region code": region_code,
            "Carrier": carrier.name_for_number(parsed, "en"),
            "Timezone": timezone.time_zones_for_number(parsed),
            "Google Dorks": dorks
        }
    except:
        return {f"{TextColors["DARK_RED"]}error": f"Check Input"}

parser = argparse.ArgumentParser(description="Simple OSINT tool for phone numbers and usernames.")
parser.add_argument('--phone', help='Phone number to lookup (with +countrycode)')
parser.add_argument('--username', help='Username to search across platforms')

args = parser.parse_args()

if __name__ == "__main__":
    print(f"{random_color}{BANNER}{TextColors['WHITE']}")
    
    ran_something = False
    
    if args.username:
        print(f"\n{TextColors["DARK_PURPLE"]}[+] Username OSINT for '{args.username}':{TextColors['WHITE']}")
        user = asyncio.run(search_username(args.username))
        if user:
            print(f"{TextColors['GREEN']}Found on:{TextColors["WHITE"]}")
            for platform, info in user.items():
                print(f"- {platform}: {info['url']}")
        else:
            print(f"{TextColors["DARK_RED"]}Not found on any checked platforms.{TextColors['WHITE']}")
        ran_something = True
    
    if args.phone:
        results = phone_lookup(args.phone)
        print(f"\n{TextColors["DARK_PURPLE"]}[+] Phone OSINT:{TextColors['WHITE']}")
        for k, v in results.items():
            if k == "Google Dorks":
                print(f"\n{TextColors["DARK_PURPLE"]}[+] Phone Google Dorks:{TextColors['WHITE']}")
                for name, url in v.items():
                    print(f" - {name}: {url}")
            else:
                print(f"{k}: {v}")
        ran_something = True
    
    if not ran_something:
        parser.print_help()