import time
import re

# from Model import DBConnection
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

# init parameters
username = 'ahmshots'
password = '128iu8iu8'
url = 'https://www.instagram.com/'

chrome_driver_path = './chromedriver.exe'
chrome_options = Options()
# chrome_options.add_argument('--headless') --> if enabled the scraper gets error :-|
webdriver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)


def login(get_url, get_username, get_password):
    """logging to Instagram page"""
    try:
        webdriver.get(get_url)
        time.sleep(2)
        webdriver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(get_username)
        webdriver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(get_password)
        webdriver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div').click()
        time.sleep(4)

        # Instagram checks bypass
        try:
            webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
            time.sleep(2)
            webdriver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        finally:
            time.sleep(0.5)
    except:
        webdriver.quit()


def init_profile_crawler():
    """reading last ID in db then write sources link to db"""
    # get last row id:
    try:
        query = 'SELECT parent_id, media, owner FROM socialmedia.info_social_sources;'
        query_result = DBConnection.execute_query(query)
        return query_result
    except:
        print('ERROR: INIT_Profile_crawler')
    finally:
        pass


def post_profile_crawler():
    """crawling in persons profile"""
    # get last row id:
    try:
        query = 'SELECT source_id, source FROM socialmedia.raw_data_source order by source_id;'
        query_result = DBConnection.execute_query(query)
        return query_result
    except:
        print('ERROR: Post_Profile_crawler')
    finally:
        pass


def extract_link_to_db(page_links, owner):
    """reading last ID in db then write sources link to db"""
    max_id = 0
    counter = 0
    # get last row id:
    try:
        query = 'select max(source_id) from socialmedia.raw_data_source'
        query_result = DBConnection.execute_query(query)
        if len(query_result) != 0:
            for row in query_result:
                max_id = row[0] + 1
        else:
            max_id = 1
    except Exception as error:
        print('Error in reading:', error)

    # export to DB
    output_list = {
        'page_links': list(page_links),
        'owner': list(owner)
    }
    print(output_list)
    query = 'insert into socialmedia.raw_data_source values (%s,%s,%s)'
    try:
        while counter < len(output_list['page_links']):
            DBConnection.write_query(query, max_id, output_list['page_links'][counter], output_list['owner'][counter])
            max_id += 1
            counter += 1
            if counter % 500 == 0:
                time.sleep(7)
    except Exception as error:
        print('Error in Writing:', error)


def extract_raw_data_to_db(source_id, extracted_account, extracted_comments, extracted_date):
    """reading last ID in db then write sources link to db"""
    max_id = 0
    counter = 0
    # get last row id:
    try:
        query = 'select max(post_id) from socialmedia.raw_data_entry'
        query_result = DBConnection.execute_query(query)
        if len(query_result) != 0:
            for row in query_result:
                max_id = row[0] + 1
        else:
            max_id = 1
    except:
        print('ERROR: Database Reading')
    finally:
        pass

    # export to DB
    output_list = {
        'comment': list(extracted_comments),
        'owner': list(source_id),
        'username': list(extracted_account),
        'date': list(extracted_date),
    }
    query = 'insert into socialmedia.raw_data_entry values (%s,%s,%s,%s,%s)'
    try:
        while counter < len(output_list['owner']):
            DBConnection.write_query(query, max_id,
                                     output_list['comment'][counter],
                                     output_list['username'][counter],
                                     output_list['date'][counter],
                                     output_list['owner'][counter])
            max_id += 1
            counter += 1
    except Exception as exception:
        print(exception)
        print('ERROR: Database Writing')
    finally:
        pass


def update_number_of_post_like(like, source_id):
    """update instagram post likes"""
    owner = source_id
    likes = like

    query = 'UPDATE socialmedia.raw_data_source SET  post_likes = %s WHERE source_id = %s'
    try:
        DBConnection.update_query(query, likes, owner)
    except:
        print("ERROR: Cant update current record")


def scroll_to_bottom(driver):
    old_position = 0
    new_position = None

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
            ('return (window.pageYOffset !== undefined) ?'
             ' window.pageYOffset : (document.documentElement ||'
             ' document.body.parentNode || document.body);'))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
            'var scrollingElement = (document.scrollingElement ||'
            ' document.body);scrollingElement.scrollTop ='
            ' scrollingElement.scrollHeight;'))
        # Get new position
        new_position = driver.execute_script(
            ('return (window.pageYOffset !== undefined) ?'
             ' window.pageYOffset : (document.documentElement ||'
             ' document.body.parentNode || document.body);'))
        time.sleep(1)


