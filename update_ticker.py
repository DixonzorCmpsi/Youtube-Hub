import time
import json
import os
import re
import random
import urllib.parse
import subprocess
from datetime import datetime, timezone, timedelta
import feedparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Prefer undetected_chromedriver if installed
try:
    import undetected_chromedriver as uc
except Exception:
    uc = None

# ==========================================
#  CONFIGURATION
# ==========================================
DATA_DIR = "news_data"  # Renamed from bovada_data
TICKER_OUTPUT_FILE = "ticker_data.js"
HEADLINE_OUTPUT_FILE = "headline_data.js"

# EXPANDED MEDIA SOURCES (NFL, CFB, NBA, GENERAL)
RSS_FEEDS = [
    # --- NFL ---
    {"url": "https://www.espn.com/espn/rss/nfl/news", "source": "ESPN NFL"},
    {"url": "https://sports.yahoo.com/nfl/rss/", "source": "Yahoo NFL"},
    {"url": "https://profootballtalk.nbcsports.com/feed/", "source": "PFT"},
    {"url": "https://rssfeeds.usatoday.com/UsatodaycomNfl-TopStories", "source": "USA Today"},
    {"url": "https://www.si.com/.rss/full/nfl", "source": "Sports Illustrated"},
    {"url": "https://api.foxsports.com/v2/content/optimized-rss?partnerKey=MB0WEEF40Key&size=30&tags=fs/nfl", "source": "FOX Sports"},

    # --- COLLEGE FOOTBALL (CFB) ---
    {"url": "https://www.espn.com/espn/rss/ncf/news", "source": "ESPN CFB"},
    {"url": "https://www.cbssports.com/rss/headlines/college-football/", "source": "CBS CFB"},
    {"url": "https://247sports.com/Season/2024-Football/Headlines/Feed", "source": "247Sports"},

    # --- NBA / GENERAL ---
    {"url": "https://www.espn.com/espn/rss/nba/news", "source": "ESPN NBA"},
    {"url": "https://www.cbssports.com/rss/headlines/nba/", "source": "CBS NBA"},
]

# Full NFL team names for team-specific searches
TEAM_NAMES = [
    "Arizona Cardinals", "Atlanta Falcons", "Baltimore Ravens", "Buffalo Bills",
    "Carolina Panthers", "Chicago Bears", "Cincinnati Bengals", "Cleveland Browns",
    "Dallas Cowboys", "Denver Broncos", "Detroit Lions", "Green Bay Packers",
    "Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Kansas City Chiefs",
    "Las Vegas Raiders", "Los Angeles Chargers", "Los Angeles Rams", "Miami Dolphins",
    "Minnesota Vikings", "New England Patriots", "New Orleans Saints", "New York Giants",
    "New York Jets", "Philadelphia Eagles", "Pittsburgh Steelers", "San Francisco 49ers",
    "Seattle Seahawks", "Tampa Bay Buccaneers", "Tennessee Titans", "Washington Commanders"
]

# TWITTER HANDLES (Insiders & Breakers)
TWITTER_HANDLES = [
    "AdamSchefter", "RapSheet", "Jay_Glazer", "JFowlerESPN", 
    "NFL_DovKleiman", "FieldYates", "MelKiperESPN", "DanOrlovsky",
    "nflnetwork", "BR_NFL", "NextGenStats", "PFF", "MikeFlorio",
    "ShamsCharania", "wojespn", # Added NBA Insiders
    "BruceFeldmanCFB", "McMurphyESPN" # Added CFB Insiders
]

# Diagnostics
FORCE_UC = True
FORCE_PROFILE = True
REMOVE_FLAGS_ON_RETRY = True
DIAGNOSTIC_LOG = "scraper.log"

if not os.path.exists(DATA_DIR): os.makedirs(DATA_DIR)

