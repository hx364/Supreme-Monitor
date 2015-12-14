import time
import sys
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import gmtime, strftime
import json


def check_item(item, name):
    l = item.find_element_by_tag_name('a')
    link = l.get_attribute('href')
    
    if name in link:
        print "Item found"
        try:
            l.find_element_by_class_name("sold_out_tag")
            print "Sold Out"
            return False
        except:
            return True
    else:                    
        return False
    
    

def filter_items(items, name):
    for i in range(len(items)):
#         print "---------Scan Item %i ---------" %(i+1)
        if check_item(items[i], name):
            return items[i]

    print "sorry, no item found"
    return False
    
def pick_size(size):
    #size: Small, Medium, Large, XLarge
    size_component = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "size")))
    size_list = size_component.find_elements_by_tag_name('option')
    flag = False
    for i in size_list:
        if i.get_attribute("text") == size:
            print "Found the %r size" %size
            i.click()
            return True
    if not flag:
        print "%r size sold out" %size
        return False


def check_cart():
    s = driver.find_element_by_name('commit')
    s.click()
    l1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "cart")))
    l2 = l1.find_elements_by_tag_name('a')
    l3 = l2[0]
    l3.click()
    
    try:
        s = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart-description")))
        driver.save_screenshot("cart.png")
        flag2 = True
    except:
        print "Can't load into the cart page"
        return False
    
    if flag2:
        print "You are Going to buy:"
        print s.text
        s1 = driver.find_element_by_id('cart-footer')
        s2 = s1.find_elements_by_tag_name('a')
        for i in s2:
            if i.text == "checkout now":
                i.click()
                return True
        driver.save_screenshot("checkout.png")
        return False


def fill_form(options):
    #filling form in the payent page
    s1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "order_billing_name")))
    s1.send_keys(options["order_billing_name"])
    for i in options:
        s = driver.find_element_by_id(i)
        try:
            s.clear()
        except:
            continue
        s.send_keys(options[i])
    i = driver.find_element_by_id("order_terms")
    i.click()

def submit():
    l = driver.find_elements_by_name("commit")
    l.click()
    driver.quit()

def go_supreme(item_name, size):
    global driver
    profile = webdriver.FirefoxProfile()
    profile.set_preference("dom.max_script_run_time", 0)
    driver = webdriver.Firefox(firefox_profile = profile)
    
    
    print "Open Supreme and scan Items"
    driver.get("http://www.supremenewyork.com/shop/all")
    clothes_list = driver.find_element_by_id("container")
    items = clothes_list.find_elements_by_class_name("inner-article")
    l = filter_items(items, item_name)
    
    if not l:
        driver.quit()
        return False
    else:
        l.click()
        print driver.current_url
        l2 = pick_size(size)
        if not l2:
            driver.quit()
            return False
        else:
            l3 = check_cart()
            if not l3:
                driver.quit()
                return False
            else:
                with open('options.json') as data_file:    
                    options = json.load(data_file)
                fill_form(options)
                # submit()
                # driver.quit()
                print "You have it!"
                return True


def monitor(item_name, size, sleep_seconds=30):
    """
    This is to monitor the website
    Once it's in stock, will try to buy one
    In caution to use this one, sometimes they may ban your connection
    """
    error=0
    I_HAVE_IT = False
    itereation = 1 
    while error<3:
        try:
            while not I_HAVE_IT:
                print "%3d  %r" %(iteration, strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
                I_HAVE_IT = go_supreme(item_name, size)
                iteration+=1
                time.sleep(sleep_seconds)
        except:
            print (sys.exc_info())
            error+=1
            continue


def main():
    item_name = 'quilted-flight-satin-parka/orange'
    size = "Small"
    #go_supreme(item_name, size)
	monitor(item_name, size)

if __name__ == "__main__":
    main()
    

