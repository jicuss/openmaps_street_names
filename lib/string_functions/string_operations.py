import re


def normalize_spacing(string):
    '''
        This function is used to normalize a string input against inconsistent newline and spacing
        It:
            - substitutes newline characters with a space
            - eliminates spacing at beginning and end of the string
            - replaces multiple consecutive spaces with a single space
    '''
    string = re.sub(r'\s+', ' ', string)
    string = re.sub(r'^\s|\s+$', '', string)

    return string


def fragment_key_formatting(string):
    '''
        This function is used to create a cache friendly fragment name
        It:
            - forces the string to lowercase
            - replaces spaces with underscore characters (_)
            - eliminates spacing at beginning and end of the string
    '''

    string = string.lower()
    string = normalize_spacing(string)
    string = re.sub(r'\s+', '_', string)

    return string


def remove_blacklisted_words(string, blacklist):
    '''
        This function strips all occurrences of any word in the blacklist from the string
    '''
    string = reduce(lambda x, y: x.replace(y, ''), blacklist, string)
    return normalize_spacing(string)


def strip_state_postal_codes(string):
    '''
        This function processes the county metadata and strips the state abbriviation
        Process:
            - replace all variations of deliminators with a ; for consistency
            - split the string on the ;, then split each of the returned strings by \,. Grab the second item in that array
            - return unique list of state postal codes in the original string
    '''
    try:
        deliminators = [';', ':', '|']  # an array of possible deliminators
        string = reduce(lambda x, y: x.replace(y, ';'), deliminators, string)
        states = map(lambda x: x.split(', ')[1], string.split(';'))

    except:
        ''' in the event that the originating string is malformed, return an empty array '''
        states = []

    return list(set(states))


def state_postal_codes():
    return ["AL", "AK", "AS", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "GU", "HI", "ID", "IL", "IN", "IA",
            "KS", "KY", "LA", "ME", "MD", "MH", "MA", "MI", "FM", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM",
            "NY", "NC", "ND", "MP", "OH", "OK", "OR", "PW", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA",
            "VI", "WA", "WV", "WI", "WY"]
