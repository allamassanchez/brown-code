from math import log

class TextModel:
    """
    A statistical representation of a body of text, used to perform comparisons
    with other TextModels or text samples.
    """
    def __init__(self, model_name):
        
        
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.specialcharacters = {}
        
        pass

    def __repr__(self):
        """
        Return a string representation of the TextModel.
        """
        s  = 'Text Model Name: ' + self.name + '\n'
        s += '  Number of Unique Words: ' + str(len(self.words)) + '\n'
        s += '  Number of Word Lengths:  ' + str(len(self.word_lengths)) + '\n'
        s += '  Number of Stems:  ' + str(len(self.stems)) + '\n'
        s += '  Number of Sentence Lengths:  ' + str(len(self.sentence_lengths))
        s += '\n'
        s += '  Number of Unique Special Characters:  ' 
        s += str(len(self.specialcharacters))
        return s

    def save_model(self):
        
        '''Takes in a TextModel object and saves its dictionaries into separate
        files'''
        
        dictionaries = [self.words, self.word_lengths, self.stems, self.sentence_lengths, self.specialcharacters]
        dictionary_names = ['words','word_lengths','stems','sentence_lengths','specialcharacters']
        filenames = [self.name + '_' + dictionary + '.txt' for dictionary in dictionary_names]
        for name in range(len(dictionaries)):
            file_write(filenames[name],dictionaries[name])
            

    def read_model(self):
        
        '''Reads a texts file and converts contents into dictionaries for
        a TextModel object'''
        
        dictionary_names = ['words','word_lengths','stems','sentence_lengths','specialcharacters']
        filenames = [self.name + '_' + dictionary + '.txt' for dictionary in dictionary_names]
        for name in range(len(filenames)):
            f = open( filenames[name],'r')
            d_str = f.read()
            f.close()
            if name == 0:
                self.words = dict(eval(d_str))
            elif name == 1:
                self.word_lengths = dict(eval(d_str))
            elif name == 2:
                self.stems = dict(eval(d_str))
            elif name == 3:
                self.sentence_lengths = dict(eval(d_str))
            elif name == 4:
                self.specialcharacters = dict(eval(d_str))
            

    def add_string(self, s):
        """
        Analyzes the string s and adds its pieces to all of the dictionaries in
        this text model.
        """
        for character in "~`!@#$%^&*()_-+={}|[]\':;<>?,./":
            if '"' in s and '"' in self.specialcharacters:
                self.specialcharacters['"'] += s.count('"')
            if character in s and character in self.specialcharacters:
                self.specialcharacters[character] += s.count(character)
            if character in s and character not in self.specialcharacters:
                self.specialcharacters[character] = s.count(character)
            if '"' in s and '"' not in self.specialcharacters:
                self.specialcharacters['"'] = s.count('"')
        s = clean_text(s)
        for word in s:
            if word in self.words:
                self.words[word] += s.count(word)
            elif word not in self.words:
                self.words[word] = s.count(word)
            if len(word) in self.word_lengths:
                self.word_lengths[len(word)] += word_lengths_of_string(s).count(len(word))
            if len(word) not in self.word_lengths:
                self.word_lengths[len(word)] = word_lengths_of_string(s).count(len(word))
            word = stem(word)
            if word in self.stems:
                self.stems[word] += 1
            elif word not in self.stems:
                self.stems[word] = 1
        if len(s) in self.sentence_lengths:
            self.sentence_lengths[len(s)] += 1
        elif len(s) not in self.sentence_lengths:
            self.sentence_lengths[len(s)] = 1
               
    def add_file(self, filename):
        
        '''Opens a file and uses add_string function to add to the object's
        dictionaries'''
        
        f = open(filename,'r',encoding = 'utf8', errors = 'ignore')
        lines_in_file = f.read()
        f.close()
        lines_in_file = lines_in_file.replace('.','\n')
        lines_in_file = lines_in_file.replace('?','\n')
        lines_in_file = lines_in_file.replace('!','\n')
        lines_in_file = lines_in_file.split('\n')
        for line in lines_in_file:
            self.add_string(line)

    def similarity_scores(self, other):
        
        '''Calculates a score for how close each of the dictionaries of different
        texts are'''
        
        other_dic = [other.words, other.word_lengths, other.stems, other.sentence_lengths, other.specialcharacters]
        self_dic = [self.words, self.word_lengths, self.stems, self.sentence_lengths, self.specialcharacters]
        sim_scores = [compare_dictionaries(other_dic[dic],self_dic[dic]) for dic in range(len(other_dic))]
        return sim_scores

    def classify(self, source1, source2):
        
        '''Calculates an overall score for all the dictionaries in both sources'''
        
        source1_scores = self.similarity_scores(source1)
        source2_scores = self.similarity_scores(source2)
        score_weights = [0.5, 0.2, 0.05, 0.2, 0.05]
        #assigns more weight to words used and frequency, word lengths
        #and sentence lengths
        source1_final_score = 0
        for number in range(len(score_weights)):
            source1_final_score += score_weights[number]*source1_scores[number]
        source2_final_score = 0
        for number in range(len(score_weights)):
            source2_final_score += score_weights[number]*source2_scores[number]
        if source1_final_score > source2_final_score:
            return source1
        elif source2_final_score >= source1_final_score:
            return source2

    def compare(self, source1, source2):
        '''takes in three TextModel objects and compares the first object with
        the other two. Returns a similarity report'''
        source1_scores = self.similarity_scores(source1)
        source2_scores = self.similarity_scores(source2)
        print('Similarity scores for', source1.name, 'and', self.name,':', str(source1_scores))
        print('Similarity scores for', source2.name, 'and', self.name,':', str(source2_scores))
        score_weights = [0.5, 0.2, 0.05, 0.2, 0.05]
        source1_final_score = 0
        for number in range(len(score_weights)):
            source1_final_score += score_weights[number]*source1_scores[number]
        source2_final_score = 0
        for number in range(len(score_weights)):
            source2_final_score += score_weights[number]*source2_scores[number]
        print(source1.name, 'and', self.name, 'weighted similarity score:', str(source1_final_score))
        print(source2.name, 'and', self.name, 'weighted similarity score:', str(source2_final_score))
        print(self.name, 'is more likely to come from', (self.classify(source1,source2)).name)
        


