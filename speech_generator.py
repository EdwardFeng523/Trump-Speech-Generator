"""
Trump tweet generator
Version 1.5
4th order markov
"""
from collections import defaultdict
import random
import pickle

def read_untagged_file(filename):
    """
    read the given untagged document
    :param filename: a ducument with bunch of words
    :return: a list of strings representing the given document
    """
    #open the file
    f = open(str(filename), "r")
    f = f.read()
    #split the file into words
    document = f.split()
    return document

# document = read_untagged_file("uh.txt")
# print document

def read_pos_file(filename):
    """
    Parses an input tagged text file.
    Input:
    filename --- the file to parse
    Returns:
    The file represented as a list of tuples, where each tuple
    is of the form (word, POS-tag).
    A list of unique words found in the file.
    A list of unique POS tags found in the file.
    """
    file_representation = []
    unique_words = set()
    unique_tags = set()
    f = open(str(filename), "r")
    for line in f:
        if len(line) < 2 or len(line.split("/")) != 2:
            continue
        word = line.split("/")[0].replace(" ", "").replace("\t", "").strip()
        tag = line.split("/")[1].replace(" ", "").replace("\t", "").strip()
        file_representation.append((word, tag))
        unique_words.add(word)
        unique_tags.add(tag)
    f.close()
    return file_representation, unique_words, unique_tags

def build_markov(document):
    """
    build the forward and backward markov chain using the given document
    :param document: a list of strings representing the given document
    :return: a tuple of dictionaries representing the forward and backward markov chains generated with the document
    """
    #Initialize the dictionaries
    forwardcount = defaultdict(lambda: defaultdict(int))
    backwardcount = defaultdict(lambda: defaultdict(int))
    forwardprob = defaultdict(lambda: defaultdict(int))
    backwardprob = defaultdict(lambda: defaultdict(int))
    #compute counts
    for i in range(len(document)-1):
        a = document[i]
        b = document[i+1]
        forwardcount[a][b] += 1
        backwardcount[b][a] += 1
    #compute forward probabilities
    for previous in forwardcount:
        sum = 0
        for current in forwardcount[previous]:
            sum += forwardcount[previous][current]
        for current in forwardcount[previous]:
            forwardprob[previous][current] = forwardcount[previous][current] / float(sum)
    #compute backward probabilities
    for previous in backwardcount:
        sum = 0
        for current in backwardcount[previous]:
            sum += backwardcount[previous][current]
        for current in backwardcount[previous]:
            backwardprob[previous][current] = backwardcount[previous][current] / float(sum)
    result =  (forwardprob, backwardprob)
    
    return result

def build_third_markov(document):
    """
    build the forward and backward markov chain using the given document
    :param document: a list of strings representing the given document
    :return: a tuple of dictionaries representing the forward and backward second order markov chains generated with the document
    """
    #Initialize the dictionaries
    forwardcount = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    backwardcount = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    forwardprob = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    backwardprob = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    #compute counts
    for i in range(len(document)-2):
        a = document[i]
        b = document[i+1]
        c = document[i+2]
        forwardcount[a][b][c] += 1
        backwardcount[c][b][a] += 1
    #compute forward probabilities
    for early in forwardcount:
        for previous in forwardcount[early]:
            sum = 0
            for current in forwardcount[early][previous]:
                sum += forwardcount[early][previous][current]
            for current in forwardcount[early][previous]:
                forwardprob[early][previous][current] = forwardcount[early][previous][current] / float(sum)
    #compute backward probabilities
    for early in backwardcount:
        for previous in backwardcount[early]:
            sum = 0
            for current in backwardcount[early][previous]:
                sum += backwardcount[early][previous][current]
            for current in backwardcount[early][previous]:
                backwardprob[early][previous][current] = backwardcount[early][previous][current] / float(sum)
    result = (forwardprob, backwardprob)
    return result