# ==========================================
#  ENGINE A: BROWSER SETUP (Persistent)
# ==========================================
def setup_driver():
    options = Options()
    
    # 1. PROFILE PATH (Critical for Twitter Login)
    user_profile = os.environ.get("USERPROFILE")
    if user_profile:
        user_data_dir = os.path.join(user_profile, "AppData", "Local", "Google", "Chrome", "User Data")
    else:
        user_data_dir = r"C:\Users\dixon\AppData\Local\Google\Chrome\User Data"

    profile_added = False
    if os.path.exists(user_data_dir):
        options.add_argument(f"user-data-dir={user_data_dir}")
        options.add_argument("profile-directory=Default")
        profile_added = True
    else:
        print(f"[warning] Chrome Profile not found at {user_data_dir}")

    # 2. STABILITY SETTINGS
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # 3. DRIVER INITIALIZATION
    try:
        def try_uc(chrome_options):
            try: return uc.Chrome(options=chrome_options)
            except OSError as oe: 
                if getattr(oe, 'winerror', None) == 17: return None
                raise

        if FORCE_UC and uc is not None:
            ucdrv = try_uc(options)
            if ucdrv: return ucdrv

        print("[info] Starting regular webdriver.Chrome...")
        
        # Version Detection
        def detect_chrome_version():
            possible_paths = [
                os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Google', 'Chrome', 'Application', 'chrome.exe'),
                os.path.join(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'), 'Google', 'Chrome', 'Application', 'chrome.exe'),
            ]
            for p in possible_paths:
                if os.path.exists(p):
                    try:
                        out = subprocess.check_output([p, '--version'], stderr=subprocess.STDOUT, text=True)
                        m = re.search(r"(\d+\.\d+\.\d+\.\d+)", out)
                        if m: return m.group(1)
                    except Exception: continue
            return None

        chrome_ver = detect_chrome_version()
        try:
            if chrome_ver: driver_path = ChromeDriverManager(version=chrome_ver).install()
            else: driver_path = ChromeDriverManager().install()
        except: driver_path = ChromeDriverManager().install()

        service = Service(driver_path)
        return webdriver.Chrome(service=service, options=options)

    except Exception:
        # Retry logic without profile if failed
        if profile_added:
            print("[info] Retry: launching without profile arguments...")
            options2 = Options()
            if not REMOVE_FLAGS_ON_RETRY:
                options2.add_argument("--no-sandbox")
                options2.add_argument("--disable-gpu")
            
            try:
                driver_path2 = ChromeDriverManager().install()
                return webdriver.Chrome(service=Service(driver_path2), options=options2)
            except: raise
        raise

# ==========================================
#  ENGINE B: TWITTER SCRAPER
# ==========================================
def scrape_twitter_news(driver):
    print("--- 🐦 SCRAPING TWITTER (X) ---")
    headlines = []
    now_utc = datetime.now(timezone.utc)
    max_age = timedelta(days=2) # Only last 48 hours
    
    for handle in TWITTER_HANDLES:
        try:
            url = f"https://twitter.com/{handle}"
            print(f"    Checking @{handle}...")
            driver.get(url)
            time.sleep(4)
            driver.execute_script("window.scrollBy(0, 700);")
            time.sleep(2)

            articles = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")
            
            for article in articles[:3]: # Top 3 per handle
                try:
                    # Time Check
                    try:
                        time_el = article.find_element(By.CSS_SELECTOR, "time")
                        dt_str = time_el.get_attribute("datetime")
                        if dt_str:
                            tweet_dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
                            if (now_utc - tweet_dt) > max_age: continue
                    except: pass

                    # Text Extraction
                    text_element = article.find_element(By.CSS_SELECTOR, "div[data-testid='tweetText']")
                    tweet_text = text_element.text
                    if not tweet_text or tweet_text.startswith("@"): continue

                    # Image/Video Extraction
                    img_url = None
                    try:
                        photos = article.find_elements(By.CSS_SELECTOR, "div[data-testid='tweetPhoto'] img")
                        if photos: img_url = photos[0].get_attribute("src")
                    except: pass
                    
                    if not img_url:
                        try:
                            videos = article.find_elements(By.CSS_SELECTOR, "div[data-testid='videoPlayer'] video")
                            if videos: img_url = videos[0].get_attribute("poster")
                        except: pass

                    # Fallback Image
                    if not img_url:
                        query = urllib.parse.quote(f"{handle} {tweet_text[:15]} NFL NBA")
                        img_url = f"https://tse2.mm.bing.net/th?q={query}&w=500&h=800&c=7&rs=1&p=0"

                    # DUAL SUMMARIES
                    # Short (180 chars) for Ticker/Single Host
                    summary_short = tweet_text[:180] + "..." if len(tweet_text) > 180 else tweet_text
                    # Long (600 chars) for Chat Panel
                    summary_long = tweet_text[:600] + "..." if len(tweet_text) > 600 else tweet_text

                    headlines.append({
                        "source": f"@{handle}",
                        "title": tweet_text[:90] + "..." if len(tweet_text) > 90 else tweet_text,
                        "image": img_url,
                        "summary": summary_short,
                        "summary_long": summary_long
                    })
                except Exception: continue
        except Exception: pass
            
    return headlines

# ==========================================
#  ENGINE C: RSS NEWS (Multi-Sport)
# ==========================================
def fetch_rss_news():
    print("--- 📰 FETCHING RSS (NFL, CFB, NBA) ---")
    headlines = []
    for feed in RSS_FEEDS:
        try:
            d = feedparser.parse(feed["url"])
            for entry in d.entries[:4]: # Top 4 per feed
                title = entry.title
                
                # Get raw summary
                raw_summary = entry.summary if 'summary' in entry else title
                clean_text = re.sub('<[^<]+?>', '', raw_summary).strip()
                
                # Dual Summaries
                summary_short = clean_text[:180] + "..." if len(clean_text) > 180 else clean_text
                summary_long = clean_text[:600] + "..." if len(clean_text) > 600 else clean_text

                # Image Logic
                img_url = None
                if 'media_content' in entry: img_url = entry.media_content[0]['url']
                if not img_url:
                    # Smart query based on source
                    sport_tag = "College Football" if "CFB" in feed['source'] else "NFL"
                    query = urllib.parse.quote(f"{title} {sport_tag}")
                    img_url = f"https://tse2.mm.bing.net/th?q={query}&w=500&h=800&c=7&rs=1&p=0"

                headlines.append({
                    "source": feed['source'],
                    "title": title,
                    "image": img_url,
                    "summary": summary_short,
                    "summary_long": summary_long
                })
        except: pass
    return headlines


def fetch_team_news():
    print("--- 🔎 FETCHING TEAM-SPECIFIC NEWS (Google News RSS) ---")
    headlines = []
    for team in TEAM_NAMES:
        try:
            query = urllib.parse.quote(f"{team} NFL")
            url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
            d = feedparser.parse(url)
            for entry in d.entries[:3]:  # Top 3 per team
                try:
                    title = entry.title
                    raw_summary = entry.summary if 'summary' in entry else title
                    clean_text = re.sub('<[^<]+?>', '', raw_summary).strip()

                    summary_short = clean_text[:250] + "..." if len(clean_text) > 250 else clean_text
                    summary_long = clean_text[:600] + "..." if len(clean_text) > 600 else clean_text

                    img_url = None
                    if 'media_content' in entry: img_url = entry.media_content[0].get('url')
                    if not img_url:
                        q = urllib.parse.quote(f"{title} {team}")
                        img_url = f"https://tse2.mm.bing.net/th?q={q}&w=500&h=800&c=7&rs=1&p=0"

                    headlines.append({
                        "source": f"Team: {team}",
                        "title": title,
                        "image": img_url,
                        "summary": summary_short,
                        "summary_long": summary_long
                    })
                except: 
                    continue
        except: 
            continue
    return headlines

# ==========================================
#  MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    driver = setup_driver()
    
    # 1. Scrape Sources
    twitter_news = scrape_twitter_news(driver)
    rss_news = fetch_rss_news()
    team_news = fetch_team_news()
    
    driver.quit()

    # 2. Combine Data
    all_headlines = twitter_news + rss_news + team_news
    random.shuffle(all_headlines)
    
    # 3. Generate Ticker (Breaking News Only)
    # Since we removed games, the ticker is now purely breaking news flow
    ticker_items = [{"type": "NEWS", "text": h["source"], "detail": h["title"]} for h in all_headlines]

    # 4. Save Files
    with open(HEADLINE_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"const headlineData = {json.dumps(all_headlines, indent=4)};\n")
    
    with open(TICKER_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"const tickerData = {json.dumps(ticker_items, indent=4)};\n")

    print(f"✅ DONE. {len(all_headlines)} Stories gathered.")
    print(f"   - Twitter: {len(twitter_news)}")
    print(f"   - RSS (general): {len(rss_news)}")
    print(f"   - Team-specific: {len(team_news)}")