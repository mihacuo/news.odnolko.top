print("started rss_news_v2.py")
import peewee
import feedparser
from datetime import datetime, timedelta
from time import monotonic
from sys import exit
from bs4 import BeautifulSoup as bs4

now = datetime.now()
year = now.strftime("%Y")
hr = now.strftime("%H")

db_en = peewee.SqliteDatabase(f"/root/www/news.odnolko.top/db/rss_en_{year}.db")
db_ru = peewee.SqliteDatabase(f"/root/www/news.odnolko.top/db/rss_ru_{year}.db")

def l(t, log):
    info_log_file: str = f"/root/www/news.odnolko.top/log/log_info_{year}.txt"
    info_log_error: str = f"/root/www/news.odnolko.top/log/log_error_{year}.txt"
    for _ in str(t):
        print(log)
        timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        if _=="0":
            with open(info_log_error, "a") as f:
                f.write(f"{timestamp}|{str(log)}\n")
        elif _=="1":
            with open(info_log_file, "a") as f:
                f.write(f"{timestamp}|{str(log)}\n")
        elif _=="9":
            pass
        else: 
            with open(info_log_error, "a") as f:
                f.write(f"{timestamp}|incorrect log type parameter\n")              

def get_urls(file):
    try:
        with open(file, "r") as f:
            contents = f.readlines()
            urls = [_.strip() for _ in contents if _.strip()[0:1] != "#" and _.strip() != ""]
            l(1, f"Loaded {len(urls)} urls from {file}")
            return urls
    except Exception as e:
        l(0, f"error when loading urls from {file}")
        exit()
        
class Rss(peewee.Model):
    title = peewee.CharField(unique=True)
    detail = peewee.CharField()
    created = peewee.DateTimeField(default=datetime.now)

    @classmethod
    def save_all(cls):
        start = monotonic()
        grand_loaded, grand_saved, grand_not_saved = 0, 0, 0
        for num, url in enumerate(cls.urls):    
            l(1, f'Loading {url}, {num+1} out of {len(cls.urls)}')
            try:
                feed = feedparser.parse(url)
            except:
                l(0,f'Error connecting to {url}')
                continue
            if not hasattr(feed, 'status'):
                l(0,f'Error with rss {url}')
                continue
            if feed.status == 404:
                l(0, f'Err:RSS url invalid:, {url}')
            elif feed.status == 301 or feed.status == 200:
                news = []
                for item in feed['entries']:
                    if hasattr(item, 'summary'):
                        summary = item.summary
                    else:
                        summary = 'MISSING'
                    if hasattr(item, 'title'):
                        title = item.title
                    else:
                        title = 'MISSING'
                    news.append([title, summary])

                # trying to save to peewee DB
                saved = 0
                not_saved = 0
                for item in news:
                    try:
                        soup = bs4(item[1], 'html.parser')
                        norm = soup.text.strip()
                        cls.create(title=item[0], detail=norm)
                        saved += 1
                    except Exception as e:
                        # (0, f"error {e} from {url}")
                        not_saved += 1
                l(1,f'{url}, {num+1} out of {len(cls.urls)} Loaded: {len(news)}; Saved: {saved}; Not: {not_saved}')
                grand_loaded += len(news)
                grand_saved += saved
                grand_not_saved += not_saved
                # unknows status code
            else:
                l(0, f'RSS Err:code {feed.status} unable to load {url}')
        l(1, f"RSS Total: {grand_loaded}; Saved: {grand_saved}({int(round(grand_saved/grand_loaded*10, 0))}%). Exec time = {monotonic()-start:.2f} secs.")
  
# return all news from the date range
    @classmethod
    def get_news_dated(cls, start, end):
        start_time = monotonic()
        data = cls.select().where((cls.created > start) & (cls.created < end))
        return data, [f"Selecting Dated news from {cls.select().count()} items",
                      f"get_news_dated returned {len(data)} items. Exec time = {monotonic()-start_time:.2f} secs."]
        # return data, ["da"]
    @staticmethod
    def get_news(data, include=False, exclude=False):
        flashes = []
        start = monotonic()
        flashes.append(f"starting get_news, working with {len(data)} items")
        result = []
        for num, item in enumerate(data):
            suitable = True
            if include: 
                for _ in include:
                    if _.lower() not in item.title.lower() or _.lower() not in item.detail.lower():
                        suitable = False
            if exclude:
                for _ in exclude:
                    if _.lower() in item.title.lower() or _.lower() in item.detail.lower():
                        suitable = False
            if suitable:
                result.append(item)
        flashes.append(f"Filtered news, with {include=}&{exclude=} is {len(result)} items. Exec time = {monotonic()-start:.2f} secs.")
        return result, flashes  
    
class Rss_en(Rss):
    urls = get_urls("/root/www/news.odnolko.top/static/rss_batches_en.txt")
    # urls = ["https://www.theregister.com/headlines.atom"]
    class Meta:
        database = db_en

    @staticmethod
    def get_latest_news(ticks):
        flashes = []
        data = []
        days = 3
        end = datetime.now()
        start = end - timedelta(days=days)
        all_latest_news = Rss_en.get_news_dated(start=start, end=end)
        flashes += all_latest_news[1]
        flashes.append(f"Latest news,start: {start.strftime('%d/%m/%Y')}, end: {end.strftime('%d/%m/%Y')}")
        for tick in ticks:
            match tick:
                case "Ag":
                    string = "silver"
                case "Pd":
                    string = "palladium"
                case "Au":
                    string = "gold"
                case "Pt":
                    string = "platinum"
                case _:
                    string = tick
            this_data = Rss_en.get_news(all_latest_news[0], include=[string])
            flashes += this_data[1]
            data.append([string, this_data[0]])
        return data, flashes
            
class Rss_ru(Rss):
    urls = get_urls("/root/www/news.odnolko.top/static/rss_batches_ru.txt")
    class Meta:
        database = db_ru

db_en.create_tables([Rss_en])
db_ru.create_tables([Rss_ru])

print(F"{Rss_en.select().count()=}")
print(F"{Rss_ru.select().count()=}")


if __name__ == "__main__":
    Rss_ru.save_all()
    Rss_en.save_all()

db_en.close()
db_ru.close()