def page_scraper():
    """try to extract links from user profile"""
    try:
        working_links = init_profile_crawler()
        print(working_links)
        for row in working_links:

            counter = 0
            links = set()
            parent_id = []

            page_url = 'https://www.' + row[1] + '.com/' + row[2] + '/'
            webdriver.get(page_url)
            webdriver.maximize_window()
            time.sleep(3)

            # page scrolling
            old_position = 0
            new_position = None

            while new_position != old_position:

                result = webdriver.find_elements_by_tag_name('a')
                for itt in result:
                    profile_link = itt.get_attribute('href')
                    if '.com/p/' in profile_link:
                        links.add(profile_link)
                        # parent_id.append(row[0])
                # Get old scroll position
                old_position = webdriver.execute_script(
                    ('return (window.pageYOffset !== undefined) ?'
                     ' window.pageYOffset : (document.documentElement ||'
                     ' document.body.parentNode || document.body);'))
                # Sleep and Scroll
                time.sleep(2)
                webdriver.execute_script((
                    'var scrollingElement = (document.scrollingElement ||'
                    ' document.body);scrollingElement.scrollTop ='
                    ' scrollingElement.scrollHeight;'))
                # Get new position
                new_position = webdriver.execute_script(
                    ('return (window.pageYOffset !== undefined) ?'
                     ' window.pageYOffset : (document.documentElement ||'
                     ' document.body.parentNode || document.body);'))
                time.sleep(1)

            result = webdriver.find_elements_by_tag_name('a')
            for itt in result:
                profile_link = itt.get_attribute('href')
                if '.com/p/' in profile_link:
                    links.add(profile_link)

            for count in links:
                parent_id.append(row[0])
                counter += 1
            try:
                time.sleep(1)
                extract_link_to_db(links, parent_id)
            except:
                print('ERROR: DB Output Error')
            time.sleep(2)
    except:
        print('ERROR: Scrapping encounter Problem')
        return False
    finally:
        time.sleep(2)
        webdriver.quit()
    return links, parent_id


def check_exists_by_xpath(xpath):
    try:
        webdriver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def get_comments():
    """this method tries to fetch all comments of instagram link."""

    query_result = post_profile_crawler()
    for item in query_result:
        extracted_date = []
        extracted_account = []
        source_id_itt = []
        extracted_comments = []
        source_id = item[0]
        page_url = item[1]

        webdriver.get(page_url)
        time.sleep(2)
        try:
            while check_exists_by_xpath('//div/ul/li/div/button'):
                time.sleep(1)
                webdriver.find_element_by_xpath('//div/ul/li/div/button').click()
                time.sleep(1)
        except:
            pass
        try:
            # it cannot show nested comments and the problem is related to xpath syntax :-|
            while check_exists_by_xpath('//*[contains(text(), "View replies")]'):
                webdriver.find_element_by_xpath('//*[contains(text(), "View replies")]').click()
                time.sleep(1)
        except:
            pass

        time.sleep(2)
        soup = BeautifulSoup(webdriver.page_source, 'html.parser')
        comments = soup.find_all('div', attrs={'class': 'C4VMK'})
        soup_2 = BeautifulSoup(str(comments), 'html.parser')

        # extract comments
        re_comments = soup_2.find_all('span', attrs={'class': ''})
        str_comments = str(re_comments).split('>')
        extracted_comments.append('Caption')
        for comments_list in str_comments:
            matched = re.search('^.*</span$', comments_list)
            if matched:
                tag_remove = matched.group()
                str_tag_remove = tag_remove.split('</span')
                for itt in str_tag_remove:
                    if itt:
                        extracted_comments.append(itt)

        # extracts date
        date = soup.find_all('time', attrs={'class': 'FH9sR Nzb55'})
        str_date = str(date).split('"')
        for date_list in str_date:
            date_match = re.search('^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01]).([0-1]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]*', date_list)
            #time_match = re.search('([0-1]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]*', date_list)
            if date_match:
                dates = re.sub('[T]', ' ', date_match.group())
                extracted_date.append(dates)

        # extract username
        account = soup_2.find_all('a', attrs={'class': 'sqdOP yWX7d _8A5w5 ZIAjV'})
        str_account = str(account).split('>')
        for account_list in str_account:
            matched = re.search('^.*</a$', account_list)
            if matched:
                tag_remove = matched.group()
                str_tag_remove = tag_remove.split('</a')
                for itt in str_tag_remove:
                    if itt:
                        extracted_account.append(itt)
                        source_id_itt.append(source_id)
        print('Lenght of comment is: ', len(source_id_itt))
        try:
            extract_raw_data_to_db(source_id_itt, extracted_account, extracted_comments, extracted_date)
        except:
            print("ERROR: DB Writing")
    webdriver.quit()


def get_likes():
    query_result = post_profile_crawler()
    for item in query_result:
        source_id = item[0]
        page_url = item[1]
        extracted_likes = 0
        webdriver.get(page_url)
        time.sleep(2)
        try:
            if check_exists_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div/span'):
                time.sleep(1)
                webdriver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div/span').click()
        except:
            if check_exists_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div/div/button'):
                time.sleep(1)
                webdriver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[2]/div/div/button').click()
        else:
            pass
        finally:
            soup = BeautifulSoup(webdriver.page_source, 'html.parser')
            likes_pics = soup.find_all('div', attrs={'class': 'Nm9Fw'})
            likes_videos = soup.find_all('div', attrs={'class': 'vJRqr'})
            likes_videos.append(soup.find_all('div', attrs={'class': 'vcOH2'}))
            likes = likes_pics + likes_videos
            str_likes = str(likes).split('>')
            for like_itt in str_likes:
                tag_remove = []
                matched = re.search('^.*</span$', like_itt)
                if matched:
                    tag_remove = matched.group().split('</span')
                else:
                    new_match = re.search('^.*like</button$', like_itt)
                    if new_match:
                        tag_remove = new_match.group().split(' like</button')
                for itt in tag_remove:
                    if itt:
                        like = str(itt)
                        extracted_likes = int(like.replace(',', ''))

        try:
            update_number_of_post_like(extracted_likes, source_id)
        except Exception as error:
            print('ERROR: Getting likes raises Error', error)
    webdriver.quit()


login(url, username, password)
if __name__ == '__main__':
    page_scraper()
    time.sleep(2)
    login(url, username, password)
    # get_comments()
    print('finished')

