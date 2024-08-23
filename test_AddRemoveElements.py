import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


@pytest.fixture
def setup(environment_details):
    print("Setting up...")
    driver = webdriver.Firefox()
    driver.get(environment_details)
    yield driver
    print("Tearing down...")
    driver.close()

def test_click_add_remove_elements(setup):
    setup.find_element(By.LINK_TEXT,"Add/Remove Elements").click()
    setup.find_element(By.XPATH,"//*[contains(text(),'Add Element')]").click()
    setup.find_element(By.XPATH,"//*[contains(text(),'Delete')]")

def test_basic_auth(setup):
    setup.get("https://admin:admin@the-internet.herokuapp.com/basic_auth")
    message = setup.find_element(By.XPATH,"//p").text
    congrats = message.startswith("Congratulations")
    assert congrats

def test_broken_images(setup):
    setup.find_element(By.LINK_TEXT,"Broken Images").click()
    color = setup.find_element(By.XPATH,"//img[@src='asdf.jpg']").get_attribute("color")
    if color == None:
        print("Image is blank")

def test_challenging_dom(setup):
    setup.find_element(By.LINK_TEXT,"Challenging DOM").click()
    rows = setup.find_elements(By.XPATH,"//table/tbody/tr")
    for row in rows:
        column_eight = row.find_element(By.XPATH,"td[7]")
        column_eight.find_element(By.LINK_TEXT,"edit").click()

def test_checkboxes(setup):
    setup.find_element(By.LINK_TEXT,"Checkboxes").click()
    checkboxes = setup.find_elements(By.XPATH,"//*[@id='checkboxes']/child::input")
    for cbox in checkboxes:
        if cbox.get_attribute("checked") == None:
            cbox.click()

def test_context_menu(setup):
    setup.find_element(By.LINK_TEXT,"Context Menu").click()
    element = setup.find_element(By.XPATH,"//*[@id='hot-spot']")
    ActionChains(setup).context_click(element).perform()
    setup.switch_to.alert.accept()

def test_disappearing_elements(setup):
    setup.find_element(By.LINK_TEXT,"Disappearing Elements").click()
    elements = setup.find_elements(By.XPATH,"//ul/child::li")
    for e in elements:
        print(e.text)

def test_drag_and_drop(setup):
    setup.find_element(By.LINK_TEXT,"Drag and Drop").click()
    source = WebDriverWait(setup,20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='column-a']")))
    target = WebDriverWait(setup,20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='column-b']")))
    ActionChains(setup).drag_and_drop(source,target).perform()

def test_dynamic_content(setup):
    setup.find_element(By.LINK_TEXT,"Dynamic Content").click()
    images = setup.find_elements(By.XPATH,"//*[@class='large-10 columns large-centered']/div/div/child::img")
    texts = setup.find_elements(By.XPATH,"//*[@class='large-10 columns large-centered']/div/div/child::img/following::div[@class='large-10 columns']")
    size = len(images)

    for img in images:
        print(img.get_attribute("src"))

    for t in texts:
        print(t.text)

def test_dynamic_controls(setup):
    setup.find_element(By.LINK_TEXT,"Dynamic Controls").click()
    cbox_status = setup.find_element(By.ID,"checkbox").get_attribute("checked")
    if cbox_status == None:
        setup.find_element(By.ID,"checkbox").click()
    setup.find_element(By.XPATH,"//button[text()='Remove']").click()

    tbox_status = setup.find_element(By.XPATH,"//*[@id='input-example']/child::input").get_attribute("disabled")
    if tbox_status == "true":
        setup.find_element(By.XPATH,"//button[text()='Enable']").click()

    wait = WebDriverWait(setup,20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='input-example']/child::input")))
    setup.find_element(By.XPATH,"//*[@id='input-example']/child::input").click()
    setup.find_element(By.XPATH, "//*[@id='input-example']/child::input").send_keys("Entering text")

def test_dynamic_loading(setup):
    setup.find_element(By.LINK_TEXT,"Dynamic Loading").click()
    setup.find_element(By.LINK_TEXT,"Example 1: Element on page that is hidden").click()
    hidden_element = setup.find_element(By.XPATH,"//*[@id='finish']")
    display_status = setup.find_element(By.XPATH,"//*[@id='finish']").get_attribute("style")
    comp = display_status == 'display: none;'
    if display_status == 'display: none;':
        setup.execute_script("arguments[0].setAttribute('style','display: block;')",hidden_element)
    wait = WebDriverWait(setup,20).until(EC.presence_of_element_located((By.XPATH,"//*[@id='finish']")))

