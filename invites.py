from datetime import datetime
from re import findall

from utils import random_sleep, config, driver

from persistence import HistoryHandler


# ********************************************
# * Handles searching and parsing of invites *
# ********************************************
class InviteHandler():
    
    
    unique_invites = set()
    
    
    # search_invites() -- Looks for search box and, if it exists, searches for [search_kw].
    def search_invites(self):
        search_input = driver.find_elements_by_xpath("//input[@title=\'" + config['SEARCH_INPUT_PLACEHOLDER'] + "\']")

        if search_input:
            search_input[0].send_keys(config['SEARCH_KW'])
        random_sleep(config['SEARCH_LOAD_TIME'][0], config['SEARCH_LOAD_TIME'][1])


    # parse_invites() -- Populates global set [unique_invites] by
    #                    sifting through all DIVs and parsing references to [search_kw]. 
    def parse_invites(self):
        all_divs = driver.find_elements_by_xpath("//div[*]")
        all_invites = list()

        for div in all_divs:
            div_invites = findall(config['SEARCH_KW'] + "(?:[a-zA-Z]|[0-9]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", \
                                      div.text)
            all_invites += div_invites

        self.unique_invites = self.unique_invites.union(set(all_invites))

        print "%s invites collected, accumulating %s unique URLs" \
              %(len(all_invites), len(self.unique_invites))
    
    
    # commit_invites() -- Pushes new invites (and their details) to local CSV file.
    def commit_invites(self):
        previously_mined = set(HistoryHandler().get_attribute('invite_URL'))
        new_data = list()
        
        for new_group in (self.unique_invites - previously_mined):
            group_title = self.get_invite_info(new_group)
            
            if not group_title:
                continue
            
            new_datum = {
                'invite_URL': new_group,
                'group_title': group_title,
                'bypass': 'FALSE',
                'joined_at': '',
                'mined_at': str(datetime.now())
            }
            new_data.append(new_datum)
        
        if new_data:
            self.unique_invites = new_data # TO-DO: DELETE
            HistoryHandler().add_data(new_data)
    
    
    # get_invite_info() -- Gets details of a particular invite.
    def get_invite_info(self, invite):
        driver.get("https://%s" %(invite))
        group_title = driver.find_element_by_class_name('block__title').text.encode('utf-8')
        random_sleep(config['INVITE_INFO_INTERVAL'][0], config['INVITE_INFO_INTERVAL'][1])
        return group_title

