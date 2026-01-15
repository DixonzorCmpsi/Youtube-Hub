import os

# --- 1. THE SCHEDULE DATA ---
# Edit this to update scores or winners live.
# To show a result: change "winner": None  ->  "winner": "BUF" (or team code)
schedule = [
    {
        "date": "SAT JAN 10",
        "time": "4:30 PM",
        "away": "LAR", "home": "CAR",  # Rams vs Panthers
        "winner": None 
    },
    {
        "date": "SAT JAN 10",
        "time": "8:00 PM",
        "away": "GB", "home": "CHI",   # Packers vs Bears
        "winner": None
    },
    {
        "date": "SUN JAN 11",
        "time": "1:00 PM",
        "away": "BUF", "home": "JAX",  # Bills vs Jaguars
        "winner": None
    },
    {
        "date": "SUN JAN 11",
        "time": "4:30 PM",
        "away": "SF", "home": "PHI",   # 49ers vs Eagles
        "winner": None
    },
    {
        "date": "SUN JAN 11",
        "time": "8:00 PM",
        "away": "LAC", "home": "NE",   # Chargers vs Patriots
        "winner": None
    },
    {
        "date": "MON JAN 12",
        "time": "8:00 PM",
        "away": "HOU", "home": "PIT",  # Texans vs Steelers
        "winner": None
    }
]

# NFL Team Config (Colors & Names)
teams = {
    "BUF": {"color": "#00338D", "name": "Bills"},
    "MIA": {"color": "#008E97", "name": "Dolphins"},
    "NE":  {"color": "#002244", "name": "Patriots"},
    "NYJ": {"color": "#125740", "name": "Jets"},
    "BAL": {"color": "#241773", "name": "Ravens"},
    "CIN": {"color": "#FB4F14", "name": "Bengals"},
    "CLE": {"color": "#311D00", "name": "Browns"},
    "PIT": {"color": "#FFB612", "name": "Steelers"},
    "HOU": {"color": "#03202F", "name": "Texans"},
    "IND": {"color": "#002C5F", "name": "Colts"},
    "JAX": {"color": "#006778", "name": "Jags"},
    "TEN": {"color": "#4B92DB", "name": "Titans"},
    "DEN": {"color": "#FB4F14", "name": "Broncos"},
    "KC":  {"color": "#E31837", "name": "Chiefs"},
    "LV":  {"color": "#000000", "name": "Raiders"},
    "LAC": {"color": "#0080C6", "name": "Chargers"},
    "DAL": {"color": "#003594", "name": "Cowboys"},
    "NYG": {"color": "#002244", "name": "Giants"},
    "PHI": {"color": "#004C54", "name": "Eagles"},
    "WAS": {"color": "#5A1414", "name": "Commanders"},
    "CHI": {"color": "#0B162A", "name": "Bears"},
    "DET": {"color": "#0076B6", "name": "Lions"},
    "GB":  {"color": "#203731", "name": "Packers"},
    "MIN": {"color": "#4F2683", "name": "Vikings"},
    "ATL": {"color": "#a71930", "name": "Falcons"},
    "CAR": {"color": "#0085CA", "name": "Panthers"},
    "NO":  {"color": "#D3BC8D", "name": "Saints"},
    "TB":  {"color": "#D50A0A", "name": "Bucs"},
    "ARI": {"color": "#97233F", "name": "Cardinals"},
    "LAR": {"color": "#003594", "name": "Rams"},
    "SF":  {"color": "#AA0000", "name": "49ers"},
    "SEA": {"color": "#002244", "name": "Seahawks"},
}