##
## Helper Methods:
##
        
def test_add_string():
    model = TextModel('model')
    model.add_string('I love! food?')
    assert model.words == {'i': 1, 'love':1, 'food':1} and\
    model.specialcharacters == {'!':1, '?':1} and\
    model.sentence_lengths == {3:1}\
    and model.stems == {'i':1, 'lov':1, 'food':1}, 'general case failed'

def test_save_model_and_read_model():
    '''tests the save_file function, read_model function, and add_file function'''
    HuffPost = TextModel('Huffington Post')
    HuffPost.add_file('HuffPost_Gun_Reform.txt')
    HuffPost2 = TextModel('Huffington Post')
    HuffPost.save_model()
    HuffPost2.read_model()
    assert HuffPost.words == HuffPost2.words and HuffPost.word_lengths == \
    HuffPost2.word_lengths and HuffPost.stems == HuffPost2.stems\
    and HuffPost.specialcharacters == HuffPost2.specialcharacters, 'methods do not work'
    
    

def test_similarity_scores():
    '''tests similarity_score function'''
    model1 = TextModel('model1')
    model2 = TextModel('model2')
    model1.add_string('I like, to eat, food')
    model2.add_string('Why, hello there!')
    answer = [compare_dictionaries(model2.words,model1.words),\
              compare_dictionaries(model2.word_lengths,model1.word_lengths),\
              compare_dictionaries(model2.stems, model1.stems),\
              compare_dictionaries(model2.sentence_lengths, model1.sentence_lengths),\
              compare_dictionaries(model2.specialcharacters, model1.specialcharacters)]
    assert model1.similarity_scores(model2) == answer, 'general case failed'
    
def test_classify():
    '''tests classify function'''
    model1 = TextModel('model1')
    model2 = TextModel('model2')
    model3 = TextModel('model3')
    model1.add_string('I like, to eat, food')
    model2.add_string('Why, hello there!')
    model3.add_string('I love poptarts!!!')
    assert model3.classify(model1,model2) == model2, 'general case failed'

def clean_text(txt):
    
    '''takes in a string and returns a list of words all lowercase and 
    without punctuation'''
    
    new_txt = ''
    txt = txt.lower()
    txt = txt.replace("'","")
    txt = txt.replace('"',"")
    
    for word in txt:
        word = word.strip("~`!@#$%^&*()_-+={}|[]\:;<>?,./")
        new_txt += word
    new_txt = new_txt.split()
    
    return new_txt

def test_clean_text():
    
    '''tests clean_text function'''
    
    assert clean_text('I lOve! to c--ook and dance?') == ['i', 'love', 'to', 'cook','and','dance'], 'cannot clean text'
    

