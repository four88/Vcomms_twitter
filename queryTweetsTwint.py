import twint 
import pandas as pd
from datetime import timedelta
from os import mkdir, path
from string import ascii_letters, digits

uk_cities = pd.read_csv('uk_cities.csv')
uk_cities = uk_cities['TCITY15NM'].values.tolist()

print(uk_cities)

def scrape_by_geo(keywords, geocode,since,until, outfile):
    c = twint.Config()
    c.Search = keywords #search keyword
    c.Since = since
    c.Until = until
    c.Limit = 50000
    c.Geo = geocode
    # c.Store_csv = True
    c.Store_json = True
    c.Output = "output/" + outfile
    c.Hide_output = True
    c.Count = True
    c.Stats = True
    c.Lang = 'en'
    twint.run.Search(c)

def clean_name(dirname):
    valid = set(ascii_letters + digits)
    return ''.join(a for a in dirname if a in valid)


def twint_loop(searchterm, geocode, since, until):

    dirname = clean_name("uk")
    try:
    # Create target Directory
        mkdir(dirname)
        print("Directory" , dirname ,  "Created ")
    except FileExistsError:
        print("Directory" , dirname ,  "already exists")

    daterange = pd.date_range(since, until)

    for start_date in daterange:

        since= start_date.strftime("%Y-%m-%d")
        until = (start_date + timedelta(days=1)).strftime("%Y-%m-%d")

        json_name = '%s.json' % since
        json_name = path.join(dirname, json_name)

        print('Getting %s ' % since )
        scrape_by_geo(searchterm,geocode, since, until, json_name)

# location geocode
uk_geo = "54.153709,-4.529766,527km"
th_geo = "9.776238,7.742880,800km"
eu_geo = "54.321720,-0.879033,2040km"

since = '2017-01-01'
until = '2020-11-07'

twint_loop("'flooding' OR 'flood' OR 'floods'",uk_geo, '21-05-2021','07-11-2022')
#


# scrape_by_city("'flooding' OR 'flood' OR 'floods' OR 'climate change'", since, 'Uk_Tweets_Dataset.csv', uk_cities)
