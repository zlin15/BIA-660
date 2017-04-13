# coding: utf-8

import bs4
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import unidecode
from unidecode import unidecode
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from scipy.spatial import distance
import itertools

# ============= Task1 ==============
driver = webdriver.Chrome('/Users/linzeyang/Desktop/BIA-660/chromedriver')
driver.get('https://www.google.com/flights/explore/')
time.sleep(0.5)


def scrape_data(start_date, from_place, to_place, city_name):
    # from_place
    to_input = driver.find_elements_by_class_name('LJTSM3-p-a')[0]
    to_input.click()
    actions = ActionChains(driver)
    a = from_place
    actions.send_keys(a)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(1.5)
    # to_place
    to_input = driver.find_elements_by_class_name('LJTSM3-p-a')[1]
    to_input.click()
    actions = ActionChains(driver)
    b = to_place
    actions.send_keys(b)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(1.5)
    # start_date
    url_changed_date = driver.current_url[:-10] + start_date
    driver.get(url_changed_date)
    time.sleep(1.5)
    # collect all output city names and store them into a list:
    results = driver.find_elements_by_class_name('LJTSM3-v-c')
    # print results[0].text  #Portland
    citi_list_ori = []
    for i in range(len(results)):
        one_city_name = results[i].text.split(',')[0]
        citi_list_ori.append(one_city_name)
    citi_list = []
    for city in citi_list_ori:
        city = unidecode(city)
        citi_list.append(city)
    # get particular city:
    for c in range(len(citi_list)):
        if city_name != citi_list[c]:
            continue
        else:
            # get Date & Price for that particular city:
            results = driver.find_elements_by_class_name('LJTSM3-v-d')
            time.sleep(0.2)
            test = results[c]
            bars = test.find_elements_by_class_name('LJTSM3-w-x')  # bars contain dates and price
            time.sleep(2.0)
            data_date_ori = []
            data_date = []
            data_price = []
            for bar in bars:
                ActionChains(driver).move_to_element(bar).perform()
                time.sleep(0.05)
                data_date_ori.append(
                    test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text)
            # print len(data_date_ori)
            for i in range(len(data_date_ori)):
                start_date = str(data_date_ori[i]).split('- ')[0]
                data_date.append(start_date)
                time.sleep(0.05)
            # print data_date, len(data_date)
            for bar in bars:
                ActionChains(driver).move_to_element(bar).perform()
                time.sleep(0.05)
                data_price.append(
                    test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text)
                time.sleep(0.05)
            # print data_price,len(data_price)
            scrape_data_date_price = pd.DataFrame(
                {'Date_Start': data_date,
                 'Price_of_TimeRange': data_price
                 })
            return scrape_data_date_price

# Task 1 Test:
X = scrape_data_90('2017-05-10', 'New York', 'united states', 'Chicago')
print X

# ============= Task2 ==============
driver = webdriver.Chrome('/Users/linzeyang/Desktop/BIA-660/chromedriver')
driver.get('https://www.google.com/flights/explore/')
time.sleep(0.5)


