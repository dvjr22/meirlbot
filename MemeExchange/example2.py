
from pytrends.request import TrendReq

google_username = "xxx@gmail.com"
google_password = "xxx"
path = ""

# connect to Google
pytrend = TrendReq(google_username, google_password, custom_useragent='My Pytrends Script')

trend_payload = {'q': 'Pizza, Italian, Spaghetti, Breadsticks, Sausage', 'cat': '0-71'}

# trend
trend = pytrend.trend(trend_payload)
#print(trend)
df = pytrend.trend(trend_payload, return_type='dataframe')
print(df)

