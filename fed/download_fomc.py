# import mechanize
#
# br = mechanize.Browser()
# #br.set_all_readonly(False)    # allow everything to be written to
# br.set_handle_robots(False)   # ignore robots
# br.set_handle_refresh(False)  # can sometimes hang without this
# br.addheaders = [('User-agent', 'Firefox')]

url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"
# response = br.open(url)
# # print(response.read() )     # the text of the page
# response1 = br.response()  # get the response again
# print(response1.read() )    # can apply lxml.html.fromstring()
# br.form = list(br.forms())[-1]
# print(br.form)
# for control in br.form.controls:
#     print(control)
    # print("type=%s, name=%s value=%s" % (control.type, control.name, br[control.name]))
# br.select_form(nr=0)
# for form in br.forms():
#     print("Form name:%s"%form.name)
#     print(form)
import time
from selenium import webdriver
driver = webdriver.Firefox()
driver.get(url)
# loginForm = driver.find_element_by_id("user_area")
time.sleep(15)
driver.find_element_by_xpath(
    ".//input[@aria-label='Checkbox for Monetary Policy']"
).click()
driver.find_element_by_xpath(
    ".//div[@class='eventSearch__submit']"
).click()

elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
    print(elem.get_attribute("href"))

for i in range(10000):
    driver.find_element_by_xpath(
        "//a[text() = 'Next']"
    ).click()
    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        print(elem.get_attribute("href"))
    time.sleep(2)

        # loginLink = loginForm.find_element_by_tag_name("a")
# webdriver.ActionChains(driver).move_to_element(loginLink).perform()
# email = driver.find_element_by_id('username')
# email.send_keys('my_email')
# passwd = driver.find_element_by_id('passwd')
# passwd.send_keys('my_pass')
# button = loginForm.find_element_by_class_name("loginButton")
# webdriver.ActionChains(driver).move_to_element(button).click().perform()

# <div class="eventSearch__submit" ng-click="changeValue()"><a href="#">Submit<span class="icon icon__sm icon--right icon-more"></span></a></div>
# <input type="checkbox" aria-label="Checkbox for Monetary Policy" checklist-value="value"
#  ng-model="checked" class="ng-scope ng-pristine ng-untouched ng-valid ng-not-empty">