def scrape_data_90(start_date, from_place, to_place, city_name):
    # from_place
    to_input = driver.find_elements_by_class_name('LJTSM3-p-a')[0]
    to_input.click()
    actions = ActionChains(driver)
    a = from_place
    actions.send_keys(a)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(1.5)
    # to_place
    to_input = driver.find_elements_by_class_name('LJTSM3-p-a')[1]
    to_input.click()
    actions = ActionChains(driver)
    b = to_place
    actions.send_keys(b)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(1.5)
    # start_date
    url_changed_date = driver.current_url[:-10] + start_date
    driver.get(url_changed_date)
    time.sleep(1.5)
    # collect all output city names and store them into a list:
    results = driver.find_elements_by_class_name('LJTSM3-v-c')
    # print results[0].text  #Portland
    citi_list_ori = []
    for i in range(len(results)):
        one_city_name = results[i]
        one_city_name = one_city_name.text.split(',')[0]
        citi_list_ori.append(one_city_name)
    citi_list = []
    for city in citi_list_ori:
        city = unidecode(city)
        citi_list.append(city)
    data_date_ori = []
    data_date = []
    data_price = []
    for c in range(len(citi_list)):
        if city_name != citi_list[c]:
            continue
        else:
            # get Date & Price for that particular city:
            results = driver.find_elements_by_class_name('LJTSM3-v-d')
            time.sleep(0.2)
            test = results[c]
            bars = test.find_elements_by_class_name('LJTSM3-w-x')
            time.sleep(2.0)
            for bar in bars:
                ActionChains(driver).move_to_element(bar).perform()
                time.sleep(0.02)
                data_price.append(
                    test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text)
                time.sleep(0.01)
                ActionChains(driver).move_to_element(bar).perform()
                time.sleep(0.02)
                data_date_ori.append(
                    test.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text)
                time.sleep(0.01)
            # Next XXX days
            right = driver.find_element_by_class_name('LJTSM3-w-D')
            actions = ActionChains(driver).move_to_element(right).double_click(right)
            actions.perform()
            time.sleep(2.0)
            right = driver.find_element_by_class_name('LJTSM3-w-D')
            actions = ActionChains(driver).move_to_element(right).double_click(right)
            actions.perform()
            time.sleep(1.5)
            # print (citi_list)
    results = driver.find_elements_by_class_name('LJTSM3-v-c')
    citi_list_ori = []
    for i in range(len(results)):
        one_city_name = results[i]
        one_city_name = one_city_name.text.split(',')[0]
        citi_list_ori.append(one_city_name)
    citi_list = []
    for city in citi_list_ori:
        city = unidecode(city)
        citi_list.append(city)
    for c in range(len(citi_list)):
        if city_name != citi_list[c]:
            continue
        else:
            results = driver.find_elements_by_class_name('LJTSM3-v-d')[c]
            time.sleep(0.2)
            bars = results.find_elements_by_class_name('LJTSM3-w-x')
            time.sleep(2.0)
            for bar in bars[:30]:
                ActionChains(driver).move_to_element(bar).perform()
                time.sleep(0.01)
                data_price.append(
                    results.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text)
                # print len(data_price)
                ActionChains(driver).move_to_element(bar).perform()
                time.sleep(0.2)
                data_date_ori.append(
                    results.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text)
            for i in range(len(data_date_ori)):
                start_date = str(data_date_ori[i]).split('- ')[0]
                data_date.append(start_date)
            scrape_data_date_price = pd.DataFrame(
                {'Date_Start': data_date,
                 'Price_of_TimeRange': data_price
                 })
            return scrape_data_date_price

#Task2 Test:
X = scrape_data_90('2017-05-10', 'New York', 'united states', 'Chicago')
print X


# ============= Task3,Part1==============
def task_3_dbscan(flight_data):
    price_one_city = []
    flight_data.Price_of_TimeRange.apply(str)
    for item in X['Price_of_TimeRange']:
        try:
            price_one_city.append(float(item.replace('$', '').replace(',', '')))
            flight_data['Price_of_TimeRange'] = price_one_city
            # print(price_one_city)
        except:
            continue
    # DBSCAN:
    px = [x for x in flight_data['Price_of_TimeRange']]
    ff = pd.DataFrame(px, columns=['fare']).reset_index()
    Y = StandardScaler().fit_transform(ff)
    db = DBSCAN(eps=0.3, min_samples=3).fit(Y)
    labels = db.labels_
    global labels
    clusters = len(set(labels))
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    # plt.subplots(figsize=(12,8))
    for k, c in zip(unique_labels, colors):
        class_member_mask = (labels == k)
        xy = Y[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=c,
                 markeredgecolor='k', markersize=14)
    plt.title("Total Clusters: {}".format(clusters), fontsize=14, y=1.01)
    plt.savefig('task_3_dbscan.png')
    # make date_price_labels dataframe
    d_p_l = pd.DataFrame({
        'date': flight_data['Date_Start'],
        'price': flight_data['Price_of_TimeRange'],
        'z_labels': labels
    })
    # transfer date to index
    for i in range(0, 90):
        d_p_l['date'][i] = i
    # sort date_p_l
    d_p_l_sort = []
    for i in range(-1, len(set(labels)) - 1):
        cluster = d_p_l.loc[d_p_l['z_labels'] == i]  # select rows whose z_labels column equals to i
        d_p_l_sort.append(cluster)
    # count mean for each cluster
    mean_cluster = []
    for i in range(len(set(labels))):
        m = np.array(d_p_l_sort[i]).mean(axis=0)
        mean_cluster.append(m)
    dates_avg_collect = []
    price_avg_collect = []
    for i in range(clusters):
        dates_avg = mean_cluster[i][0]
        dates_avg_collect.append(dates_avg)
    for i in range(clusters):
        price_avg = mean_cluster[i][1]
        price_avg_collect.append(price_avg)
    mean_cluster_zip = zip(dates_avg_collect, price_avg_collect)
    mean_cluster_array = np.array(list(mean_cluster_zip))
    noise_points = d_p_l[d_p_l['z_labels'] == -1]
    delete_labels = noise_points.drop('z_labels', axis=1)
    noise_points_array = np.array(delete_labels)
    noise_points = d_p_l[d_p_l['z_labels'] == -1]
    delete_labels = noise_points.drop('z_labels', axis=1)
    noise_points_array = np.array(delete_labels)
    #  print np.array(mean_cluster_zip)
    a = np.array(mean_cluster_zip)
    b = np.array(noise_points_array)
    dist_all = []
    for i in a:
        for j in b:
            dist_all.append(distance.euclidean(i, j))
    num_of_clusters = len(set(labels))
    composite_list = [dist_all[x:x + num_of_clusters] for x in
                      range(0, len(dist_all), num_of_clusters)]  # Count distance from noise point to each Cluster
    # so len(composite_list)=len(b)=5 there are 5 noise point
    # Count each noise point's shortest cluster, output is the nearest cluster's index
    nearest_cluster_index = []
    for i in range(len(composite_list)):
        list_index = composite_list[i].index(min(composite_list[i]))
        nearest_cluster_index.append(list_index)
    # print noise_points['price']
    # print nearest_cluster_index
    # Count mean & standard diviation for each cluster
    clus_mean = []
    clus_std = []
    for i in range(len(mean_cluster)):
        a = mean_cluster[i][1]
        clus_mean.append(a)
    for i in range(len(set(labels))):
        std = np.array(d_p_l_sort[i]['price']).std()
        clus_std.append(std)
    # Count threthrod
    two_std_from_mean = [x - 2 * y for x, y in zip(clus_mean, clus_std)]
    threthrod = max(two_std_from_mean, 50)
    # print threthrod
    outliers = []
    for i in range(len(noise_points['price'])):
        if noise_points['price'].iloc[i] < threthrod[nearest_cluster_index[i]]:
            outliers.append(flight_data.iloc[noise_points.index[i], :])
            # print noise_points['price'].iloc[i]
    if outliers != []:
        return pd.DataFrame(outliers)
    else:
        return 'no outliers found'


