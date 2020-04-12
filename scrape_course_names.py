

from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np


# Scrape all course names from golf advisor

ga_url = 'https://www.golfadvisor.com/course-directory/2-usa/'

# Load html contents to bs object
r = requests.get(ga_url)
soup = BeautifulSoup(r.content)

# extract all gamelinks
state_list = soup.find_all("div",{"class":"LocationTagPromo-title"})

# obtain state specifc urls
state_urls = []
for st in state_list:

    # create temp dict
    temp_dict = {}

    # scrape url
    st_url = st.find_all('a')[0]['href']

    # only date state links
    if 'destinations' in st_url:

        pass

    else:
        # add url to list
        temp_dict['state_url'] = st_url

        # scrape state text
        temp_dict['state'] = st.text

        # add temp dict to master list
        state_urls.append(temp_dict)

        # print url
        print(st_url)

# create dataframe of state urls
state_df = pd.DataFrame(state_urls)

#%%

region_results_lst = []

# loop through state and scrape all regions
for st_url, state in zip(state_df['state_url'], state_df['state']):

    # extract state page html
    r = requests.get(st_url)
    soup = BeautifulSoup(r.content)

    # extract all regions in state
    region_sub = soup.find_all("div",{"class":"LocationTagPage-sublocations section"})
    region_list = region_sub[0].find_all("div",{"class":"LocationTagPromo-info"})

    # loop through regions to extract all links and course counts
    for reg in region_list:

        temp_dict = {}

        # Extract region name and link
        region_name_soup = reg.find("div", {"class":"LocationTagPromo-title"})

        temp_dict['region_url'] = region_name_soup.find('a')['href']
        temp_dict['region'] = region_name_soup.text.strip('\n')

        # extract course and review count
        temp_dict['count_review_str'] = reg.find("div", {"class":"LocationTagPromo-description"})\
            .text

        # add state
        temp_dict['state'] = state

        # append result to master list
        region_results_lst.append(temp_dict)

        print(region_name_soup.find('a')['href'])

# create dataframe of regions
region_link_df = pd.DataFrame(region_results_lst)

# parse out course count and review string
region_link_df['course_count'] = [x.split(' | ')[0].split(' ')[0] for x in region_link_df['count_review_str']]

# subset to only regions with courses
region_link_df = region_link_df[region_link_df['course_count'] != '0']\
    .reset_index(drop=True)

#%%
# Scrape all course names from regions

master_course_list = []

for region_url, state, region_str in zip(region_link_df['region_url'],
                      region_link_df['state'],
                      region_link_df['region']):

    # extract state page html
    r = requests.get(region_url)
    soup = BeautifulSoup(r.content)

    # extract all regions in state
    course_sub = soup.find_all("div",{"class":\
        "LocationTagPage-courses section"})

    # extract all courses in region
    courses_parent = course_sub[0].find_all("div",{"class":"StandardCoursePromo"})

    # loop through all courses to extract name
    for course in courses_parent:

        temp_dict = {}

        course_name = course.find("div",{"class":"StandardCoursePromo-title"}).text.strip("\n")

        temp_dict['state'] = state
        temp_dict['region'] = state
        temp_dict['course'] = course_name

        master_course_list.append(temp_dict)

        print(course_name)

all_us_courses = pd.DataFrame(master_course_list)

all_us_courses.to_csv('inital_course_list.csv', index=False)