def stem(word):
    
    '''takes in a string and returns only the roots of the words'''
    
    if 'ing' in word or 'ies'in word and len(word) > 5:
        # finds stem of words ending in 'ing'
        # finds stem of plural words endings in 'ies'
        word = word[:word.rfind('i')]
    if 's' == word[-1] and len(word) > 2: 
        # finds stem of plural words  and possesives ending in just 's'
        word = word[:-1]
    if 'e' == word[-1] or 'y' == word[-1] and len(word) > 3:
        # removes the suffix 'e' or 'y'
        word = word[:-1]
    if 'ship' in word and len(word) > 4:
        # finds stem of words with the suffix 'ship'
        word = word[:word.rfind('s')]
    if 'ion' in word or 'ily' in word:
        word = word[:word.rfind('i')]  
    return word

def test_stem():
    '''test the function stem'''
    assert stem('love') == stem('loving'), 'cannot find stem of ing'
    assert stem('insecurities') == stem('insecurity'), 'cannot find stem of ies plural'
    assert stem('friends') == stem('friendship'), 'cannot find true stem'

def word_lengths_of_string(txt):
    
    '''returns a list of the lengths of very word from inputted list of strings'''
    
    list_of_lengths = [len(word) for word in txt]
    return list_of_lengths

def test_word_lengths_of_string():
    
    '''tests word_lengths_of_string function'''
    
    assert word_lengths_of_string(['i', 'love', 'food']) == [1,4,4], 'cannot find lengths of words'
    assert word_lengths_of_string([]) == [], 'empty string failed'

def file_write(filename, dictionary):
    
    '''function creates a file, converts a dictionary into a string, and writes
    it into the file'''
    
    f = open(filename, 'w')
    f.write(str(dictionary))
    f.close

def compare_dictionaries(d1, d2):
    
    '''Creates a score for two dictionaries of the same category from different
    TextModel objects'''
    
    number_of_words_in_d1 = 0
    score = 0
    if len(d2) == 0 or len(d1) == 0:
        return -100000
    elif len(d1) and len(d2) == 0:
        return 0
    for word in d1:
        number_of_words_in_d1 += d1[word]
    if number_of_words_in_d1 == 0:
            return 0
    for word in d2:
        probability = 0.5
        if word in d1:
            probability = d1[word]
        probability = probability/number_of_words_in_d1
        score += d2[word] * log(probability)
    return score
            
def test_compare_dictionaries():
    d1 = {'hello': 4, 'hi':2}
    d2 = {}
    d3 = {'hello': 2, 'hi':1}
    assert compare_dictionaries(d1, d2) == -100000, 'empty dictionary failed'
    assert compare_dictionaries(d1,d3) == 2*log(4/6) + log(2/6), 'general case failed'

def run_experiments():
    HuffPost = TextModel('Huffington Post')
    FoxNews = TextModel('Fox News')
    CNN = TextModel('CNN')
    Breitbart = TextModel('Breitbart')
    WashingtonPost = TextModel('Washington Post')
    NewYorkTimes = TextModel('New York Times')
    HuffPost.add_file('HuffPost_Beto.txt')
    HuffPost.add_file('HuffPost_New_Zealand.txt')
    HuffPost.add_file('HuffPost_Gun_Reform.txt')
    HuffPost.add_file('HuffPost_AIPAC.txt')
    FoxNews.add_file('FoxNews_Beto.txt')
    FoxNews.add_file('FoxNews_New_Zealand.txt')
    FoxNews.add_file('FoxNews_Gun_Reform.txt')
    FoxNews.add_file('FoxNews_AIPAC.txt')
    CNN.add_file('CNN_Beto.txt')
    CNN.add_file('CNN_New_Zealand.txt')
    CNN.compare(HuffPost, FoxNews)
    Breitbart.add_file('Breitbart_Beto.txt')
    Breitbart.add_file('Breitbart_New_Zealand.txt')
    Breitbart.compare(HuffPost, FoxNews)
    WashingtonPost.add_file('WashingtonPost_Beto.txt')
    WashingtonPost.add_file('WashingtonPost_New_Zealand.txt')
    WashingtonPost.compare(HuffPost, FoxNews)
    NewYorkTimes.add_file('NewYorkTimes_Beto.txt')
    NewYorkTimes.add_file('NewYorkTimes_New_Zealand.txt')
    NewYorkTimes.compare(HuffPost, FoxNews)
    FoxNews.compare(Breitbart, HuffPost)


    

# TODO: Test your code! (before writing any functions)
run_experiments()
test_stem()
test_word_lengths_of_string()
test_compare_dictionaries()
test_similarity_scores()
test_classify()
test_save_model_and_read_model()
test_add_string()