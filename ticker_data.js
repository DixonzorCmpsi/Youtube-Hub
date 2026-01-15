const tickerData = [
    {
        "type": "NEWS",
        "text": "Team: Los Angeles Rams",
        "detail": "Rams have better OL than the Greatest Show on Turf - Turf Show Times"
    },
    {
        "type": "NEWS",
        "text": "CBS CFB",
        "detail": "Miami vs. Ole Miss prediction, pick, spread, odds: Hurricanes, Rebels meet in Fiesta Bowl CFP semifinal"
    },
    {
        "type": "NEWS",
        "text": "Team: Tennessee Titans",
        "detail": "Jaguars clinch AFC South title with win over Titans - NFL.com"
    },
    {
        "type": "NEWS",
        "text": "Team: New Orleans Saints",
        "detail": "With Week 18 over, the New Orleans Saints' 2026 NFL Draft slot is set - Saints Wire"
    },
    {
        "type": "NEWS",
        "text": "Team: San Francisco 49ers",
        "detail": "49ers Opponents Set for the 2026 Season - 49ers.com"
    },
    {
        "type": "NEWS",
        "text": "Team: Atlanta Falcons",
        "detail": "Falcons rework Cousins deal, set up key decision - ESPN"
    },
    {
        "type": "NEWS",
        "text": "Team: Atlanta Falcons",
        "detail": "REPORT: Falcons restructure Kirk Cousins' contract - Atlanta Falcons"
    },
    {
        "type": "NEWS",
        "text": "Team: San Francisco 49ers",
        "detail": "49ers' full list of 2026 opponents confirmed - Niner Noise"
    },
    {
        "type": "NEWS",
        "text": "Team: Miami Dolphins",
        "detail": "Tua Tagovailoa says fresh start from Dolphins following midseason benching would be 'dope' - NFL.com"
    },
    {
        "type": "NEWS",
        "text": "Team: Minnesota Vikings",
        "detail": "Vikings updated 2026 NFL Draft order: Current 1st-round pick after Week 18 - Daily Norseman"
    },
    {
        "type": "NEWS",
        "text": "Team: Detroit Lions",
        "detail": "Lions fire offensive coordinator John Morton after one season - NFL.com"
    },
    {
        "type": "NEWS",
        "text": "Team: Tampa Bay Buccaneers",
        "detail": "Tampa Bay Buccaneers opponents 2026: Who\u2019s on the schedule, how easy or hard will their schedule be - SB Nation"
    },
    {
        "type": "NEWS",
        "text": "Team: Cincinnati Bengals",
        "detail": "Cincinnati Bengals\u2019 spot in 2026 NFL Draft order finalized - Cincy Jungle"
    },
    {
        "type": "NEWS",
        "text": "PFT",
        "detail": "Report: Falcons request to interview Lions COO Mike Disner for president of football ops"
    },
    {
        "type": "NEWS",
        "text": "Team: Philadelphia Eagles",
        "detail": "5 reasons for optimism and concern as Eagles enter playoffs - NBC Sports Philadelphia"
    },
    {
        "type": "NEWS",
        "text": "Team: Las Vegas Raiders",
        "detail": "Tom Brady\u2019s Latest Hail Mary: Saving the Raiders - The Wall Street Journal"
    },
    {
        "type": "NEWS",
        "text": "Team: Cincinnati Bengals",
        "detail": "2026 NFL Offseason Important Dates To Know - Bengals.com"
    },
    {
        "type": "NEWS",
        "text": "PFT",
        "detail": "NFL coaches, GMs fired: Black Monday live tracker, latest news, rumors and updates from PFT"
    },
    {
        "type": "NEWS",
        "text": "Team: Green Bay Packers",
        "detail": "Latest NFL coaching twist might quietly save Jeff Hafley for Packers - Lombardi Ave"
    },
    {
        "type": "NEWS",
        "text": "Team: Cleveland Browns",
        "detail": "Browns rally for walk-off win, but enter offseason of QB uncertainty after another shaky Shedeur Sanders performance vs. Bengals - Yahoo Sports"
    },
    {
        "type": "NEWS",
        "text": "Team: Kansas City Chiefs",
        "detail": "Chiefs Terminate Contract After Missing NFL Playoffs - Athlon Sports"
    },
    {
        "type": "NEWS",
        "text": "Team: Arizona Cardinals",
        "detail": "Mock draft roundup: Experts express mixed view on Cardinals and No. 3 overall pick - Arizona Sports"
    },
    {
        "type": "NEWS",
        "text": "CBS NBA",
        "detail": "Use DraftKings promo code to get $300 in bonus bets by targeting Louisville-Duke, Cavaliers-Pacers on Tuesday"
    },
    {
        "type": "NEWS",
        "text": "Team: Seattle Seahawks",
        "detail": "Why Schlereth could see Seahawks pulling off repeat of Super Bowl 48 - Seattle Sports"
    },
    {
        "type": "NEWS",
        "text": "Team: Arizona Cardinals",
        "detail": "Cardinals\u2019 firing of Jonathan Gannon says more about them than the head coach - The Athletic - The New York Times"
    },
    {
        "type": "NEWS",
        "text": "Team: Los Angeles Chargers",
        "detail": "Chargers open up as betting favorites ahead of Week 6 vs. Dolphins - Bolts From The Blue"
    },
    {
        "type": "NEWS",
        "text": "Team: Dallas Cowboys",
        "detail": "Cowboys fire DC Matt Eberflus: Top replacement candidates - ESPN"
    },
    {
        "type": "NEWS",
        "text": "CBS CFB",
        "detail": "Texas Tech celebrates signing of QB Brendan Sorsby with Times Square billboard"
    },
    {
        "type": "NEWS",
        "text": "Team: Washington Commanders",
        "detail": "Commanders receive No. 7 overall pick in 2026 NFL Draft - Washington Commanders"
    },
    {
        "type": "NEWS",
        "text": "Team: New York Jets",
        "detail": "2026 NFL Draft Order: Raiders Secure No. 1 Pick, Jets Hold No. 2 Pick - FOX Sports"
    },
    {
        "type": "NEWS",
        "text": "Team: Green Bay Packers",
        "detail": "Matt LaFleur gives updates on Packers\u2019 injuries, playoff practice plans - Acme Packing Company"
    },
    {
        "type": "NEWS",
        "text": "Team: New Orleans Saints",
        "detail": "Saints\u2019 loss locks in their draft pick. See where they\u2019ll pick in the 2026 NFL Draft. - NOLA.com"
    },
    {
        "type": "NEWS",
        "text": "ESPN NBA",
        "detail": "Kings' Murray to miss 3-4 weeks with ankle sprain"
    },
    {
        "type": "NEWS",
        "text": "ESPN NBA",
        "detail": "Cavs without Strus for at least another month"
    },
    {
        "type": "NEWS",
        "text": "Yahoo NFL",
        "detail": "Ravens reportedly fire coach John Harbaugh after missing playoffs, ending 18-year run that included Super Bowl win"
    },
    {
        "type": "NEWS",
        "text": "Team: Jacksonville Jaguars",
        "detail": "Bills vs Jaguars picks, predictions, odds for NFL playoff game Sunday - azcentral.com and The Arizona Republic"
    },
    {
        "type": "NEWS",
        "text": "Team: Jacksonville Jaguars",
        "detail": "Identifying the Jaguars' Most Impactful Rookie - Sports Illustrated"
    },
    {
        "type": "NEWS",
        "text": "Team: Minnesota Vikings",
        "detail": "Minnesota Vikings 2026 NFL Draft Pick Order and Big Board for Top Needs - Bleacher Report"
    },
    {
        "type": "NEWS",
        "text": "Team: Detroit Lions",
        "detail": "Lions NFL mock draft 2026: What experts are saying about first round - Detroit Free Press"
    },
    {
        "type": "NEWS",
        "text": "ESPN NFL",
        "detail": "Harbaugh out as coach of Ravens, sources say"
    },
    {
        "type": "NEWS",
        "text": "Team: Detroit Lions",
        "detail": "2026 NFL offseason calendar: Detroit Lions important dates, deadlines - Pride Of Detroit"
    },
    {
        "type": "NEWS",
        "text": "Team: Baltimore Ravens",
        "detail": "Ravens waste no time making a flurry of signings after end of 2025 NFL season - Ebony Bird"
    },
    {
        "type": "NEWS",
        "text": "Team: Houston Texans",
        "detail": "Who will the Texans face on Monday Night Football in the Wild Card Round? - Houston Texans"
    },
    {
        "type": "NEWS",
        "text": "Team: Washington Commanders",
        "detail": "Commanders part ways with OC Kliff Kingsbury, DC Joe Whitt Jr. after disappointing 2025 - NFL.com"
    },
    {
        "type": "NEWS",
        "text": "Team: Baltimore Ravens",
        "detail": "Ravens vs. Steelers: Pittsburgh rallies past Baltimore to seize AFC North title on dramatic last-second missed kick - Yahoo Sports"
    },
    {
        "type": "NEWS",
        "text": "Team: New England Patriots",
        "detail": "NFL Playoff Picture: Where Patriots Finished In AFC After Week 18 Win - NESN"
    },
    {
        "type": "NEWS",
        "text": "Team: New York Giants",
        "detail": "Giants expected to speak with Kevin Stefanski after his Browns firing - New York Post"
    },
    {
        "type": "NEWS",
        "text": "Team: Minnesota Vikings",
        "detail": "Vikings players who are set to hit free agency or are cut candidates - Sports Illustrated"
    },
    {
        "type": "NEWS",
        "text": "Team: Chicago Bears",
        "detail": "Chicago Bears open practice windows for Kyler Gordon and Braxton Jones, while Rome Odunze nears a return - Chicago Tribune"
    },
    {
        "type": "NEWS",
        "text": "Team: Pittsburgh Steelers",
        "detail": "Steelers earn NFL's final playoff spot after missed Ravens kick - NBC News"
    },
    {
        "type": "NEWS",
        "text": "Team: Buffalo Bills",
        "detail": "Bills\u2019 opponents for 2026 announced - RochesterFirst"
    },
    {
        "type": "NEWS",
        "text": "Team: Miami Dolphins",
        "detail": "Miami Dolphins 2026 General Manager Tracker - Miami Dolphins"
    },
    {
        "type": "NEWS",
        "text": "CBS CFB",
        "detail": "The $1 million running back is here: Jadan Baugh is one symbol of college football's new economy"
    },
    {
        "type": "NEWS",
        "text": "Yahoo NFL",
        "detail": "Report: Falcons request to interview Lions COO Mike Disner for president of football ops"
    },
    {
        "type": "NEWS",
        "text": "Team: Philadelphia Eagles",
        "detail": "Eagles Urged to Make Major Move on Offense Following NFC Shakeup - Heavy Sports"
    },
    {
        "type": "NEWS",
        "text": "Team: Chicago Bears",
        "detail": "NFL Predictions: 4 Picks for Green Bay Packers vs Chicago Bears - Sportsnaut"
    },
    {
        "type": "NEWS",
        "text": "ESPN CFB",
        "detail": "CFP quarterfinal ratings up 14%, overall by 3%"
    },
    {
        "type": "NEWS",
        "text": "Team: Indianapolis Colts",
        "detail": "Texans 38, Colts 30: Houston locks up No. 5 seed in AFC, awaits playoff opponent - Houston Chronicle"
    },
    {
        "type": "NEWS",
        "text": "Team: Carolina Panthers",
        "detail": "Carolina Panthers 2026 opponents are set - Panthers.com"
    },
    {
        "type": "NEWS",
        "text": "Team: Philadelphia Eagles",
        "detail": "Philadelphia Eagles 2026 schedule of opponents: Home, away matchups confirmed - Bleeding Green Nation"
    },
    {
        "type": "NEWS",
        "text": "Team: New Orleans Saints",
        "detail": "New Orleans Saints sign eight players to reserve/future contracts - New Orleans Saints | NewOrleansSaints.com"
    },
    {
        "type": "NEWS",
        "text": "Team: Seattle Seahawks",
        "detail": "2025 NFL playoffs, Super Bowl odds: Seattle Seahawks are Super Bowl 60 favorites heading into playoffs for first time since 2014 - Yahoo Sports"
    },
    {
        "type": "NEWS",
        "text": "Team: Los Angeles Rams",
        "detail": "Rams 21-19 Seahawks (Nov 16, 2025) Final Score - ESPN"
    },
    {
        "type": "NEWS",
        "text": "Team: Las Vegas Raiders",
        "detail": "Inside Raiders' lost 2025 season: Tom Brady's influence, private meetings and dysfunction - ESPN"
    },
    {
        "type": "NEWS",
        "text": "Team: Tennessee Titans",
        "detail": "Interim Coach Mike McCoy Extends One Thank You After Another After Titans Wrap Up 2025 Season - Tennessee Titans"
    },
    {
        "type": "NEWS",
        "text": "Yahoo NFL",
        "detail": "Bills sign K Matthew Wright to practice squad"
    },
    {
        "type": "NEWS",
        "text": "Team: Tennessee Titans",
        "detail": "2026 NFL draft: What is the Tennessee Titans' first-round pick worth? - Titans Wire"
    },
    {
        "type": "NEWS",
        "text": "Team: Tampa Bay Buccaneers",
        "detail": "Todd Bowles believes he's 'earned the chance' to return as Buccaneers coach despite disappointing finish - NFL.com"
    },
    {
        "type": "NEWS",
        "text": "@PFF",
        "detail": "The Ravens are officially parting ways with HC John Harbaugh\n\nBaltimore during the Harbaug..."
    },
    {
        "type": "NEWS",
        "text": "Team: Jacksonville Jaguars",
        "detail": "Jaguars clinch AFC South title with win over Titans - NFL.com"
    },
    {
        "type": "NEWS",
        "text": "Team: Denver Broncos",
        "detail": "Ranking & Grading Broncos' 4 Big Free-Agent Signings of 2025 - Sports Illustrated"
    },
    {
        "type": "NEWS",
        "text": "Team: Cleveland Browns",
        "detail": "Cleveland Browns News and Rumors 1/6/25: At First Glance, Browns Strategy Appears Aimless - 247Sports"
    },
    {
        "type": "NEWS",
        "text": "ESPN NBA",
        "detail": "Best trade fits for 16 contenders -- and two wild-card teams"
    },
    {
        "type": "NEWS",
        "text": "Team: Cincinnati Bengals",
        "detail": "Free agents, NFL Draft & possible changes: Bengals embark on big offseason - WLWT"
    },
    {
        "type": "NEWS",
        "text": "Team: Las Vegas Raiders",
        "detail": "Tom Brady wanted Geno Smith on Raiders over Seahawks QB Sam Darnold - Sports Illustrated"
    },
    {
        "type": "NEWS",
        "text": "Team: Houston Texans",
        "detail": "Houston Texans celebrate first time not playing in Wild Card weekend opener - Awful Announcing"
    },
    {
        "type": "NEWS",
        "text": "Yahoo NFL",
        "detail": "Early 2026 Fantasy Football QB Rankings: Justin Boone's top quarterbacks for next season"
    },
    {
        "type": "NEWS",
        "text": "Team: Los Angeles Chargers",
        "detail": "What makes Chargers\u2019 Justin Herbert the most \u2018mentally tough dude of all time\u2019 - The New York Times"
    },
    {
        "type": "NEWS",
        "text": "@PFF",
        "detail": "The teams with the most pressures this season "
    },
    {
        "type": "NEWS",
        "text": "Team: Los Angeles Rams",
        "detail": "Rams vs Panthers picks, predictions, odds for NFL playoff game Saturday - azcentral.com and The Arizona Republic"
    },
    {
        "type": "NEWS",
        "text": "Team: Chicago Bears",
        "detail": "It\u2019s on to the NFL playoffs: Brad Biggs\u2019 10 thoughts after Chicago Bears backed into the No. 2 seed - Chicago Tribune"
    },
    {
        "type": "NEWS",
        "text": "Team: New England Patriots",
        "detail": "Patriots to host Chargers in NFL wild card playoffs - Pats Pulpit"
    },
    {
        "type": "NEWS",
        "text": "Team: New York Jets",
        "detail": "Who Will the Jets Play in the 2026 NFL Season? - New York Jets"
    },
    {
        "type": "NEWS",
        "text": "Team: Miami Dolphins",
        "detail": "What to Know About the Dolphins' 2026 Strength of Schedule - Sports Illustrated"
    },
    {
        "type": "NEWS",
        "text": "Team: Atlanta Falcons",
        "detail": "NFL news roundup: Falcons QB Kirk Cousins agrees to re-worked contract - NFL.com"
    },
    {
        "type": "NEWS",
        "text": "ESPN CFB",
        "detail": "How long will a quarterback stay? A college football transfer portal conundrum"
    },
    {
        "type": "NEWS",
        "text": "Team: Pittsburgh Steelers",
        "detail": "Steelers Get Disrespectful NFL Playoff Odds Ahead Of Wild Card Round - SportsNet Pittsburgh"
    },
    {
        "type": "NEWS",
        "text": "ESPN NFL",
        "detail": "Sources: Commanders' Kingsbury, Whitt both out"
    },
    {
        "type": "NEWS",
        "text": "Team: Indianapolis Colts",
        "detail": "Numbers Prove Colts' Collapse To End The NFL Season Wasn't Just Embarrassing, It Was Historic - OutKick"
    },
    {
        "type": "NEWS",
        "text": "CBS CFB",
        "detail": "Why Oregon can finally break through in College Football Playoff and win first national championship"
    },
    {
        "type": "NEWS",
        "text": "Team: Denver Broncos",
        "detail": "Broncos 2026 opponents released ahead of postseason - kdvr.com"
    },
    {
        "type": "NEWS",
        "text": "Team: Buffalo Bills",
        "detail": "ESPN insider downplays Bills\u2019 most glaring defensive concern for postseason run - BuffaLowDown"
    },
    {
        "type": "NEWS",
        "text": "CBS NBA",
        "detail": "NBA odds, picks, best bets for Tuesday, Jan. 6 from proven model: This 3-leg parlay returns +709"
    },
    {
        "type": "NEWS",
        "text": "ESPN NBA",
        "detail": "Four trade proposals for Trae Young: What could Atlanta get for the star guard?"
    },
    {
        "type": "NEWS",
        "text": "Team: Carolina Panthers",
        "detail": "Panthers release former Clemson star player who made inspiring NFL comeback - WBTV"
    },
    {
        "type": "NEWS",
        "text": "ESPN CFB",
        "detail": "Sources: OC Weis to coach Ole Miss in CFP semi"
    },
    {
        "type": "NEWS",
        "text": "Team: Baltimore Ravens",
        "detail": "Ravens fire HC John Harbaugh after his 18th season ends with missing playoffs - NFL.com"
    },
    {
        "type": "NEWS",
        "text": "CBS NBA",
        "detail": "The sky is falling for the Thunder: Four reasons why OKC has come back to earth after sizzling start"
    },
    {
        "type": "NEWS",
        "text": "Team: New York Giants",
        "detail": "New York Giants future 2026 opponents set - Giants.com"
    },
    {
        "type": "NEWS",
        "text": "Team: New York Jets",
        "detail": "49ers DC Robert Saleh Interviewing for Head Coaching Job One Year After Jets Firing - Sports Illustrated"
    },
    {
        "type": "NEWS",
        "text": "Team: Houston Texans",
        "detail": "Houston Texans need win over Indianapolis Colts and loss by Jacksonville Jaguars to win AFC South for third straight season - ABC13 Houston"
    },
    {
        "type": "NEWS",
        "text": "Team: Green Bay Packers",
        "detail": "NFL announces Packers-Bears will have a flag-happy referee - Acme Packing Company"
    },
    {
        "type": "NEWS",
        "text": "ESPN CFB",
        "detail": "Sources: Arch's roomie now rival as WR joins OU"
    },
    {
        "type": "NEWS",
        "text": "PFT",
        "detail": "Lions fire offensive coordinator John Morton"
    },
    {
        "type": "NEWS",
        "text": "Team: Indianapolis Colts",
        "detail": "Colts' Charvarius Ward on concussions: 'If I walk away, I won\u2019t regret it' - IndyStar"
    },
    {
        "type": "NEWS",
        "text": "Team: Kansas City Chiefs",
        "detail": "Patrick Mahomes Posts Cryptic Photos of Him Walking Off the Field - People.com"
    },
    {
        "type": "NEWS",
        "text": "Team: Pittsburgh Steelers",
        "detail": "Texans vs Steelers picks, predictions, odds for NFL playoff game Monday - azcentral.com and The Arizona Republic"
    },
    {
        "type": "NEWS",
        "text": "CBS NBA",
        "detail": "Today's top games to watch, best bets, odds: Duke at Louisville, Texas Tech at Houston and more"
    },
    {
        "type": "NEWS",
        "text": "Team: Los Angeles Chargers",
        "detail": "Los Angeles Chargers vs. Denver Broncos: How to watch today's NFL game, kickoff time, TV channel and more - Yahoo Sports"
    },
    {
        "type": "NEWS",
        "text": "Team: Arizona Cardinals",
        "detail": "Cardinals To Pick Third In NFL Draft For 2026 - Arizona Cardinals"
    },
    {
        "type": "NEWS",
        "text": "ESPN NFL",
        "detail": "Tracking NFL head coach firings: Ravens move on from John Harbaugh"
    },
    {
        "type": "NEWS",
        "text": "Team: Dallas Cowboys",
        "detail": "Impact: How history could narrow down Cowboys' next DC options - Dallas Cowboys | Official Site of the Dallas Cowboys"
    },
    {
        "type": "NEWS",
        "text": "Team: Washington Commanders",
        "detail": "Commanders waste no time making a flurry of signings after 2025 season - Riggo's Rag"
    },
    {
        "type": "NEWS",
        "text": "PFT",
        "detail": "Bills sign K Matthew Wright to practice squad"
    },
    {
        "type": "NEWS",
        "text": "Team: Dallas Cowboys",
        "detail": "Darkhorse Cowboys defensive coordinator candidate emerges from NFL insider - Sports Illustrated"
    },
    {
        "type": "NEWS",
        "text": "Team: Tampa Bay Buccaneers",
        "detail": "Bucs' Finalized List of 2026 Opponents Includes Cowboys, Chargers, Rams - Tampa Bay Buccaneers"
    },
    {
        "type": "NEWS",
        "text": "Team: San Francisco 49ers",
        "detail": "San Francisco 49ers opponents for 2026 season announced - 49ers Webzone"
    },
    {
        "type": "NEWS",
        "text": "Team: Carolina Panthers",
        "detail": "NFL overreactions: Panthers are a safe bet as big underdog - The New York Times"
    },
    {
        "type": "NEWS",
        "text": "Team: New York Giants",
        "detail": "2026 NFL draft: What is the New York Giants' first-round pick worth? - Giants Wire"
    },
    {
        "type": "NEWS",
        "text": "Team: New England Patriots",
        "detail": "NFL playoff picture: How New England Patriots can clinch AFC\u2019s No. 1 seed in Week 18 - Yahoo Sports"
    },
    {
        "type": "NEWS",
        "text": "ESPN NFL",
        "detail": "Morton fired as Lions' OC after just one season"
    },
    {
        "type": "NEWS",
        "text": "Team: Denver Broncos",
        "detail": "Broncos\u2019 opponents finalized for 2026 season - Denver Broncos"
    },
    {
        "type": "NEWS",
        "text": "Team: Cleveland Browns",
        "detail": "Browns fire coach Stefanski, will keep GM Berry - ESPN"
    },
    {
        "type": "NEWS",
        "text": "Team: Buffalo Bills",
        "detail": "Bills brace for grueling playoff journey starting in Jacksonville - Democrat and Chronicle"
    },
    {
        "type": "NEWS",
        "text": "@PFF",
        "detail": "Have you ever wanted to create your own NFL Draft Big Board? NOW YOU CAN!\n\nUse the PFF Big..."
    },
    {
        "type": "NEWS",
        "text": "Team: Seattle Seahawks",
        "detail": "Super Bowl odds: Seahawks, Rams, Broncos lead a tight playoff field - The Athletic - The New York Times"
    },
    {
        "type": "NEWS",
        "text": "Team: Kansas City Chiefs",
        "detail": "Chiefs waive quarterback Shane Buechele, make 5 other roster moves - Arrowhead Pride"
    }
];
