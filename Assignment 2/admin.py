# Name:  Cyrus Eftos
# Student Number: 10434000

# “admin.py”, a CLI program that allows the user to add, list, search, view and delete details of
# quotes, and stores the data in a text file.

import json  # Import the json module to allow us to read and write data in JSON format.
import random
import textwrap

FILENAME = 'data.txt'


def input_int(prompt):
    """Integer Input.
    This function repeatedly prompts for input until an integer is entered.

     Args:
         prompt: List containing quotes stored as dictionaries.

     """

    while True:
        input_int_value = input(prompt)
        try:
            num_response = int(input_int_value)
        except ValueError:
            print('Invalid input - Try again.')
            continue
        if num_response < 1:
            print("Please enter a number greater than 0")
            continue
        return num_response


def input_something(prompt):
    """String Input.
    This function repeatedly prompts for input until something (not just whitespace) is entered.

     Args:
         prompt:

     """

    while True:
        input_something_value = input(prompt).strip()
        if not input_something_value:
            continue
        return input_something_value


def save_changes(data_list, statement):
    """Save Changes.
    This function opens "data.txt" in write mode and writes dataList to it in JSON format.

    Args:
        data_list: List containing quotes stored as dictionaries.
        statement: String to be printed after the changes have been saved.

    """
    with open(FILENAME, 'w') as loaded_file:
        json.dump(data_list, loaded_file)
    print(statement)


def format_quote(quote):
    """Format Quote.
    Take a string (quote), shorten if it's more than 40 characters using textwrap.shorten(),
    then using format() wrap the string with double quotes.

    Args:
        quote: The quote to reformat.
    Returns:
        Truncated quote (if less than 40 char) surrounded by double quotes.

    """

    return '"{}"'.format(textwrap.shorten(quote, width=40, placeholder="..."))


def format_author(author, year):
    """Format Author.

    This function accepts author, year parameters and returns a string containing the author
    name with or without the year at the end, depending on whether the year contains “u”.

     Args:
         author: The author to include.
         year: The year to include.
     Returns:
         Formatted author and year string

     """
    # author + ('' if year == 'u' else 'year'). author + (return '' if year is 'u' else return 'year')
    return '— ' + str(author) + ('' if year == 'u' else ', ' + str(year))


# Here is where we attempt to open data.txt and read the data into a "data" variable.
# If the file does not exist or does not contain JSON data, set "data" to an empty list instead.

try:
    with open(FILENAME, 'r') as outfile:
        data = json.load(outfile)
except FileNotFoundError:  # catch FileNotFoundError exception
    file = open(FILENAME, 'w')  # Create new file
    data = []  # Declare empty list
except ValueError:  # catch ValueError exception
    data = []  # Declare empty list

# Print welcome message, then enter the endless loop which prompts the user for a choice.
print('Welcome to the QuoteMaster Admin Program.')

