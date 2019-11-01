import urllib
import requests
import

query = "'trade war'"
# Notice the " and ' around trade war! This ensures phrase matching.
query = urllib.parse.quote_plus(query) # Format into URL encoding
number_result = 10