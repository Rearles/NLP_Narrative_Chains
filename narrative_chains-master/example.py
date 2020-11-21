import json
import random
import chains
from pprint import pprint


def parse_test_instance(story):
    """Returns TWO ParsedStory instances representing option 1 and 2"""
    # this is very compressed
    id = story.InputStoryid
    story = list(story)
    sentences = [chains.nlp(sentence) for sentence in story[2:6]]
    alternatives = [story[6], story[7]]
    return [chains.ParsedStory(id, id, chains.nlp(" ".join(story[2:6]+[a])), *(sentences+[chains.nlp(a)])) for a in alternatives]

def story_answer(story):
    """Tells you the correct answer. Return (storyid, index). 1 for the first ending, 2 for the second ending"""
    #obviously you can't use this information until you've chosen your answer!
    return story.InputStoryid, story.AnswerRightEnding



# Load training data and build the model
#data, table = chains.process_corpus("train.csv", 100)
#print(table.pmi("move", "nsubj", "move", "nsubj"))

# load the pre-built model
with open("all.json") as fp:
    table = chains.ProbabilityTable(json.load(fp))
    
def compute_pmi(story):
    total = 0 #this will be what is returned at the end
    id, deps = chains.extract_dependency_pairs(story) #unpacks the tuple into a dictionary of story id, which is a number and deps which is a dictionary of a list of tuples
    for dependency_pairs1 in deps.values():
        total += entity_pmi(dependency_pairs1)
    return total
    
def entity_pmi(dep_pair):
    """ Calculate the average pmi of each verb dependecy pair passed """
    total = 0
    # keep track of how many dependency pairs we've seen
    num = 0
    for i in range(0, len(dep_pair) - 1):
        for j in range(i, len(dep_pair)):
            dep_i = dep_pair[i]
            dep_j = dep_pair[j]
            total += table.pmi(dep_i[0],dep_i[1],dep_j[0],dep_j[1])
            num += 1
    num += 0.001
    return total / num

# load testing data
test = chains.load_data("val.csv")
percentright = 0
for t in test:
    one, two = parse_test_instance(t) #get two choice sentences
    pmi1 = compute_pmi(one)
    pmi2 = compute_pmi(two)
    # logic to choose between one and two
    answer = story_answer(t)
    if pmi1 > pmi2: #means that our choice is 1
        if answer[1] == 1:
            pprint("Choice:"+ str(1))
            pprint("Correct!")
            percentright = percentright + 1
            pprint(percentright)
            pprint("Percentage correct:" + str(percentright/1572))
    
        elif answer[1] != 1:
            pprint("Choice:"+ str(1))
            pprint("Wrong!")
    elif pmi2 > pmi1:
        if answer[1] == 2:
            pprint("Choice:"+ str(2))
            pprint("Correct!")
            percentright = percentright + 1
            pprint(percentright)
            pprint("Percentage correct:" + str(percentright/1572))
        elif answer[1] != 2:
            pprint("Choice:"+ str(1))
            pprint("Wrong!")
    elif pmi1 == pmi2:
        c = random.choice([1, 2])
        if answer[1] == c:
            pprint("Choice:"+ str(1))
            pprint("Correct!")
            percentright = percentright + 1
            pprint(percentright)
            pprint("Percentage correct:" + str(percentright/1572))
        elif answer[1] != c:
            pprint("Choice:"+ str(1))
            pprint("Wrong!")
            
    pprint("answer:"+ str(story_answer(t)))
