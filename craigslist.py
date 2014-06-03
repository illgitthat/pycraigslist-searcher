from bs4 import BeautifulSoup
import urllib2
import re
import fnmatch
import time

cities = ["washingtondc", "miami", "sfbay", "newyork", "losangeles", "sandiego"] #Craigslist subdomains
keywords = ["web*", "wordpress", "site"] # What you want to search for...
category = "cpg" # Craigslist category key

header = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8">	
            <title>New Craigslist listings</title>
            <link href="http://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.1/css/bootstrap.min.css" rel="stylesheet">
            <link href='http://fonts.googleapis.com/css?family=Milonga' rel='stylesheet' type='text/css'>
        </head>
        <body>
        """
html = ""

for city in cities:
    link = "http://" + city + ".craigslist.org"
    url = urllib2.urlopen(link + "/" + category) # Fetches category page
    content = url.read()
    soup = BeautifulSoup(content)

    for a in soup.findAll('a',href=True): # This checks each link on the page
        if re.findall('/cpg/*', a['href']):
            for word in keywords: # This checks each keyword in the link
                matches = fnmatch.filter(str(a.contents).split(), word)
                if matches:
                    listing = link + str(a['href'])
                    print listing
                    
                    url = urllib2.urlopen(listing) # individual listing
                    content = url.read()
                    soup = BeautifulSoup(content)
                    
                    title = soup.title.string
                    for match in matches:
                        title = title.replace(str(match), '<b>' + str(match) + '</b>')
                    body = ""
                    body = str(soup.find(id="postingbody"))
                    
                    try:
                        # Finds email address to reply to
                        reply = soup.find("a", {"id": "replylink"})['href']
                        url = urllib2.urlopen(link + reply) 
                        content = url.read()
                        soup = BeautifulSoup(content)
                        
                        email = str(soup.find(class_='gmail')).replace(">gmail", ">Reply by email").replace(";su=", ";su=RE: ")
                        email = email.replace("&amp;body=%0A%0A", " - I can help&amp;body=")
                        email = email.replace('%0A"', '%0A%0AHello,%0A%0A%0A%0A--%0AAdam Bloom%0A571.969.ADAM (2326)%0Aadamc.bloom@gmail.com"')
                    except:
                        email = "Contact info in post"
                    
                    title = '<h2><a href="' + listing + '">' + title + '</a> [' + city + ']</h2>'
                    email = '<h5>' + email + '</h5>'
                    html = html + title + unicode(body, "utf-8") + email + '<hr>'
                    
    print "finished " + city
f = open('C:\Users\Adam\Desktop\craigslist.html', 'w')
html = header + html
f.write(html.encode('utf8'))
print "looks like we finished!"