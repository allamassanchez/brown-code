##
## Section B) Markov
##
import random

def test_helper_dict(filename):
    
    '''Determines if the length and keys  of dictionary are correct'''
    
    file = open(filename,'r')
    long_string = file.read()
    file.close()
    list_of_words = long_string.split()
    
    length = len(list_of_words) + 1 #accounts for key of sentence-start words
    words_used = []
    for word in list_of_words:
        if '.' in word or '!' in word or '?' in word:
            length -= 1 #sentence-ending words should not have a key
        elif word in words_used:
            length -= 1 #keys are only created for unique words
        else:
            words_used += word
    
    if len(create_dictionary(filename)) == length:
        return True
    
    else:
        return False


def test_create_dictionary():
    
    ''' tests create_dicionary function'''

    assert test_helper_dict('sample.txt') == True, 'not good dict'
    print ('Your dictionary is great!')
    

def create_dictionary(filename):
    
    '''Creates a dictionary with words from provided text'''

    file = open(filename,'r')
    long_string = file.read()
    file.close()
    
    list_of_words = long_string.split()
    
    dictionary = {}
    current_word = '$'
    for next_word in list_of_words:
        if '!' in current_word or '?' in current_word or '.' in current_word:
                current_word = next_word
                dictionary['$'] += [current_word]
        elif current_word not in dictionary:
            dictionary[current_word] = [next_word]
            current_word = next_word
        else:
            dictionary[current_word] += [next_word]
            current_word = next_word
    return dictionary


test_create_dictionary()
#test_helper_dict('sample.txt')
    
    # TODO: complete
def helper_test_generate_text(filename,num_words):
    
    '''Determines if length of text produced is correct'''
    
    dictionary = create_dictionary(filename)
    # Wrote same exact code from generate_text without printing it
    text = ''
    for n in range(0,num_words):
        if n == 0:
            next_word = random.choice(dictionary['$'])
            text += ' ' + next_word
        elif next_word not in dictionary:
            text += ' ' + random.choice(dictionary['$'])
        else:
            next_word = random.choice(dictionary[next_word])
            text += ' ' + next_word
            if next_word not in dictionary:
                next_word = '$'
    text = text.split() # added to count number of words
    if len(text) == num_words:
        return True

def test_generate_text():
    
    '''tests generate_text function'''
    
    assert helper_test_generate_text('sample.txt',50) == True, 'not good text'
    print('Your text makes sense ish :) ')

def generate_text(word_dict, num_words):
    
    '''Creates text based on dictionary from a file'''
    
    text = ''
    for n in range(0,num_words):
        if n == 0:
            next_word = random.choice(word_dict['$'])
            text += next_word
        elif next_word not in word_dict:
            next_word = '$'
        else:
            next_word = random.choice(word_dict[next_word])
            text += ' ' + next_word
    

    print(text)
    return text

test_generate_text()
#helper_test_generate_text('sample.txt',25)

brave_dictionary = create_dictionary('brave.txt')
brown_vision_dictionary = create_dictionary('brown_vision.txt')
romeo_dictionary = create_dictionary('romeo.txt')




#generate_text(brown_vision_dictionary, 50)

            
    
    # TODO: complete
generate_text(brown_vision_dictionary, 10)
generate_text(romeo_dictionary, 100)
generate_text(brave_dictionary,100)

#TODO: Test your code! (before writing any functions)
