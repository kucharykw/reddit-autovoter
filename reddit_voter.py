import json  # for reading my login and password
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


def log_in(username, password):
    """If not loggen in already, log in using form located on the right side then wait 10 seconds."""
    try:
        login_form = driver.find_element_by_id('login_login-main')

        username_tbox = login_form.find_element_by_name('user')
        username_tbox.clear()
        username_tbox.send_keys(username)

        password_tbox = login_form.find_element_by_name('passwd')
        password_tbox.clear()
        password_tbox.send_keys(password)

        submit = login_form.find_element_by_class_name('btn')
        submit.click()
        print('Succesfully logged in as user {}'.format(username))

    except NoSuchElementException:
        print('User already logged in.')

def allow_cookies():
    """Accept cookies if a window is visible. If not, pass."""
    try:
        cookies_form = driver.find_element_by_id('eu-cookie-policy')
        cookies_button = cookies_form.find_element_by_class_name(
            'infobar-btn-container')
        cookies_button.click()
        print('Cookies allowed.')
    except NoSuchElementException:
        print('Cookies pop-up not visible.')
        pass

def vote_subreddit(subreddit, vote, n_pages=1):
    """Go to subreddit and upvote or downvote all posts on first page (n_pages added for future extension).
    Accepted subreddit formats are e.g. 'r/funny' or full URL, i.e. 'https://old.reddit.com/r/funny/'.
    Set vote to either vote='upvote' or vote='downvote'.
    """
    if subreddit.startswith('https://old.reddit.com'):
        url = subreddit
    elif subreddit.startswith('r/'):
        url = 'https://old.reddit.com/{}/'.format(subreddit)
    else:
        print('Incorrect subreddit format given. Aborting.')
        return

    driver.get(url)
    driver.implicitly_wait(10)

    allow_cookies()
    log_in(login['username'], login['password'])
    time.sleep(10)

    if vote == 'upvote':
        arrows = driver.find_elements_by_css_selector('div.arrow.up')
    elif vote == 'downvote':
        arrows = driver.find_elements_by_css_selector('div.arrow.down')

    driver.implicitly_wait(10)
    for arrow in arrows:
        arrow.click()
    print('Page {}ed succesfully.'.format(vote))


# Read my login and password from file
login_file = 'login.json'
with open(login_file, 'r') as f_obj:
    login = json.load(f_obj)
    print('Succesfully read user {} login data.'.format(login['username']))

driver = webdriver.Firefox()
vote_subreddit('r/funny', 'downvote', 1)
