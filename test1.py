import bs4
import requests
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#
# url="https://www.youtube.com/channel/UCOhHO2ICt0ti9KAh-QHvttQ/videos"
# data=requests.get(url)
# soup=bs4.BeautifulSoup(data.text,'html.parser')
#
# for links in soup.find_all('a'):
#     #link=links.get('class')
#     print(''.join(links.findAll(text=True)))
#     # print(links)
#     # if links=="yt-simple-endpoint style-scope ytd-grid-video-renderer":
#     #     print("https://www.youtube.com"+links)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from time import sleep
import csv
import re
from datetime import datetime
#New line added
#I have created new branch name change1 and I am testing it now.
print("Hello World")
app = QtWidgets.QApplication([])
dlg = uic.loadUi("C:\\Users\DELL\.PyCharm2019.2\config\scratches\WebScraping\home.ui")
dlg2 = uic.loadUi("C:\\Users\DELL\.PyCharm2019.2\config\scratches\WebScraping\display.ui")
global flagout
flagout = 0
dlg2.data_tw.setColumnWidth(0, 240)
dlg2.data_tw.setColumnWidth(1, 100)
dlg2.data_tw.setColumnWidth(2, 150)
dlg2.data_tw.setColumnWidth(3, 150)
dlg2.data_tw.setColumnWidth(4, 230)
dlg2.data_tw.setColumnWidth(5, 200)
dlg2.data_tw.setColumnWidth(6, 150)
dlg2.data_tw.setColumnWidth(7, 120)


