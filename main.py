import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import os

AUDIBLE_URL = "https://www.audible.co.uk/adblbestsellers?ref=a_adblbests_c5_pageSize_3&pf_rd_p=936af2d3-3c4b-4217-a77c-041f7ca03d0d&pf_rd_r=E7CZJ1W791FBQAKW9TC2&pageSize=50"
ACCEPTED_LANGUAGE = os.getenv("ACCEPTED_LANGUAGE")
USER_AGENT = os.getenv("USER_AGENT")

headers = {
    "Accepted-Language": ACCEPTED_LANGUAGE,
    "User-Agent": USER_AGENT
}

response = requests.get(url=AUDIBLE_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
titles = [book_title.getText().replace("  ", "").replace("\n","").split('.',1)[1] for book_title in soup.find_all(name="h3", class_="bc-heading")[3:]]
authors = [book_author.getText().replace("  ", "").replace("\n","")[3:] for book_author in soup.find_all(class_="authorLabel")]
run_times = [run_time.getText().replace("  ", "").replace("\n","")[8:] for run_time in soup.find_all(class_="runtimeLabel")]
release_dates = [release_date.getText().replace("  ", "").replace("\n","")[13:] for release_date in soup.find_all(class_="releaseDateLabel")]
languages = [language.getText().replace("  ", "").replace("\n","")[9:] for language in soup.find_all(class_="languageLabel")]
ratings = [rating.getText().replace("\n", "").split(' stars')[0] for rating in soup.find_all(class_="ratingsLabel")]
prices = [price.getText().replace("\n","").replace("Regular price:", "").replace(" ","") for price in soup.find_all(class_="buybox-regular-price")]

# Create a Pandas Dataframe
audible_data = [titles, authors, run_times, release_dates, languages, ratings, prices]
df = DataFrame(audible_data).transpose()
df.columns = ['Title', 'Author', 'Run_Time', 'Release_Date', 'Language', 'Rating', 'Price']

# Export to CSV file
df.to_csv('audible_top_50.csv', encoding='utf-8-sig')
