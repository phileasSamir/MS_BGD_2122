"""
Extract type facts from a Wikipedia file


=== Purpose ===

The goal of this lab is to extract the class to which an entity belongs from Wikipedia.
For example, given the Wikipedia article about Leicester:

    Leicester is a small city in England

the goal is to extract:

    Leicester TAB city


=== Provided Data ===

We provide
1. a preprocessed version of the Simple Wikipedia (wikipedia-first.txt), which looks like above
2. a template for your code, extractor.py
3. a gold standard sample (gold-standard-sample.tsv).


=== Task ===

Complete the extract_type() function so that it extracts the type of the article entity from the content.
For example, for a content of "Leicester is a beautiful English city in the UK", it should return "city".
Exclude terms that are too abstract ("member of...", "way of..."), and try to extract exactly the noun(s).
You can also skip articles (e.g. return None) if you are not sure or if the text does not contain any type.
In order to ensure a fair evaluation, do not use any non-standard Python libraries except nltk (pip install nltk).

Input:
April
April is the fourth month of the year with 30 days.

Output:
April TAB month


=== Development and Testing ===

We provide a certain number of gold samples for validating your model.
Finally, we calculate a F1 score using following equation:

F1 = (1 + beta * beta) * precision * recall / (beta * beta * precision + recall)

with beta = 0.5, putting more weight on precision in that way.

=== Submission ===

1. Take your code, any necessary resources to run the code, and the output of your code on the test dataset (no need to put the other datasets!)
2. ZIP these files in a file called firstName_lastName.zip
3. submit it here before the deadline announced during the lab:

https://www.dropbox.com/request/Wa81LB15Vdwg8Q9aPZSb
=== Contact ===

If you have any additional questions, you can send an email to: chadi.helwe@telecom-paris.fr

"""

# import custom packages
from utils import Parsy, eval_f1


# a simplified wiki page document
wiki_file = 'wikipedia-first.txt'
# some gold samples for validation
gold_file = 'gold-standard-sample.tsv'
# predicted results generated by your model
# you are supposed to submit this file
result_file = 'results.tsv'


import string
import nltk
from nltk import word_tokenize

def extract_type(wiki_page, debug=False):
    '''

    :param wiki_page is an object contains a title and the first sentence from its wiki page.
    :return:
    '''
    title = wiki_page.title
    content = wiki_page.content
    
    # Code goes here

    # GENERAL THINKING:
    # We iterated over our mistakes to find new rules that help us select the right type without degrading overall performance.
    # For edge cases (for instance, the first if statement in our loop), we only added words that made sense in the overall list of pages.
    # For instance, we corrected Senator and novel because in the context of Wikipedia, those are most likely nouns.
    # But, we did not correct "military": this is because military can indeed be an adjective, and is properly classified in most cases.
    # So, we accept to be wrong for "Army", because it means we are right *in general*.
    # in other words: we tried not to overfit.

    # We tokenize and pos-tag the words of the content
    tokens = nltk.pos_tag(word_tokenize(content))

    # Initialize some variables
    found_verb = False
    found_nouns = False
    letype = "None"
    oldtype = "None"

    # We iterate over pos-tags and tokens
    for i, (t, pos) in enumerate(tokens):

        # Some mistakes in the nltk pos-tagger regarding punctuation
        # Overall, if we meet punctuation, we just want to ignore it
        if t in string.punctuation:
            continue

        # Some mistakes in the nltk perceptron pos-tagger
        if t in ["novel","Senator","military"]:
            pos = "NN"
        
        # We select the first noun, just in case
        if not found_verb and letype == "None" and pos in ["NN","NNS"]:
            letype = t
        
        # Usually, the right type is the last noun after the first verb
        # So, if we find a verb, we set "found_verb" to True
        if pos in ["VBP", "VBD", "VBZ"]:
            found_verb = True

        # If we found a verb previously and then find a noun
        if found_verb == True and pos in ["NN","NNS"]:

            # We always select the first noun after the verb, just in case
            if letype == "None":
                letype = t
                found_nouns = True

            # If new noun is not a "class" or vague noun
            if t not in ["name","part","type","first","word","kind"]:
                # We save the last saved type in the oldtype variable
                oldtype = letype
                # Our new type is current token
                letype = t
                # We have now found the noun phrase that interests us
                found_nouns = True
        
        # The POS-tags here represent all possible POS-tags within a noun phrase
        # If our current POS-tag is not in these, it means we've left the first noun phrase
        # So, we should break
        if found_nouns == True and (pos not in ["NN","NNS","IN","JJ","VBD","POS"] or t == "with" or t=="from"):
            # If we find a conjugated verb, our current noun is most likely the subject of that verb
            # So, we go back to the previously selected type
            if pos == "VBP" and letype != "None" and oldtype != "None":
                letype = oldtype
            break

        # Prints to help debug
        if debug:
            print(t,pos,letype)
    
    # Prints to help debug
    if debug:
        print(tokens)
        print(letype)
        
    return letype

def run():
    """
    First, extract types from each sentence in the wiki file
    Next, use gold samples to evaluate your model
    :return:
    """
    with open(result_file, 'w', encoding="utf-8") as output:
        for page in Parsy(wiki_file):
            typ = extract_type(page)
            if typ:
                output.write(page.title + "\t" + typ + "\n")

    # Evaluate on some gold samples for checking your model
    eval_f1(gold_file, result_file)


run()