def fetch():
    try:
        QApplication.processEvents()
        clearData()
        flagout = 1
        if flagout == 1:
            dlg.hide()  # hide the main window
        # for n in range(100):
        #     sleep(0.1)
        #     QApplication.processEvents()
        QApplication.processEvents()
        global searchkey
        searchkey = dlg.searchbar_le.text()
        count = 0
        if searchkey:
            print(searchkey)
        else:
            searchkey = "hospitals in vadodara"
        flagcount = 0
        countkey = dlg.count_le.text()
        if countkey:
            print(countkey)
            countkey = int(countkey)
            flagcount = 1
        else:
            countkey = 20

        # date = datetime.now()
        # new_date_time = str(date.year) + str(date.month) + str(date.day) + str(date.hour) + str(date.minute) + str(
        #     date.second)
        # writer = csv.writer(open(str(searchkey) + "_" + new_date_time + '.csv', 'w', newline=''))
        # a = "Name"
        # b = "Rating"
        # c = "No. of People Rated"
        # d = "Category"
        # e = "Address"
        # f = "Plus Code"
        # g = "Website"
        # h = "Contact No."
        # writer.writerow(
        #     [a.encode("UTF-8"), b.encode("UTF-8"), c.encode("UTF-8"), d.encode("UTF-8"), e.encode("UTF-8"),
        #      f.encode("UTF-8"),
        #      g.encode("UTF-8"), h.encode("UTF-8")])

        chromedriver = r'C:\Users\DELL\.PyCharm2019.2\config\scratches\WebScraping\chromedriver'
        driver = webdriver.Chrome(executable_path=chromedriver)
        # driver.set_window_position(-10000, 0)     #hide the webdriver
        driver.get("https://www.google.com/maps")

        sleep(3)
        search_query = driver.find_element_by_name('q')
        search_query.send_keys(searchkey)
        sleep(1)
        # driver.find_element_by_xpath('//*[@class="searchbox-searchbutton"]').click()
        search_query.send_keys(Keys.RETURN)
        sleep(3)
        print(driver.current_url)
        sleep(1)
        c = 0
        row_number = 0
        while True:
            QApplication.processEvents()
            sel = Selector(text=driver.page_source)
            a = sel.xpath('//*[@class="section-result-title"]/span/text()').extract()
            print(a)

            sleep(2)
            for i in a:
                QApplication.processEvents()
                z = re.match("^\"", str(i))
                if bool(z):
                    i = i.split("\"")[1]
                    # i="\""+str(i)+"\""
                    print(i)
                    print("It passed")
                    continue
                    # driver.find_element_by_xpath('//*[@class="section-result-title"]/span[text()="' + str(i) + '"]').click()
                    # driver.find_element_by_xpath('//*[@class="section-result-title"]/span[text()="+ "\"" + str(i) + "\"" + "]').click()
                else:
                    driver.find_element_by_xpath(
                        '//*[@class="section-result-title"]/span[text()="' + str(i) + '"]').click()
                sleep(3)
                sel = Selector(text=driver.page_source)
                name = sel.xpath(
                    '//*[@class="section-hero-header-title-title GLOBAL__gm2-headline-5"]/text()').extract()
                "GLOBAL__gm2-headline-5 section-hero-header-title-title"
                rating = sel.xpath('//*[@class="section-star-display"]/text()').extract()
                information = sel.xpath('//*[@class="widget-pane-link"]/text()').extract()

                print(name[0])
                if rating:
                    print(rating[0])
                else:
                    rating.insert(0, "NULL")
                length = len(information)
                for i in range(0, length):
                    print(information[i])

                flag3 = 0
                for j in information:
                    x = re.search("^\(.*\)$", j)
                    if x:
                        print("It passed")
                        flag3 = 1
                if flag3 == 0:
                    information.insert(0, "NULL")
                    print("Updated List:" + str(information))

                flag2 = 0
                for k in information:
                    y = re.search("^....\+.+$", k)
                    if y:
                        print("It passed")
                        flag2 = 1
                if flag2 == 0:
                    information.insert(3, "NULL")  # changed before 1
                    print("Updated List!!!!:" + str(information))

                for l in information:
                    z = re.match("^Located in: \w+", l)
                    if bool(z):
                        information.remove(l)
                        print("It passed")

                if "Add website" in information:
                    information.insert(4, "NULL")
                    information.remove("Add website")

                if "Add phone number" in information:
                    information.insert(5, "NULL")
                    information.remove("Add phone number")

                sleep(1)
                print(information)
                # writer.writerow([name[0].encode('utf-8'), rating[0].encode('utf-8'), information[0].encode('utf-8'),
                #                  information[1].encode('utf-8'), information[2].encode('utf-8'),
                #                  information[3].encode('utf-8'),
                #                  information[4].encode('utf-8'), information[5].encode('utf-8')])
                count += 1
                # dlg.results_lbl.setText("Count: "+str(count))
                print("Count: " + str(count))
                if len(information) == 5:
                    information.insert(1, "0")
                dlg2.show()
                users = (name[0], rating[0], information[0],
                         information[1], information[2],
                         information[3],
                         information[4], information[5])
                # for row_number, user in enumerate(users):
                #     dlg2.data_tw.insertRow(row_number)
                #     print(row_number)
                #     print(user)

                dlg2.data_tw.insertRow(row_number)
                for column_number, data in enumerate(users):
                    QApplication.processEvents()
                    cell = QtWidgets.QTableWidgetItem(str(data))
                    dlg2.data_tw.setItem(row_number, column_number, cell)
                row_number += 1
                dlg2.count_lbl.clear()

                dlg2.count_lbl.setText("Count: " + str(count))

                sleep(2)
                QApplication.processEvents()
                driver.find_element_by_xpath('//*[@class="section-back-to-list-button blue-link noprint"]').click()
                print("\n\n")
                sleep(2)
                c += 1
                if flagcount == 1:
                    if c == countkey:
                        break
            if flagcount == 1:
                if c == countkey:
                    dlg2.results_lbl.setText("Data have been fetched")
                    dlg.searchbar_le.clear()
                    dlg.count_le.clear()
                    driver.close()
                    dlg.show()
                    break
            QApplication.processEvents()
            chek = driver.find_element_by_xpath('//*[@id="n7lv7yjyC35__section-pagination-button-next"]')
            print("check:" + str(chek.is_enabled()))
            if chek.is_enabled():
                print("Continuing the fetching process")
                driver.find_element_by_xpath('//*[@id="n7lv7yjyC35__section-pagination-button-next"]').click()
            else:
                print("All results are fetched")
                dlg2.results_lbl.setText("Data have been fetched")
                dlg.searchbar_le.clear()
                dlg.count_le.clear()
                driver.close()
                dlg.show()
                break

            # noresult=driver.find_element_by_xpath('//*[@class="section-no-result-title"]/text()').extract()
            # if noresult:
            #     break
            # else:
            #     pass
            sleep(4)
    except Exception as e:
        print(e)


