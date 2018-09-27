from utils import random_sleep, config, driver

from selenium.webdriver.common.action_chains import ActionChains


# *********************
# * Handles scrolling *
# *********************
class ScrollHandler():
    
    
    previous_last_div = None
    
    
    def __init__(self):
        self.previous_last_div = self.get_last_div()
    

    # parse_order_attribute() -- Please refer to get_last_div().
    def parse_order_attribute(self, div):
        return float(div.get_attribute('style').split('translateY')[1].split(');')[0][1:-2])


    # get_last_div() -- Gets DIV at the bottom of the screen as defined by parse_order_attribute().
    def get_last_div(self):
        ordered_divs = dict()

        for div in driver.find_elements_by_xpath("//div[contains(@style, 'transform: translateY')]"):
            order = self.parse_order_attribute(div)
            ordered_divs[order] = div
        return ordered_divs[max(ordered_divs)]


    # scroll_down() -- Scrolls among messages that are already loaded.
    def scroll_down(self):
        last_div = self.get_last_div()
        scroll_down = ActionChains(driver)
        scroll_down.move_to_element(last_div).perform()
        random_sleep(config['SCROLL_INTERVAL'][0], config['SCROLL_INTERVAL'][1])
    
    
    # scroll_ended() -- Checks if it has reached the last message in the screen
    #                   and gives it some time to load the next batch.
    def scroll_ended(self):
        last_div = self.get_last_div()
        scroll_ended = (self.previous_last_div == last_div)
        self.previous_last_div = last_div

        return scroll_ended

