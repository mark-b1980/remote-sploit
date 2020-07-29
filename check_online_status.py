import sys, random, requests, time

URLLIST = """wikipedia.org
google.com
youtube.com
twitter.com
facebook.com
amazon.com
imdb.com
merriam-webster.com
apple.com
dictionary.com
instagram.com
tripadvisor.com
pinterest.com
wiktionary.org
fandom.com
yahoo.com
yelp.com
cambridge.org
urbandictionary.com
espncricinfo.com
craigslist.org
roblox.com
linkedin.com
weather.com
espn.com
healthline.com
britannica.com
microsoft.com
bbc.com
cricbuzz.com
walmart.com
webmd.com
thepirate-bay.org
livescore.com
ytmp3.cc
rottentomatoes.com
homedepot.com
whatsapp.com
bestbuy.com
thesaurus.com
gsmarena.com
live.com
xvideos.com
timeanddate.com
theguardian.com
accuweather.com
office.com
mayoclinic.org
flashscore.com
genius.com
indiatimes.com
blog.google
cnn.com
yourdictionary.com
spotify.com
nytimes.com
spanishdict.com
pornhub.com
xnxx.com
steampowered.com
thefreedictionary.com
dominos.com
y2mate.com
bbc.co.uk
cnet.com
netflix.com
poki.com
reddit.com
investopedia.com
skyscanner.com
playstation.com
ebay.com
samsung.com
dailymail.co.uk
uptodown.com
nih.gov
indeed.com
collinsdictionary.com
techradar.com
globo.com
vocabulary.com
friv.com
speedtest.net
ndtv.com
expedia.com
premierleague.com
unsplash.com
quora.com
ryanair.com
medicalnewstoday.com
macys.com
nike.com
santanderbank.com
booking.com
pizzahut.com
target.com
adobe.com
about.google
businessinsider.com
goodhousekeeping.com""".split("\n")


def test_rand_url():
    r = requests.get(random.choice(URLLIST))
    if r.status_code == 200:
        return True
    return False


def wait_for_connection(test_delay):
    r = 0
    while r == 0:
        try:
            r = requests.get("https://" + random.choice(URLLIST), timeout=2.0).status_code
        except requests.exceptions.ConnectionError:
            r = 0

        if r == 0:
            print("waiting for internet connection ...")
            time.sleep(test_delay)