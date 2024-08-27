import pytest
from selenium import webdriver
from selenium.common import MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ait
import time


@pytest.fixture
def setup(environment_details):
    print("Setting up...")
    driver = webdriver.Firefox()
    driver.get(environment_details)
    yield driver
    print("Tearing down...")
    driver.close()

@pytest.mark.skip
def test_click_add_remove_elements(setup):
    setup.find_element(By.LINK_TEXT,"Add/Remove Elements").click()
    setup.find_element(By.XPATH,"//*[contains(text(),'Add Element')]").click()
    setup.find_element(By.XPATH,"//*[contains(text(),'Delete')]")

@pytest.mark.skip
def test_basic_auth(setup):
    setup.get("https://admin:admin@the-internet.herokuapp.com/basic_auth")
    message = setup.find_element(By.XPATH,"//p").text
    congrats = message.startswith("Congratulations")
    assert congrats

@pytest.mark.skip
def test_broken_images(setup):
    setup.find_element(By.LINK_TEXT,"Broken Images").click()
    color = setup.find_element(By.XPATH,"//img[@src='asdf.jpg']").get_attribute("color")
    if color == None:
        print("Image is blank")

@pytest.mark.skip
def test_challenging_dom(setup):
    setup.find_element(By.LINK_TEXT,"Challenging DOM").click()
    rows = setup.find_elements(By.XPATH,"//table/tbody/tr")
    for row in rows:
        column_eight = row.find_element(By.XPATH,"td[7]")
        column_eight.find_element(By.LINK_TEXT,"edit").click()

@pytest.mark.skip
def test_checkboxes(setup):
    setup.find_element(By.LINK_TEXT,"Checkboxes").click()
    checkboxes = setup.find_elements(By.XPATH,"//*[@id='checkboxes']/child::input")
    for cbox in checkboxes:
        if cbox.get_attribute("checked") == None:
            cbox.click()

@pytest.mark.skip
def test_context_menu(setup):
    setup.find_element(By.LINK_TEXT,"Context Menu").click()
    element = setup.find_element(By.XPATH,"//*[@id='hot-spot']")
    ActionChains(setup).context_click(element).perform()
    setup.switch_to.alert.accept()

@pytest.mark.skip
def test_disappearing_elements(setup):
    setup.find_element(By.LINK_TEXT,"Disappearing Elements").click()
    elements = setup.find_elements(By.XPATH,"//ul/child::li")
    for e in elements:
        print(e.text)

@pytest.mark.skip
def test_drag_and_drop(setup):
    setup.find_element(By.LINK_TEXT,"Drag and Drop").click()
    source = WebDriverWait(setup,20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='column-a']")))
    target = WebDriverWait(setup,20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='column-b']")))
    ActionChains(setup).drag_and_drop(source,target).perform()


# Method to capture src attribute of dynamically appearing images.
def test_dynamic_content(setup):
    setup.find_element(By.LINK_TEXT,"Dynamic Content").click()
    images = setup.find_elements(By.XPATH,"//*[@class='large-10 columns large-centered']/div/div/child::img")
    texts = setup.find_elements(By.XPATH,"//*[@class='large-10 columns large-centered']/div/div/child::img/following::div[@class='large-10 columns']")
    size = len(images)

    # Capturing src attribute of the images
    for img in images:
        print(img.get_attribute("src"))
    # Capturing text displayed next to each image
    for t in texts:
        print(t.text)

# Method to capture attributes of some elements and changing their status
def test_dynamic_controls(setup):
    setup.find_element(By.LINK_TEXT,"Dynamic Controls").click()
    cbox_status = setup.find_element(By.ID,"checkbox").get_attribute("checked")

    # Check whether checkbox is enabled of disabled.
    if cbox_status == None:
        setup.find_element(By.ID,"checkbox").click()
    setup.find_element(By.XPATH,"//button[text()='Remove']").click()

    # Checking whether text box is disabled and if yes click to enable it
    tbox_status = setup.find_element(By.XPATH,"//*[@id='input-example']/child::input").get_attribute("disabled")
    if tbox_status == "true":
        setup.find_element(By.XPATH,"//button[text()='Enable']").click()

    # Wait for the text box to get enabled
    wait = WebDriverWait(setup,20).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='input-example']/child::input")))
    setup.find_element(By.XPATH,"//*[@id='input-example']/child::input").click()
    setup.find_element(By.XPATH, "//*[@id='input-example']/child::input").send_keys("Entering text")

# Method to navigate to a page with hidden element and displaying it
def test_dynamic_loading(setup):
    setup.find_element(By.LINK_TEXT,"Dynamic Loading").click()
    setup.find_element(By.LINK_TEXT,"Example 1: Element on page that is hidden").click()
    hidden_element = setup.find_element(By.XPATH,"//*[@id='finish']")
    display_status = setup.find_element(By.XPATH,"//*[@id='finish']").get_attribute("style")

    # Check elements display status
    display_status == 'display: none;'
    if display_status == 'display: none;':
        # Use javascript to change the attribute display from none to block
        setup.execute_script("arguments[0].setAttribute('style','display: block;')",hidden_element)
    wait = WebDriverWait(setup,20).until(EC.presence_of_element_located((By.XPATH,"//*[@id='finish']")))

@pytest.mark.skip
# Method to display an ad that's hidden in the page.
def test_entry_ad(setup):
    setup.find_element(By.LINK_TEXT,"Entry Ad").click()
    setup.find_element(By.XPATH,"//h3[text()='Entry Ad']").click()
    restart_ad = setup.find_element(By.ID,"restart-ad")
    setup.execute_script("arguments[0].setAttribute('style','display:block;')",restart_ad)

# Method to exit the browser viewport to get a modal dialog appear.
def test_exit_intent(setup):
    setup.find_element(By.LINK_TEXT,"Exit Intent").click()
    window_size = setup.get_window_size()
    # Capturing the window width and height
    width = window_size['width']
    height = window_size['height']

    # Adjusting screen size metrics to move mouse to desired position
    width_click = width-1000
    height_click = height - (height-5)

    # AIT command to move the mouse
    ait.move(1000, 5)
    modal = setup.find_element(By.XPATH,"//*[@id = 'ouibounce-modal']")
    if modal.is_displayed():
        print("Modal dialog is opened")
    else:
        print("Failed")