# --- 2. GENERATE SCHEDULE ROWS HTML ---
def generate_rows(schedule_data):
    rows_html = ""
    for game in schedule_data:
        h_team = teams.get(game['home'], {"color": "#444", "name": game['home']})
        a_team = teams.get(game['away'], {"color": "#444", "name": game['away']})
        
        # Logic for Checks/X's
        h_status = ""
        a_status = ""
        if game['winner']:
            if game['winner'] == game['home']:
                h_status = '<div class="status-icon win">✔</div>'
                a_status = '<div class="status-icon lose">✘</div>'
            elif game['winner'] == game['away']:
                h_status = '<div class="status-icon lose">✘</div>'
                a_status = '<div class="status-icon win">✔</div>'

        rows_html += f"""
            <div class="row match-row">
                <div class="match-time">
                    <span class="m-day">{game['date']}</span>
                    <span class="m-clock">{game['time']}</span>
                </div>
                
                <div class="battle-container">
                    <div class="team-wrapper">
                        {a_status}
                        <div class="team-logo" style="background: {a_team['color']}">{game['away']}</div>
                    </div>

                    <div class="vs-divider">@</div>

                    <div class="team-wrapper">
                        <div class="team-logo" style="background: {h_team['color']}">{game['home']}</div>
                        {h_status}
                    </div>
                </div>
            </div>
        """
    return rows_html

