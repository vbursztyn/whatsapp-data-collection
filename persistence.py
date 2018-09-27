from csv import DictReader, DictWriter


HISTORY_DATA_FILE = 'mined_invites.csv'


# ************************
# * Handles history data *
# ************************
class HistoryHandler():
    
    
    history_file = HISTORY_DATA_FILE
    
    
    # get_all() -- Gets all data.
    def get_all(self):
        previously_mined = None

        with open(self.history_file, 'r') as history_f:
            previously_mined = [ { k: v for k, v in row.items() } \
                                  for row in DictReader(history_f, skipinitialspace = True) ]
        
        return previously_mined
    
    
    # get_attribute() -- Gets a column of data (e.g., 'invite_URL').
    def get_attribute(self, attr_name):
        previously_mined = None

        with open(self.history_file, 'r') as history_f:
            previously_mined = [ row[attr_name] for row in DictReader(history_f, skipinitialspace = True) ]
        
        return previously_mined
    
    
    # add_data() -- Adds new rows of data (ensurance of uniqueness should be done prior to its call,
    #               probably using get_attribute() first);
    #               [new_data] is a list of dictionaries, consistently to what is returned by get_all().
    def add_data(self, new_data):
        all_data = self.get_all() + new_data       
        keys = all_data[0].keys()
        
        with open(self.history_file, 'w') as output_f:
            committer = DictWriter(output_f, keys)
            committer.writeheader()
            committer.writerows(all_data)

