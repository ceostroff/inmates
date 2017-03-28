A. Originally I intended to scrape the biographical information for about 8,000 inmates in region 2 of the Florida Department of Corrections. 

B. To do this, I taught myself selenium to find each inmate's URL linking to their profile showing their demographics. I made a function first finding all of the URLs on the page. To do this, I used an xpath to locate the tag I needed and get the href attribute containing the link. Due to the horrible coding of the Department of Corrections page, I couldn't get the element by class, tag or ID. I then stored all of these links to a list. 

I then opened the pages in the next function and created a python dictionary to get the text for each of the keys by passing them as attributes in the dictionary. In this, I used Beautiful Soup. I then appended each inmate's information to the list of inmates. 

After this, I opened a CSV file and wrote the keys to be the headers and matched that with the key's attributes. 

In this exercise, I was unable to figure out how to click the "Next" button at the bottom of the page and when that existed, to go through and get the links. My attempt at this has been commented out of the file. What you will get if you run my python file is the information for the first 20 inmates in the Baker Correctional institution. 
