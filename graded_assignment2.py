punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']


def strip_punctuation(string):
    """[summary]

    Args:
        string (string): [line of words]
       
    Returns:
        [string]: [a line w/o punctuation]
    """

    new_string = ""
    for char in string:
        if char in punctuation_chars:
            char = char.replace(char, '')
        new_string += char
    return new_string


def collect_all_words(file_name):
    """[summary]

    Args:
        file_name ([object reference to file]): 
                [initial file with all provided data]

    Returns:
        [list]: [list -> lists (each)-> words]
    """
    list_of_lists = []
    for line in file_name:
        
        line = strip_punctuation(str(line))  # eliminating punctuation in line (string)
        list_of_lists.append(line.split())  # adding to the end the list of words to another the list
    return list_of_lists


def positive_negative_words_counter(big_list):
    """[summary]

    Args:
        big_list ([list]): [list -> lists (each) -> words]

    Returns:
        [tuple]: [the number of negative and positive words]
    """

    file_negative = open("negative_words.txt", "r")  # opening particular file that contain negative words to be counted
    file_positive = open("positive_words.txt", "r")
    negative_words_list = file_negative.readlines()  # split of negative words in one line
    positive_words_list = file_positive.readlines()

    positive_words_list = list(map(lambda x: x.strip(), positive_words_list)) #! remember that
    negative_words_list = list(map(lambda x: x.strip(), negative_words_list)) #! eliminates the '\n' inside all elements in a list 

    counter_negative = 0
    counter_positive = 0
    for first_list in big_list:  # going through a list to access inner lists
        for word in first_list:  # particular list of words that was considered in each line of opened file
            if word in negative_words_list:
                counter_negative += 1
            if word in positive_words_list:
                counter_positive += 1

    file_negative.close()  # standard practice
    file_positive.close()
    return counter_positive, counter_negative


def number_of_retweets(file_name):
    """[summary]

    Args:
        file_name ([object reference to file]): [initial file with all provided data]

    Returns:
        [int]: [total number of retweets]
    """
    file_name.seek(0) # protector, saves when file object does not point to the beginning of a file
    first_index = None
    last_index = None
    retweet_count = 0
    guard = True
    for line in file_name:
        if guard is True: # used only once at the beginning, when second value in csv is a header element
            guard = False
            continue

        first_index = line.index(b",") # find out first occurrence of ','(position)
        last_index = line.index(b",", first_index+1) #find out the second occurrence of ','

        retweet_count += int(line[first_index+1:last_index]) #calculates the total # of retweets
    return retweet_count

def number_of_replies(file_name):
    """[summary]

    Args:
        file_name ([object reference of file]): [initial file with all provided data]

    Returns:
        [int]: [total number of replies]
    """
    file_name.seek(0) # protector, saves when file object does not point to the beginning of a file
    first_index = None
    second_index = None
    reply_count = 0
    guard = True
    for line in file_name:
        if guard is True: # used only once at the beginning, when second value in csv is a header element
            guard = False
            continue

        first_index = line.index(b",") # find out first occurrence of ','(position)
        second_index = line.index(b",", first_index+1) #find out the second occurrence of ','
        

        reply_count += int(line[second_index+1:]) #calculates the total # of replies
    return reply_count


twitter_file = open("project_twitter_data.csv", "rb")  # opens a file that contain data
big_list = collect_all_words(twitter_file)  # creates a list of lists which has a words as the elements inside

positive_words, negative_words = positive_negative_words_counter(big_list)  # assigning # of positive and negative words
retweet_count = number_of_retweets(twitter_file)
reply_count = number_of_replies(twitter_file)
twitter_file.close()

my_csv = open("my_file.csv", "w")
my_csv.write("Number of Retweets,Number of Replies,Positive Score,Negative Score,Net Score\n")
my_csv.write("{},{},{},{},{}".format(retweet_count, reply_count, positive_words, negative_words, 0))