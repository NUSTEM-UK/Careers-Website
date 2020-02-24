"""Cleans NUSTEM website data for subsequent processing.

(this file pinched from postcards data crunching, and not actually used)

Pulls Atom feed for 'School Deliveries' post type from live server, then
formats relevant parts as a Pandas DataFrame and outputs a CSV for onward
analysis.

NB. Set Wordpress to generate large (ie. 300+) feeds before running, for
full data collection. `wp-admin`.
NNB. Reset Wordpress subsequently. Ahem.
"""

import feedparser
import time
from urlextract import URLExtract
from urllib.parse import urlparse
import pandas as pd


extractor = URLExtract()

# Set up destination dataframe
column_names = ["Publication date", "Post URL", "Post Title", "School", "Activity URLs"]
output = pd.DataFrame(columns=column_names)
print(output)

# Get the feed and handle it
d = feedparser.parse('https://nustem.uk/feed/atom/?post_type=careers_resource')
print(d['feed']['link']) # Indexed
print(d.feed.title) # Convenience dot notation
print(len(d.entries))

num_entries = enumerate(d.entries) # We need an index to build the output DataFrame
for i, entry in num_entries:
    edate = time.strftime('%Y-%m-%d', entry.published_parsed)
    print(edate + "; " + entry.updated + "; " + entry.title + "; " + entry.link)
    urls = extractor.find_urls(entry.content[0].value) # Extract URLs in full content body.
    activity = [] # Empty the activity list for this entry
    school = ""   # Empty the school assignment for this entry
    # URL decision tree
    for url in urls:
        parsed = urlparse(url)
        if parsed.path: # If there isn't a path, link goes to site root
            partpath = parsed.path[1:] # Slice off leading slash
            partpath = partpath[:partpath.find("/")]
            if partpath != "wp": # omit anything that has a /wp component, because that'll be to /content/uploads.
                if partpath == "activity":
                    activity.append(parsed.path) # Append full activity path to list 
                else:
                    # Not robust: assumes any remaining URL must be the school name.
                    # we want just the (canonical/clean) part-URL form of the school name
                    school = partpath
    print(i)
    print("School: " + school)
    print("Activity: " + str(activity))
    print("---")
    # Build this output line as a Pandas DataFrame, so it can be appended
    # to the empty output we instantiated earlier.
    thisline=pd.DataFrame({"Publication date": edate, 
                           "Post URL": entry.link,
                           "Post Title": entry.title,
                           "School": school}, index=[0])
    # Append that temp frame to the output frame
    output = output.append(thisline, ignore_index=True)
    # ...then set the relevant cell for the Activity, as a list object.
    output.at[i, "Activity URLs"] = activity

# We've now iterated over all the entries returned from the feed,
# so output the resulting DataFrame to disk.

output.to_csv('data/website_data.csv')
