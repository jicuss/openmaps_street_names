import unittest

from lib.string_functions.string_operations import normalize_spacing,fragment_key_formatting,remove_blacklisted_words,strip_state_postal_codes


class StringOperationTests(unittest.TestCase):

    def test_normalize_spacing(self):
        '''
            pass a string with irregular spacing, newline characters, space at beginning / end of string. verify spacing is correct
        '''
        string = '\n            First   Second\n            Third\n        '
        self.assertEquals(normalize_spacing(string),'First Second Third',msg ='Not Normalizing Spacing Correctly')

    def test_fragment_key_formatting(self):
        '''
            pass a string with irregular spacing, newline characters, space at beginning / end of string. verify spacing is correct and replaced with _
        '''
        string = ' \na  random fragment  \n name '
        self.assertEquals(fragment_key_formatting(string),'a_random_fragment_name')


    def test_remove_blacklisted_words(self):
        blacklisted_words = ["Road", "Street", "Drive", "Avenue", "Lane", "Court", "North", "East", "West", "South", "Circle", "Place", "Way", "Northeast", "Northwest", "Southeast", "Southwest", "Boulevard"]
        string = 'Walnut Street'
        self.assertEquals(remove_blacklisted_words(string,blacklisted_words),'Walnut')
        string = '215th Avenue'
        self.assertEquals(remove_blacklisted_words(string,blacklisted_words),'215th')

    def test_strip_state_postal_codes(self):
        for string in ['Boone, IL:Winnebago, CA','Boone, IL;Winnebago, CA','Boone, IL|Winnebago, CA']:
            self.assertEquals(strip_state_postal_codes(string),['CA','IL'])

if __name__ == '__main__':
    unittest.main()
