This is a python script that uses BeautifulSoup and Selenium to scrape one jail, Baker Correctional Institution, in the Florida Department of Corrections. 

The script starts with the homepage of the inmate database, of which the first page is hosted using an HTML address. From these, the url defaults to a generic paging address with a unique session ID. Selenium loads each page, finds the next button and clicks it, taking the urls from each inmate on every page. During the course of the while loop, it continues clicking the next button and getting links until the button no longer exists.

A function getDetails() then opens each of the links, which have been stored in a list, and gets the demographic information for each inmate. This is then stored to a python dictionary. The last function writes this information to a CSV.

Will update this repo later to cycle through more than just one jail and to get additional information, including charges. 

- Updated March 29, 2017

<-- Original Post March 24, 2017 -->

Originally I intended to scrape the biographical information for about 8,000 inmates in region 2 of the Florida Department of Corrections. 

B. To do this, I taught myself selenium to find each inmate's URL linking to their profile showing their demographics. I made a function first finding all of the URLs on the page. To do this, I used an xpath to locate the tag I needed and get the href attribute containing the link. Due to the horrible coding of the Department of Corrections page, I couldn't get the element by class, tag or ID. I then stored all of these links to a list. 

I then opened the pages in the next function and created a python dictionary to get the text for each of the keys by passing them as attributes in the dictionary. In this, I used Beautiful Soup. I then appended each inmate's information to the list of inmates. 

After this, I opened a CSV file and wrote the keys to be the headers and matched that with the key's attributes. 

In this exercise, I was unable to figure out how to click the "Next" button at the bottom of the page and when that existed, to go through and get the links. My attempt at this has been commented out of the file. What you will get if you run my python file is the information for the first 20 inmates in the Baker Correctional institution. 

So, while I did fail this assignment, I learned more in the five days I worked on it than I ever thought possible. I didn't realize when starting this project that I would need selenium do to the DOC's page being an asp database. I didn't realize how difficult it would be for me to loop through the pages. But I taught myself a lot over the last few days. So I don't really see this as failing. I learned something new. For the first time, I found how much I can do when giving it my all and at many points, what I'm turning in now is more than I thought it could be. I'd rather reach high and miss than play it safe. So I will finish this project. Not for a grade, but because I know I can do it and because I am driven to learn this. I learned so much while failing at this assignment and couldn't be more proud of myself.

- 