def clearData():
    dlg2.data_tw.clearSelection()
    while dlg2.data_tw.rowCount() > 0:
        dlg2.data_tw.removeRow(0)
        dlg2.data_tw.clearSelection()


def saveData():
    date = datetime.now()
    new_date_time = str(date.year) + str(date.month) + str(date.day) + str(date.hour) + str(date.minute) + str(
        date.second)
    writer = csv.writer(open(
        "C:\\Users\DELL\.PyCharm2019.2\config\scratches\WebScraping\\" + str(searchkey) + "_" + new_date_time + '.csv',
        'w',encoding="utf-8", newline=''))
    a = b"Name"
    b = b"Rating"
    c = b"No. of People Rated"
    d = b"Category"
    e = b"Address"
    f = b"Plus Code"
    g = b"Website"
    h = b"Contact No."
    writer.writerow(
        [a.decode(), b.decode(), c.decode(), d.decode(), e.decode(),
         f.decode(),
         g.decode(), h.decode()])
    row = dlg2.data_tw.rowCount()
    try:
        for i in range(row):
            item1 = dlg2.data_tw.item(i, 0)
            name = item1.text()
            item2 = dlg2.data_tw.item(i, 1)
            rating = item2.text()
            item3 = dlg2.data_tw.item(i, 2)
            people_rated = item3.text()
            item4 = dlg2.data_tw.item(i, 3)
            category = item4.text()
            item5 = dlg2.data_tw.item(i, 4)
            address = item5.text()
            item6 = dlg2.data_tw.item(i, 5)
            plus_code = item6.text()
            item7 = dlg2.data_tw.item(i, 6)
            website = item7.text()
            item8 = dlg2.data_tw.item(i, 7)
            contact_no = item8.text()
            if people_rated == "NULL":
                people_rated_new = "NULL"
            else:
                s1 = people_rated.split('(')[1]
                people_rated_new = s1.split(')')[0]
            writer.writerow([name, rating, people_rated_new, category, address, plus_code, website, contact_no])
        dlg2.results_lbl.setText("Data has been saved")
    except Exception as e:
        print(e)