while True:
    print('Choose [a]dd, [i]nsert, [l]ist, [r]andom, [s]earch, [v]iew, [d]elete or [q]uit.')

    extra_input = None  # create an empty extra_input variable
    initial_choice = input('> ')  # prompt for input and store in initial_choice variable
    # test initial_choice if it's longer than 1 character. We can then assume that the input has extra information
    # that we can use instead of prompting the user for information again.
    if len(initial_choice) > 1:
        extra_input = initial_choice[1:].strip()  # strip whitespace
    choice = initial_choice[0].lower()  # take

    # if choice in {'l', 'r', 's', 'v', 'd'} and len(list) < 1: also could works but 'and not' seems more python-y
    if choice in {'l', 'r', 's', 'v', 'd'} and not data:
        print('There are no quotes saved')
        continue

    if choice == 'a':

        quote_input = input_something("Enter the quote: ")
        author_input = input_something("Enter the author's name: ")
        year_input = input_something("Enter the year  (enter "u" if unknown): ")

        data.append({'quote': quote_input, 'author': author_input, 'year': year_input})
        save_changes(data, 'Quote by "' + str(author_input) + '" saved!')

        continue

    elif choice == 'i':
        print('Please enter the quote in the correct format: "Quote" - Author, Year')
        quote_string = input_something("Enter quote: ")

        # I found a few ways of accomplishing this. The below example is a one liner that is difficult to read.
        # It uses regex to split the entered string by the '-' & ',' delimiters then iterates over the list
        # and appends the items we want to keep to a new list.
        # splitList = [string for string in re.split(r'(-+|,)', quoteString) if string not in ('"', '-', ',')]
        # this is basically a compressed version of the following...
        # splitList = []
        # for string in list:
        #   if string not in ('delimiters we want to remove'):
        #       new_list.append(string)

        # I've used the following way of manipulating the strings using rfind(), replace() and strip(). Using rfind()
        # method we can use the returned index to split the string using the provided delimiter, the replace() method
        # is then used to remove any unwanted characters and then the strip() method is used to remove any whitespace.

        quote = quote_string[:quote_string.rfind('"')].replace('"', '').strip()
        author = quote_string[quote_string.rfind('-'):quote_string.rfind(',')].replace('-', '').strip()
        year = quote_string[quote_string.rfind(','):].replace(',', '').strip()

        # Probably don't need to cast these to strings but it seems safer to do so.
        data.append({'quote': str(quote), 'author': str(author), 'year': str(year)})
        save_changes(data, 'Quote by "' + str(author) + '" saved!')

        continue

    elif choice == 'l':
        # loops over data list and prints formatted quotes
        for i, entry in enumerate(data):
            # prints formatted quote. Example: 1) "Brevity is the soul of wit." - William Shakespeare, 1602
            print(str(i + 1) + ') ', format_quote(entry['quote']), format_author(entry['author'], entry['year']))

    elif choice == 's':
        if extra_input:
            search_input = extra_input.lower()
        else:
            search_input = input_something("Enter the quote: ")
        search_count = 0  # declare search_count variable
        for key, value in enumerate(data):

            # Use search_input to check if a newly created set contains the entered string. I decided to cast
            # everything to lowercase so it doesn't matter what case the quote is stored as.
            if search_input.lower() in value['quote'].lower() + value['author'].lower():
                search_count += 1  # increment search_count
                # print out the quote, author, year using the formatting functions.
                print(format_quote(data[key]['quote']), format_author(data[key]['author'], data[key]['year']))

        # If no results print "No results found...". If results print the number of quotes found.
        print('No results found...' if search_count is 0 else 'Found: ' + str(search_count) + ' quote(s)')

        continue

    elif choice == 'r':
        random_quote = random.choice(data)
        print('"{}"'.format(random_quote['quote']), '\n', format_author(random_quote['author'], random_quote['year']))

        continue

    elif choice == 'v':
        if extra_input:
            try:
                user_choice = int(extra_input)
            except ValueError:
                print('Invalid input - Try again.')
                user_choice = input_int("Quote number to view: ")
        else:
            user_choice = input_int("Quote number to view: ")
        try:
            loaded_quote = data[int(user_choice - 1)]
            print('"{}"'.format(loaded_quote['quote']), '\n',
                  format_author(loaded_quote['author'], loaded_quote['year']))
        except IndexError:
            print('Sorry, There is only', len(data), 'quotes stored. Use [l]ist or [s]earch to find a quote to view')

        continue

    elif choice == 'd':
        if extra_input:
            try:
                user_choice = int(extra_input)
            except ValueError:
                print('Invalid input - Try again.')
                user_choice = input_int("Quote number to delete: ")
        else:
            user_choice = input_int("Quote number to delete: ")
        try:
            deleted_quote = data.pop(int(user_choice - 1))  # Delete the quote.
            save_changes(data, 'Quote by "' + str(deleted_quote['author']) + '" removed!')  # save changes

        except IndexError:
            print('Sorry, There is only', len(data), 'quotes stored. Use [l]ist or [s]earch to find a quote to remove')

        continue

    elif choice == 'q':
        break

    else:
        print("Please enter a valid option!\n")

print("Goodbye!")
