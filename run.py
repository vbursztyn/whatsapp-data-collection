from random import randint

from utils import random_sleep, config, driver

from persistence import HistoryHandler
from invites import InviteHandler
from scrolling import ScrollHandler


ih = InviteHandler()
ih.search_invites()

# Ensures focus on the right section of the screen
driver.execute_script("document.getElementById('pane-side').focus();")

sh = ScrollHandler()

for i in range(randint(config['N_SCROLLS'][0], config['N_SCROLLS'][1])):
    ih.parse_invites()
    sh.scroll_down()
    while not sh.scroll_ended():
        ih.parse_invites()
        sh.scroll_down()
    
    random_sleep(config['SCROLL_LOAD_TIME'][0], config['SCROLL_LOAD_TIME'][1])

ih.commit_invites()