# --- 3. THE FULL HTML TEMPLATE ---
def create_hud():
    rows_content = generate_rows(schedule)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DeeTalk - Ultimate Broadcast HUD</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@800&display=swap');

        :root {{
            --brand-purple: #4c1d95; 
            --brand-purple-light: #7c3aed;
            --neon-cyan: #06b6d4; 
            --neon-green: #10b981; 
            --lose-red: #ef4444;
            --text-white: #ffffff;
            --dark-bg: rgba(15, 23, 42, 0.98);
        }}

        body {{
            margin: 0; padding: 0; width: 1920px; height: 1080px; overflow: hidden;
            background: transparent;
            font-family: 'Rajdhani', sans-serif;
        }}

        /* --- THE MEGA BORDER FRAME --- */
        .broadcast-frame {{
            position: absolute; 
            top: 0; left: 0; width: 1920px; height: 1080px;
            box-sizing: border-box;
            border: 18px solid var(--brand-purple); /* Thick border */
            pointer-events: none; /* Lets you click through to video below */
            z-index: 999; /* On top of everything */
            
            /* Inner Glow and Bottom Accent like reference */
            box-shadow: inset 0 0 40px rgba(0,0,0,0.8), 0 0 20px rgba(124, 58, 237, 0.5);
        }}
        .broadcast-frame::after {{
            content: ''; position: absolute;
            bottom: 0; left: 0; width: 100%; height: 8px;
            background: linear-gradient(90deg, var(--brand-purple), var(--neon-cyan), var(--brand-purple));
        }}

        /* --- UTILITIES --- */
        .skew-box {{ transform: skewX(-10deg); }}
        .unskew-text {{ transform: skewX(10deg); display: inline-block; }}

        /* --- 1. TOP LEFT LOGO (DEETALK) --- */
        .top-left-logo {{
            position: absolute; top: 50px; left: 50px; /* Pushed in for border */
            display: flex; align-items: center; gap: 10px;
        }}
        .logo-box {{
            background: linear-gradient(90deg, #2e1065, #5b21b6);
            padding: 12px 35px;
            border-left: 6px solid var(--neon-cyan);
            color: white; font-weight: 900; font-size: 28px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            clip-path: polygon(0 0, 100% 0, 95% 100%, 0% 100%);
        }}
        .sub-count {{
            background: var(--neon-cyan); color: #0f172a;
            padding: 10px 18px; font-weight: 800; font-size: 22px;
            clip-path: polygon(10% 0, 100% 0, 90% 100%, 0% 100%);
        }}

        /* --- 2. SIDEBAR SCHEDULE (SUPER SIZED) --- */
        .sidebar-table {{
            position: absolute; top: 50px; right: 50px; /* Pushed in */
            width: 500px; /* MUCH WIDER for broadcast impact */
            background: var(--dark-bg);
            color: white;
            border-top: 8px solid var(--neon-cyan);
            box-shadow: -10px 10px 40px rgba(0,0,0,0.8);
            border-bottom-left-radius: 12px;
        }}
        .table-header {{
            background: linear-gradient(90deg, var(--neon-cyan), #3b82f6);
            padding: 18px; text-align: center;
        }}
        .table-header h2 {{ margin: 0; font-family: 'Montserrat', sans-serif; font-size: 32px; text-transform: uppercase; color: #0f172a; }}
        .table-header p {{ margin: 0; font-size: 16px; font-weight: 700; opacity: 0.8; color: #0f172a;}}

        /* Schedule Specific Styles (BIGGER & CLOSER) */
        .match-row {{
            display: flex; align-items: center; justify-content: space-between;
            padding: 18px 25px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .match-row:nth-child(even) {{ background: rgba(255,255,255,0.03); }}
        
        .match-time {{
            display: flex; flex-direction: column;
            width: 80px; text-align: center;
            font-size: 15px; opacity: 0.9;
            border-right: 1px solid rgba(255,255,255,0.2);
            padding-right: 20px; margin-right: 20px;
        }}
        .m-day {{ font-weight: 800; color: var(--neon-cyan); line-height: 1.1; margin-bottom:2px; }}
        .m-clock {{ font-weight: 600; }}

        /* --- BATTLE CONTAINER (TIGHT CLOSE ICONS) --- */
        .battle-container {{
            display: flex; align-items: center; 
            flex-grow: 1; justify-content: center;
            gap: 15px; /* Close proximity battle like reference */
        }}
        
        .team-wrapper {{ position: relative; display: flex; align-items: center; justify-content: center; }}

        .team-logo {{
            width: 70px; height: 70px; /* SUPER SIZED ICONS */
            display: flex; justify-content: center; align-items: center;
            font-weight: 900; font-size: 24px; color: white;
            border-radius: 10px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.6);
            border: 3px solid rgba(255,255,255,0.15);
            text-shadow: 2px 2px 4px black;
            z-index: 2;
        }}

        .vs-divider {{ font-size: 16px; opacity: 0.5; font-weight: 900; }}
        
        .status-icon {{ 
            position: absolute; top: -10px; right: -10px;
            font-size: 32px; font-weight: 900; text-shadow: 0 0 10px rgba(0,0,0,1);
            z-index: 10;
        }}
        .win {{ color: var(--neon-green); }}
        .lose {{ color: var(--lose-red); opacity: 0.9; }}

        /* --- 3. LOWER THIRD ASSEMBLY --- */
        .lower-third-container {{
            position: absolute; bottom: 50px; left: 50px; /* Pushed in */
            display: flex; align-items: flex-end; width: 100%;
        }}
        
        /* Date Box (10 JAN LIVE) */
        .date-box {{
            width: 110px; height: 110px;
            background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%);
            color: white; border-top: 5px solid var(--brand-purple-light);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            margin-right: 15px; box-shadow: 0 0 20px rgba(76, 29, 149, 0.5);
        }}
        .date-big {{ font-size: 48px; font-weight: 900; line-height: 1; }}
        .date-small {{ font-size: 18px; font-weight: 700; color: var(--neon-cyan); }}

        .main-content-stack {{ display: flex; flex-direction: column; width: 850px; }}
        
        /* Headline (PLAYOFFS WILDCARD TA) */
        .headline-bar {{
            background: linear-gradient(90deg, #172554 0%, #1e3a8a 100%);
            padding: 18px 35px; border-left: 10px solid var(--brand-purple-light);
            display: flex; align-items: center; height: 70px;
        }}
        .headline-text {{
            color: white; font-family: 'Montserrat', sans-serif;
            font-size: 46px; font-weight: 900; text-transform: uppercase;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5); letter-spacing: 1px;
        }}
        
        /* Ticker */
        .ticker-bar {{
            background: #0f172a; height: 40px;
            display: flex; align-items: center; margin-top: 4px;
            overflow: hidden; position: relative;
        }}
        .ticker-label {{
            background: var(--brand-purple-light); color: white;
            padding: 0 20px; height: 100%; display: flex; align-items: center;
            font-weight: 800; font-size: 16px; z-index: 2;
        }}
        .ticker-marquee {{
            white-space: nowrap; color: #cbd5e1; font-weight: 600; font-size: 20px;
            padding-left: 20px; animation: scroll-left 20s linear infinite;
        }}
        @keyframes scroll-left {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

        /* Socials (DEETALK TV) */
        .socials-box {{
            background: linear-gradient(135deg, #2e1065, #0f172a);
            height: 114px; width: 220px; margin-left: 15px;
            border-bottom: 5px solid var(--neon-cyan);
            display: flex; flex-direction: column; justify-content: center; align-items: center; color: white;
        }}
        .social-handle {{ font-size: 22px; font-weight: 700; display: flex; align-items: center; gap: 8px; }}

        /* --- 4. BOTTOM RIGHT POLL --- */
        .poll-box {{
            position: absolute; bottom: 50px; right: 50px;
            width: 450px; height: 150px;
            background: linear-gradient(135deg, #0f172a, #1e1b4b);
            border-right: 10px solid var(--neon-cyan);
            display: flex;
        }}
        .poll-icon-area {{
            width: 90px; background: var(--neon-cyan);
            display: flex; justify-content: center; align-items: center;
            font-size: 50px; color: #0f172a; font-weight: 900;
        }}
        .poll-content {{
            flex-grow: 1; padding: 25px;
            display: flex; justify-content: center; align-items: center; text-align: center;
        }}
        .poll-text {{
            color: white; font-family: 'Montserrat', sans-serif;
            font-size: 28px; font-weight: 800; text-transform: uppercase;
            line-height: 1.2;
        }}
    </style>
</head>
<body>

    <div class="broadcast-frame"></div>

    <div class="top-left-logo">
        <div class="logo-box">DEETALK</div>
        <div class="sub-count">8.1k ✔</div>
    </div>

    <div class="sidebar-table">
        <div class="table-header">
            <h2>Wild Card Weekend</h2>
            <p>Road to the Super Bowl</p>
        </div>
        <div class="table-rows">
            {rows_content}
        </div>
    </div>

    <div class="lower-third-container">
        
        <div class="date-box">
            <span class="date-big">10</span>
            <span class="date-small">JAN</span>
            <span class="date-small" style="margin-top:5px; font-size:12px;">LIVE</span>
        </div>

        <div class="main-content-stack">
            <div class="headline-bar skew-box">
            <span class="headline-text unskew-text">PLAYOFFS WILDCARD TA</span>
            </div>
            <div class="ticker-bar skew-box">
                <div class="ticker-label unskew-text">LATEST</div>
                <div class="ticker-marquee unskew-text">
                    Welcome to DeeTalk • breaking NFL Wild Card Weekend news • Subscribe for daily updates • Join our discord for fantasy football tips • 
                </div>
            </div>
        </div>

        <div class="socials-box skew-box">
            <div class="unskew-text">
                <div class="social-handle" style="margin-bottom: 5px; color: var(--neon-cyan);">DEETALK TV</div>
                <div class="social-handle" style="font-size: 14px; opacity: 0.8;">X / IG / YT</div>
            </div>
        </div>

    </div>

    <div class="poll-box">
        <div class="poll-icon-area">?</div>
        <div class="poll-content">
            <span class="poll-text">WHO WILL GO THROUGH?</span>
        </div>
    </div>

</body>
</html>
"""
    
    # Write the unified HUD
    with open("hud.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("SUCCESS: hud.html updated with Mega Border, Bigger Icons, and Full 'DeeTalk' preserved layout.")

if __name__ == "__main__":
    create_hud()