def googleData():
    date = datetime.now()
    new_date_time = str(date.year) + str(date.month) + str(date.day) + str(date.hour) + str(date.minute) + str(
        date.second)
    writer = csv.writer(open(
        "C:\\Users\DELL\.PyCharm2019.2\config\scratches\WebScraping\\" + "google_data_" + str(
            searchkey) + "_" + new_date_time + '.csv',
        'w', newline=''))
    a = b"Name"
    b = b"Given Name"
    c = b"Additional Name"
    d = b"Family Name"
    e = b"Yomi Name"
    f = b"Given Name Yomi"
    g = b"Additional Name Yomi"
    h = b"Family Name Yomi"
    i = b"Name Prefix"
    j = b"Name Suffix"
    k = b"Initials"
    l = b"Nickname"
    m = b"Short Name"
    n = b"Maiden Name"
    o = b"Birthday"
    p = b"Gender"
    q = b"Location"
    r = b"Billing Information"
    s = b"Directory Server"
    t = b"Mileage"
    u = b"Occupation"
    v = b"Hobby"
    w = b"Sensitivity"
    x = b"Priority"
    y = b"Subject"
    z = b"Notes"
    aa = b"Language"
    ab = b"Photo"
    ac = b"Group Membership"
    ad = b"E-mail 1 - Type"
    ae = b"E-mail 1 - Value"
    af = b"Phone 1 - Type"
    ag = b"Phone 1 - Value"
    ah = b"Phone 2 - Type"
    ai = b"Phone 2 - Value"
    aj = b"Address 1 - Type"
    ak = b"Address 1 - Formatted"
    al = b"Address 1 - Street"
    am = b"Address 1 - City"
    an = b"Address 1 - PO Box"
    ao = b"Address 1 - Region"
    ap = b"Address 1 - Postal Code"
    aq = b"Address 1 - Country"
    ar = b"Address 1 - Extended Address"
    arr = b"Organization 1 - Type"
    at = b"Organization 1 - Name"
    au = b"Organization 1 - Yomi Name"
    av = b"Organization 1 - Title"
    aw = b"Organization 1 - Department"
    ax = b"Organization 1 - Symbol"
    ay = b"Organization 1 - Location"
    az = b"Organization 1 - Job Description"
    ba = b"Website 1 - Type"
    bb = b"Website 1 - Value"

    writer.writerow(
        [a.decode(), b.decode(), c.decode(), d.decode(), e.decode(),
         f.decode(),
         g.decode(), h.decode(), i.decode(), j.decode(), k.decode(), l.decode(), m.decode(), n.decode(), o.decode(),
         p.decode(), q.decode(), r.decode(), s.decode(), t.decode(), u.decode(), v.decode(), w.decode(), x.decode(),
         y.decode(), z.decode(), aa.decode(), ab.decode(), ac.decode(), ad.decode(), ae.decode(), af.decode(),
         ag.decode(), ah.decode(), ai.decode(), aj.decode(), ak.decode(), al.decode(), am.decode(), an.decode(),
         ao.decode(), ap.decode(), aq.decode(), ar.decode(), arr.decode(), at.decode(), au.decode(), av.decode(),
         aw.decode(), ax.decode(), ay.decode(), az.decode(), ba.decode(), bb.decode()])
    row = dlg2.data_tw.rowCount()
    try:
        for i in range(row):
            item1 = dlg2.data_tw.item(i, 0)
            name = item1.text()
            item2 = dlg2.data_tw.item(i, 1)
            rating = item2.text()
            item3 = dlg2.data_tw.item(i, 2)
            people_rated = item3.text()
            item4 = dlg2.data_tw.item(i, 3)
            category = item4.text()
            item5 = dlg2.data_tw.item(i, 4)
            address = item5.text()
            item6 = dlg2.data_tw.item(i, 5)
            plus_code = item6.text()
            item7 = dlg2.data_tw.item(i, 6)
            website = item7.text()
            item8 = dlg2.data_tw.item(i, 7)
            contact_no = item8.text()
            if people_rated == "NULL":
                people_rated_new = ''
            else:
                s1 = people_rated.split('(')[1]
                people_rated_new = s1.split(')')[0]
            writer.writerow(
                ['', name, "Rating:" + rating + ", People Rated:" + people_rated_new + ", Category:" + category, '', '',
                 '', '', '', '', '', '', '', '', '', '', '', plus_code, '', '', '', '', '', '', '', '', '', '', '', '',
                 '', '', '', contact_no, '', '', '', address, '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                 '', '', website])
        dlg2.results_lbl.setText("Data has been saved")
    except Exception as e:
        print(e)


def close():
    dlg2.close()


dlg.search_pb.pressed.connect(fetch)
# dlg.open_pb.pressed.connect(open_file)
dlg2.save_pb.pressed.connect(saveData)
dlg2.save_pb.pressed.connect(googleData)
dlg2.cancel_pb.pressed.connect(close)

dlg.show()
app.exec()

# h=sel.xpath('//*[@class="section-filter-user-rating-at-least"]/text()').extract()
# print(h)
# driver.find_element_by_xpath('//*[@class="section-result-title"]/span[text()="Tricolour Hospitals"]').click()
# sleep(3)

# next_page = driver.find_element_by_xpath('//span[text()="Sunshine Global Hospitals"]')
# next_page.click()
# name=sel.xpath('//*[@class="GLOBAL__gm2-headline-5 section-hero-header-title-title"]/text()').extract()
# rating=sel.xpath('//*[@class="section-star-display"]/text()').extract()
# no_of_people_rated=sel.xpath('//*[@class="widget-pane-link"]/text()').extract()

# print(name[0])
# print(rating[0])
# length=len(no_of_people_rated)
# for i in range(0,length):
#     print(no_of_people_rated[i])
#
# sleep(1)
# driver.find_element_by_xpath('//*[@class="section-back-to-list-button blue-link noprint"]').click()