def build_forth_markov(document):
    """
    build the forward and backward markov chain using the given document
    :param document: a list of strings representing the given document
    :return: a tuple of dictionaries representing the forward and backward second order markov chains generated with the document
    """
    #Initialize the dictionaries
    forwardcount = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda:defaultdict(int))))
    backwardcount = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda:defaultdict(int))))
    forwardprob = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda:defaultdict(int))))
    backwardprob = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda:defaultdict(int))))
    #compute counts
    for i in range(len(document)-3):
        a = document[i]
        b = document[i+1]
        c = document[i+2]
        d = document[i+3]
        forwardcount[a][b][c][d] += 1
        backwardcount[d][c][b][a] += 1
    #compute forward probabilities
    for very_early in forwardcount:
        for early in forwardcount[very_early]:
            for previous in forwardcount[very_early][early]:
                sum = 0
                for current in forwardcount[very_early][early][previous]:
                    sum += forwardcount[very_early][early][previous][current]
                for current in forwardcount[very_early][early][previous]:
                    forwardprob[very_early][early][previous][current] = forwardcount[very_early][early][previous][current] / float(sum)
    #compute backward probabilities
    for very_early in backwardcount:
        for early in backwardcount[very_early]:
            for previous in backwardcount[very_early][early]:
                sum = 0
                for current in backwardcount[very_early][early][previous]:
                    sum += backwardcount[very_early][early][previous][current]
                for current in backwardcount[very_early][early][previous]:
                    backwardprob[very_early][early][previous][current] = backwardcount[very_early][early][previous][current] / float(sum)
#    with open('filename.pickle', 'wb') as handle:
#        pickle.dump(forwardprob, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
#    with open('filename.pickle', 'rb') as handle:
#        b = pickle.load(handle)
#
#    print (forwardprob == b)
    result = (forwardprob, backwardprob)
    return result

def generate_sentence(word, forwardmarkov, backwardmarkov, sforward, sbackward, forforward, forbackward):
    """
    generate a sentence containing the given word using the given markov chains
    :param word: a string representing the given word, assume it cannot be one of the termination marks: ! . ?
    :param forwardmarkov: a two dimensional dictionary representing the forward markov chain generated by build_markov
    :param backwardmarkov: a two dimensional dictionary representing the backward markov chain
    :param sforward: a three dimensional dictionary representing the second order forward markov chain
    :param sbackward: a three dimensional dictionary representing the second order backward markov chain
    :return: a string representing the generated sentence
    """
    #test if the given word is in the markov chain
    if word not in forwardmarkov and word not in backwardmarkov:
        return "I have never said that word you entered, but I'll make America great again!"
    else:
        #initialize the needed information
        firsthalf = ""
        secondhalf = ""
        nextforward = word
        nextbackward = word
        #generate the two neighboring word using the first order markov
        num = random.random()
        prob = 0
        for next in forwardmarkov[nextforward]:
            prob += forwardmarkov[nextforward][next]
            if prob > num:
                verynextforward = next
                currentbackward = next
                secondhalf = secondhalf + " " + verynextforward
                break
        for last in sbackward[currentbackward][nextbackward]:
            prob += sbackward[currentbackward][nextbackward][last]
            if prob > num:
                # print currentforward, nextforward, next
                verynextbackward = last
                currentforward = last
                firsthalf = verynextbackward + " " + firsthalf
                break
        #developing the sentence
        termination = ["!", ".", '."',"?"]
        while verynextforward not in termination:
            num = random.random()
            prob = 0
            for next in forforward[currentforward][nextforward][verynextforward]:
                prob += forforward[currentforward][nextforward][verynextforward][next]
                if prob > num:
                    currentforward = nextforward
                    nextforward = verynextforward
                    verynextforward = next
                    break
            secondhalf = secondhalf + " " + verynextforward
        while verynextbackward not in termination:
            num = random.random()
            prob = 0
            for last in forbackward[currentbackward][nextbackward][verynextbackward]:
                prob += forbackward[currentbackward][nextbackward][verynextbackward][last]
                if prob > num:
                    currentbackward = nextbackward
                    nextbackward = verynextbackward
                    verynextbackward = last
                    break
            firsthalf = verynextbackward + " " + firsthalf
        firsthalf = firsthalf[2:]
        result = firsthalf + word + secondhalf
        # check the quotation mark issue
        num = 0
        for ele in result[:-2]:
            if ele == '"':
                num += 1
        if num % 2 != 0 and result[-1] != '"':
            result = result + '"'
        return result


document = read_untagged_file("Trump1 copy.txt")
markov = build_markov(document)
forward = markov[0]
backward = markov[1]
smarkov = build_third_markov(document)
sforward = smarkov[0]
sbackward = smarkov[1]
formarkov = build_forth_markov(document)
forforward = formarkov[0]
forbackward = formarkov[1]
# print generate_sentence("population",forward, backward, sforward, sbackward)



def run(word, times):
    """
    run the experiments
    :param word: the input word
    :param times: the number of times you want to run the experiment
    :return: the shortest sentence generated by the machine
    """
    sentence = generate_sentence(word, forward, backward, sforward, sbackward, forforward, forbackward)
    for exp in range(times - 1):
        new = generate_sentence(word, forward, backward, sforward, sbackward, forforward, forbackward)
        if len(new) < len(sentence):
            sentence = new
    print (sentence)

run("hate", 1)
