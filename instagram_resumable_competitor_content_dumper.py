 # -*- encoding: utf-8 -*-
from unidecode import unidecode
import selenium
import datetime as datemonth007
from datetime import datetime
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

browser = webdriver.Chrome()
time.sleep(1)


## Extracting data from Instagram*******************************************************************************************************************

##Pre crawled existance check

k = pd.read_csv("browse_data.csv")
links = dict(zip(k.name, k.link))

no_browsing_list = ["parulgargmakeup","pooja_sharma_makeovers"]
##Checkiing the previous crawled status and resuming from where it left 
try :
	to_remove = []
	with open('Instagram_Tracker.csv','r') as file :
		reading_previous = file.read()
	print "Resuming previous crawling"
	for brand_name in links :
		if brand_name + " --->  " +  "Average likes per post for this month = " in reading_previous or brand_name in no_browsing_list :
			to_remove.append(brand_name)
			#del links[brand_name]
			print "Already crawled " + brand_name + " so, not crawling it again"
		else :
			pass
	for deleting in to_remove :
		del links[deleting]
	print "Brands that are going to be crawled are :- "
	for brand_name in links :
		print brand_name

except :
	print "Starting a fresh crawl"

#Exiting if every brand data has been already crawled in the file
if len(links) == 0 :	
	print "Already every brand has been crawled in file, so Aborting...if you want to do a fresh crawl again then delete Instagram_Tracker.csv first then run again "
	browser.quit()
	quit(1)

#opening both files
o1 = open('Instagram_Tracker.csv','a')
f1 = csv.writer(o1)
f1.writerow(['Details'])


try :
	check_df = pd.read_csv("commenters_details.csv")
except :
	with open("commenters_details.csv","a") as kkk :
		lmk = csv.writer(kkk)
		lmk.writerow(['insta_id_name','comment','insta_id_link','post_title','post_date_time','page_name','page_link'])

##Crawling Instagram

for brand in links :


	#Gucci Instagram 

	tries = 1
	for attempt in range(5) :
	  try :
	    
	    link = str(links[brand].replace("\n","").replace("\r",""))
	    print brand
	    print link
	    browser.get(link)
	    time.sleep(1)
	    page_soup = soup(browser.page_source,"html.parser")
	    follower = page_soup.findAll("span",{"class" : "g47SY "})[1]['title']
	    follower = brand + " Instagram followers =" + follower
	    f1.writerow([follower])
	    print follower
	    time.sleep(1)
	  except :
	  	time.sleep(random.randint(1,3))
	  	print tries
	  	tries = tries + 1
	  else :
	    break
	else :
	  failing = 'Failed_loading_from -- ' + str(link)
	  failed_execution.append(failing)

	ActionChains(browser).send_keys(Keys.SPACE).perform()



	time.sleep(1)
	start_click = browser.find_elements_by_class_name("eLAPa")[0]
	print start_click
	start_click.click()



	try :
		start_click.click()
		start_click.click()
		start_click.click()
		start_click.click()

	except :
		pass

	time.sleep(3)


	#Browsing through posts

	total_post_likes = 0
	post_count = 0
	current_month = int(datemonth007.datetime.now().strftime("%m"))
	post_month = current_month
	old_like = 0

	while current_month == post_month or current_month-1 == post_month :#or current_month-2 == post_month or current_month-3 == post_month :

		page_soup = soup(browser.page_source,"html.parser")

		try :
			current_like = int(page_soup.findAll("div",{"class" : "Nm9Fw"})[0].span.text.strip().replace(",",""))
		except :
			current_like = int(page_soup.findAll("span",{"class" : "vcOH2"})[0].span.text.strip().replace(",",""))


		print "current post like = " + str(current_like)
		if current_like != old_like :
			old_like = current_like
			total_post_likes = total_post_likes + current_like
			post_count = post_count + 1
			print "current post no = " + str(post_count)
			post_month = int(page_soup.findAll("time",{"class" : "_1o9PC Nzb55"})[0]['datetime'].split("T")[0].split("-")[1])

			#grabbing all comments

			time.sleep(1)
			start_click = browser.find_elements_by_class_name("lnrre")
			view_comment_loop_counter = 0
			while len(start_click) != 0 and view_comment_loop_counter < 20 :

				start_click = browser.find_elements_by_class_name("lnrre")[0]
				print start_click
				try :
					
					start_click.click()
					start_click.click()
					start_click.click()
					start_click.click()
					ActionChains(browser).double_click(start_click).perform()

				except :
					pass
				try :
					ActionChains(browser).send_keys(Keys.PAGE_UP).perform()
					ActionChains(browser).send_keys(Keys.PAGE_UP).perform()
					ActionChains(browser).send_keys(Keys.PAGE_UP).perform()
					ActionChains(browser).send_keys(Keys.PAGE_UP).perform()
					ActionChains(browser).send_keys(Keys.PAGE_UP).perform()
					ActionChains(browser).send_keys(Keys.PAGE_UP).perform()
				except :
					pass

				time.sleep(1)
				try :
					click = browser.find_elements_by_class_name("lnrre")[0]
					try :
						start_click = browser.find_elements_by_class_name("lnrre")
					except :
						pass
				except :
					start_click = []
				view_comment_loop_counter = view_comment_loop_counter + 1

			page_soup = soup(browser.page_source,"html.parser")
			all_commenters_tag = page_soup.findAll("div",{"class" : "C4VMK"})
			comment_count = 0
			for single_comment in all_commenters_tag :
				if comment_count == 0 :
					ownwer_comment = unidecode(single_comment.span.text.strip())
					print ownwer_comment
					pass
				else :
					commenter_insta_id = "https://www.instagram.com" + str(single_comment.a['href'])
					commenter_comment = single_comment.span.text.strip()

					commenter_comment = unidecode(commenter_comment)
					# commenter_comment = commenter_comment.encode('ascii', 'replace')
					# commenter_comment = commenter_comment.replace("?", "")
					post_date_time = page_soup.findAll("time",{"class" : "_1o9PC Nzb55"})[0]['datetime']

					with codecs.open("commenters_details.csv","a","utf-8") as kkk :
						lmk = csv.writer(kkk)
						lmk.writerow([str(single_comment.a['href']).replace("/",""),str(commenter_comment),commenter_insta_id,ownwer_comment,str(post_date_time),str(brand),str(link)])

				comment_count =  comment_count + 1



			ActionChains(browser).send_keys(Keys.RIGHT).perform()
			time.sleep(3)

		else :

			ActionChains(browser).send_keys(Keys.RIGHT).perform()



	Total_no_of_post_this_month = brand + " --->  " + "Total no of post this month till current date = " + str(post_count) 
	Total_no_of_likes_on_posts_this_month = brand + " --->  " + "Total no of likes on posts this month = " + str(total_post_likes) 
	Average_likes_per_post = brand + " --->  " +  "Average likes per post for this month = " + str(float(total_post_likes) / float(post_count)) 


	print Total_no_of_post_this_month
	print Total_no_of_likes_on_posts_this_month
	print Average_likes_per_post



	f1.writerow([Total_no_of_post_this_month])
	f1.writerow([Total_no_of_likes_on_posts_this_month])
	f1.writerow([Average_likes_per_post])

	o1.close	


end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

time.sleep(1)

browser.quit()
# ##*****************************************************************************************************************************************************


