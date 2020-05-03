 # -*- encoding: utf-8 -*-
from unidecode import unidecode
import selenium
import datetime as datemonth007
from datetime import datetime
from datetime import timedelta
from time import gmtime, strftime, localtime
start_time = datetime.now()
from selenium import webdriver
from bs4 import BeautifulSoup as soup
import sys
import os
import time
import csv
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import codecs

failed_execution = ['Execution completed successfully']

#88888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888

#Initial start and account login***************************************************************************************************************************************

browser = webdriver.Firefox()
time.sleep(1)
browser.get("https://www.instagram.com/accounts/login/?source=auth_switcher")

email = browser.find_element_by_name('username')
email.clear()
password = browser.find_element_by_name('password')
password.clear()

email.send_keys('udita0512@gmail.com') #enter email
password.send_keys('passwordjahsdjh') #enter password
password.send_keys(Keys.RETURN)
time.sleep(5)


## Filtering data to unfollow*******************************************************************************************************************


id_aready_unfollowed = pd.read_csv("alread_unfollowed_ids.csv")
id_aready_unfollowed = id_aready_unfollowed.drop_duplicates("link").reset_index(drop = True)
id_aready_unfollowed = id_aready_unfollowed["link"].tolist()


id_aready_followed = pd.read_csv("alread_followed_ids.csv")
id_aready_followed = id_aready_followed.drop_duplicates("link").reset_index(drop = True)
id_aready_followed["time"] = pd.to_datetime(id_aready_followed["time"], format = "%Y-%m-%d %H:%M:%S", errors = 'coerce')
three_days_before_today = str(datetime.now() - timedelta(days = 3)).split(".")[0].split(":")[0] + str(":00:00")
id_aready_followed = id_aready_followed[id_aready_followed["time"] <= three_days_before_today]
id_aready_followed = id_aready_followed["link"].tolist()
id_to_unfollow = id_aready_followed
print len([x for x in id_to_unfollow if x not in id_aready_unfollowed])




def checking_no_of_ids_unfollowed_this_hour() :
	current_start_hour = str(datetime.now()).split(".")[0].split(":")[0] + str(":00:00")
	current_end_hour = str(datetime.now() + timedelta(minutes=60)).split(".")[0].split(":")[0] + str(":00:00")
	hourly_count_df = pd.read_csv("alread_unfollowed_ids.csv")
	hourly_count_df["time"] =  pd.to_datetime(hourly_count_df["time"], format = "%Y-%m-%d %H:%M:%S",errors = 'coerce')
	mask = (hourly_count_df['time'] > current_start_hour) & (hourly_count_df['time'] <= current_end_hour)
	hourly_count_df = hourly_count_df.loc[mask]
	#print hourly_count_df
	hourly_count =  len(hourly_count_df)
	return hourly_count

def checking_no_of_ids_unfollowed_this_day() :
	current_start_day = str(datetime.now()).split(" ")[0]+ str(" 00:00:00")
	current_end_day = str(datetime.now() + timedelta(days=1)).split(" ")[0]+ str(" 00:00:00")
	daily_count_df = pd.read_csv("alread_unfollowed_ids.csv")
	daily_count_df["time"] =  pd.to_datetime(daily_count_df["time"], format = "%Y-%m-%d %H:%M:%S",errors = 'coerce')
	mask = (daily_count_df['time'] > current_start_day) & (daily_count_df['time'] <= current_end_day)
	daily_count_df = daily_count_df.loc[mask]
	#print daily_count_df
	daily_count =  len(daily_count_df)
	return daily_count



hourly_count = checking_no_of_ids_unfollowed_this_hour()
daily_count = checking_no_of_ids_unfollowed_this_day()

print hourly_count
print daily_count

while True :
	if hourly_count <= 15 and daily_count <= 2000:
		for single_id in id_to_unfollow :
			hourly_count = checking_no_of_ids_unfollowed_this_hour()
			daily_count = checking_no_of_ids_unfollowed_this_day()
			if hourly_count <= 15 and daily_count <= 2000:
				if single_id not in id_aready_unfollowed :
					browser.get(single_id)
					current_time_stamp = strftime("%Y-%m-%d %H:%M:%S", localtime())
					try :
						try :
							follow_button = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/div/span/span[1]')
							#follow_button = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/button')
						except :
							follow_button = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[2]/div/span/span[1]/button')

						while str(follow_button.text) == "Following" or str(follow_button.text) == "Requested":
							follow_button.click()
							time.sleep(2)
							try :
								follow_button.click()
								follow_button.click()
							except :
								pass
							try :
								try :

									unfollow_button = browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]')
								except :
									unfollow_button = browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[1]')
								unfollow_button.click()

								time.sleep(10)
							except :
								pass

							try :
								follow_button = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/button')
							except :
								follow_button = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/span/span[1]/button')

						with open("alread_unfollowed_ids.csv","a") as f :
							f1 = csv.writer(f)
							f1.writerow([current_time_stamp,single_id])
						id_aready_unfollowed.append(single_id)
						print str(single_id) + " unfollowed and log maintained"
						hourly_count = checking_no_of_ids_unfollowed_this_hour()
						daily_count = checking_no_of_ids_unfollowed_this_day()

					except :
						pass

	elif daily_count > 2000 :
		print "daily count limit reached"
		browser.quit()
	elif hourly_count > 15 :
		print "hourly limit reached"

	hourly_count = checking_no_of_ids_unfollowed_this_hour()
	daily_count = checking_no_of_ids_unfollowed_this_day()
	print "currrent_unfollowed_hourly_count = " + str(hourly_count)
	print "currrent_unfollowed_daily_count = " + str(daily_count)
	time.sleep(1)
		
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

time.sleep(1)

