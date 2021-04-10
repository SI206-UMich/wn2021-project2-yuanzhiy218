# Ted Yuan
# Working with Banghan Guo, Xingyu Pan
# Unique name: yuanzhiy

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import string



def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """

    with open(filename, "r") as fp:
        soup = BeautifulSoup(fp.read(), 'html.parser')
    rows = soup.find_all('tr')
    return_list = list()
    for row in rows:
        td_result = row.find_all('td')
        finder = td_result[1]
        title = finder.find('a', class_='bookTitle').text
        title = title.strip()
        
        author = finder.find('a',class_='authorName').text
        author = author.strip()
        return_list.append((title, author))
    return return_list
        
    #Booktitles = []
    #Authors = []
    #tags = soup.find_all('img')
    #for tag in tags:
     #   t = tag.parent.get('title', None)
    #    a = tag.parent.get('author',None)
     #   if t and a != None:
    #        Booktitles.append(t.strip('/n'))
     #       Authors.append(t.strip('/n'))
    #return (Booktitles,Authors)
    

def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    requested = requests.get(url)
    soup = BeautifulSoup(requested.text, 'html.parser')
    rows = soup.find_all("a", class_ = "bookTitle")
    return_list = list()
    for row in rows[:10]:
        return_list.append("https://www.goodreads.com" + row.get("href"))
    return return_list
    


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    return_list = list()
    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    #parent = soup.find('div', id = "metacol")
    #book_title = parent.find(id = "book_title").text.strip('\n').strip()
   # author = parent.find('a', class_ = "authorName").text
   # pages = parent.find('span', itemprop ='pagenumber').text.strip('\n').strip()
   # return (bookTitle, author, pages)
    title = soup.find("h1", id = "bookTitle")
    title = title.get_text()
    title = title.strip()
    authorAnchor = soup.find("a", class_ = "authorName")
    author = authorAnchor.find("span")
    author = author.get_text()
    author = author.strip()
    page_num_anchor = soup.find("div", id= "details")
    page_num_anchor_row = page_num_anchor.find("div", class_ = "row")
    page_num = page_num_anchor_row.find_all("span")[-1]
    page_num = page_num.get_text()
    page_num = page_num.strip(' pages')
    return_list = [str(title), str(author), int(page_num)]
    return tuple(return_list)


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    with open(filepath) as fh:
        soup = BeautifulSoup(fh, 'html.parser')
    books = soup.find_all(class_='category clearFix')
    lists = list()
    for book in books:
        url = book.find('a')
        url2 = url.get('href')
        cat = book.find('a')
        category = cat.find('h4')
        category = category.text
        category = category.strip()
        title_div = book.find('div', class_='category__winnerImageContainer')
        title = title_div.find('img').get('alt')


        #info = book.find('a')
       # link = info.get('href')
       # category = info.h4.text.strip('\n').strip()
        #name = info.img.get('alt', '')


        lists.append(tuple((str(category),str(title),str(url2))))
    return lists



def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w+') as file_opened:
        writer = csv.writer(file_opened, delimiter=',')
        write_list = ['Book title', 'Author Name']
        writer.writerow(write_list)
        for line in data:
            writer.writerow(line)
    #dir = os.path.dirname(__file__)
    #outFile = open(os.path.join(dir, filename+'.csv'),'w',newline='')
    #csv_writer = csv.writer(outFile, delimiter = ',', quotechar = '"', quoting=csv.QUOTE_ALL)
    #csv_writer.writerow(['Book title','Author Name'])
    #for tup in data:
     #   csv_writer.writerow(tup)
    #outFile.close()


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    with open(filepath) as fh:
        soup = BeautifulSoup(fh, 'html.parser')
    div = soup.find(class_='readable stacked')
    contents = div.contents[3].text
    value = re.findall(r'[A-Z]\w{3}\w*(?:\s[A-Z]\w*)+', contents)
    return value


class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        key = get_titles_from_search_results("search_results.htm")
        # check that the number of titles extracted is correct (20 titles)
        length = len(key)
        correct_num = 20
        self.assertEqual(length, correct_num)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(key), list) # not sure can compare directly
        # check that each item in the list is a tuple
        for i in key:
            self.assertEqual(type(i), tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(key[0], ("Harry Potter and the Deathly Hallows (Harry Potter, #7)", "J.K. Rowling"))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(key[-1], ("Harry Potter: The Prequel (Harry Potter, #0.5)", "J.K. Rowling"))

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)

        # check that each URL in the TestCases.search_urls is a string
        for i in TestCases.search_urls:
            self.assertEqual(type(i), str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for j in TestCases.search_urls:
            result = ("https://www.goodreads.com/book/show/" in j)
            self.assertTrue(result)


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        summaries = []
        for url in TestCases.search_urls:
            summaries.append(get_book_summary(url))
        # check that the number of book summaries is correct (10)
        self.assertTrue(len(summaries)==10)
            
        for item in summaries:
            # check that each item in the list is a tuple
            self.assertIsInstance(item, tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(item), 3)
            # check that the first two elements in the tuple are string
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertIsInstance(item[2], int)
            # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        summary = summarize_best_books('best_books_2020.htm')
        # check that we have the right number of best books (20)
        self.assertTrue(len(summary) == 20)
            # assert each item in the list of best books is a tuple
        for item in summary:
            self.assertIsInstance(item, tuple)
            # check that each tuple has a length of 3
            self.assertTrue(len(item)==3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(summary[0],('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(summary[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        titles = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        write_csv(titles,'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv') as fh:
            csv_lines = list(csv.reader(fh, delimiter=','))
        #for line in titles:
         #   csv_lines.append(get_titles_from_search_results(line))

        #check that there are 21 lines in the csv
        self.assertTrue(len(csv_lines)==21)
        #check that the header row is correct
        self.assertEqual(csv_lines[0], ['Book title', 'Author Name'])
        #check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])
        

if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



