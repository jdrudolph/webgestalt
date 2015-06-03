from subprocess import call
import time
import os

import selenium
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import EMAIL

def click_option(driver, menu, text):
    select = Select(driver.find_element_by_name(menu))
    select.select_by_visible_text(text)

def run(rejected, background, folder='.', name=''):
    """
    run webgestalt GO-enrichment analysis with given rejected and background
    files. Specify folder to save to other location than current.
    >>> rejected = 'test/rej.txt'
    >>> background = 'test/background.txt'
    >>> run(rejected, background, folder='test', name='results')
    """
    rejected = os.path.abspath(rejected)
    background = os.path.abspath(background)
    folder = os.path.abspath(folder)

    driver = selenium.webdriver.Firefox()
    main_window = driver.window_handles[0]
    driver.implicitly_wait(5)
    driver.get('http://bioinfo.vanderbilt.edu/webgestalt')

    start = driver.find_element_by_link_text('START')
    start.click()

    # LOGIN
    login_form = driver.find_element_by_id('loginForm')
    login_form_email = login_form.find_element_by_id('email')
    login_form_email.send_keys(EMAIL)
    time.sleep(1)
    login_form_submit = login_form.find_element_by_name('submit')
    login_form_submit.click()

    # INPUT
    click_option(driver, 'organism', 'hsapiens')
    time.sleep(4)
    click_option(driver, 'idtype', 'hsapiens__entrezgene')
    time.sleep(4)

    inputfile = driver.find_element_by_name('inputfile')
    inputfile.send_keys(rejected)

    enter = driver.find_element_by_css_selector('[value=ENTER]')
    enter.click()

    # ANALYSIS
    id_info = driver.find_element_by_link_text('[Download]')
    call(['wget', '-O', os.path.join(folder, '{}_idinfo.tab'.format(name)),
        id_info.get_attribute('href')])

    analysis_menu = driver.find_element_by_class_name('dropdown')
    analysis_menu.click() # makes options visible
    analysis = driver.find_element_by_link_text('GO Analysis')
    analysis.click()

    refsetfile = driver.find_element_by_name('refsetfile')
    refsetfile.send_keys(background)

    click_option(driver, 'upload_idtype', 'hsapiens__entrezgene')

    submit = driver.find_element_by_css_selector('[value="Run Enrichment Analysis"]')
    submit.click()

    # RESULTS
    driver.switch_to_window(driver.window_handles[1])
    element = WebDriverWait(driver, 100).until(
         EC.presence_of_element_located((By.LINK_TEXT, "View results"))
    )
    element.click()

    driver.switch_to_window(driver.window_handles[2])
    img = driver.find_element_by_tag_name('img')
    img_src = img.get_attribute('src')
    call(['wget', '-O', os.path.join(folder, '{}.gif'.format(name)), img_src])

    for window in driver.window_handles:
        driver.switch_to_window(window)
        driver.close()