task_3_dbscan(X)


# =========== Task3,Part2 =================
def task_3_IQR(flight_data):
    PriceTags = flight_data['Price_of_TimeRange']
    sorted_Prices = PriceTags.sort_values(axis=0)
    q1 = np.percentile(sorted_Prices, 25)
    q3 = np.percentile(sorted_Prices, 75)  # 855
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = []
    for price in sorted_Prices:
        if price not in range(int(lower_bound), int(upper_bound)):
            outliers.append(price)
    plt.boxplot(sorted_Prices)
    plt.savefig('task_3_iqr.png')


task_3_IQR(X)


# ============= Task4==============
def task_4_dbscan(flight_data):
    d_p_l = pd.DataFrame({
        'date': flight_data['Date_Start'],
        'price': flight_data['Price_of_TimeRange'],
        'z_labels': labels
    })
    # transfer date to index
    for i in range(0, 90):
        d_p_l['date'][i] = i
    # sort date_p_l
    d_p_l_sort = []
    for i in range(-1, len(set(labels)) - 1):
        cluster = d_p_l.loc[d_p_l['z_labels'] == i]  # select rows whose z_labels column equals to i
        d_p_l_sort.append(cluster)
    num_clu_larger_5 = []
    for i in range(1, len(d_p_l_sort)):  # Engore label=-1 which are noise data
        if len(d_p_l_sort[i]) > 5:
            num_clu_larger_5.append(d_p_l_sort[i])
    scale_price = max(d_p_l['price']) - min(d_p_l['price'])
    scale_date = 90
    price_per_clus = []
    for i in range(1, len(set(labels))):
        that_clus_price = pd.DataFrame(d_p_l_sort[i])['price']
        price_per_clus.append(that_clus_price)
    con_5_price = []  # count contiguous set of 5 days
    for i in range(len(price_per_clus)):
        for j in range(0, len(price_per_clus[i]) - 4):
            price_per_clus[i][j:j + 5]
            con_5_price.append(price_per_clus[i][j:j + 5])
            j = j + 1
    price_pairs = []  # every two pair in con_5_price
    for i in range(len(con_5_price)):
        one_pair = itertools.combinations(con_5_price[i], 2)
        price_pairs.append(one_pair)
    global price_pairs
    test = []
    detector = []
    x = 0
    for k in range(len(con_5_price)):
        for i in price_pairs[k]:
            if i[0] - i[1] <= 20 and i[1] - i[0] <= 20:
                detector.append(list(con_5_price[k]))
                k = k + 1
                if k > len(con_5_price) - 1:
                    break
    return detector


task_4_dbscan(X)

