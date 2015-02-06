This is the README file for A0105860L's submission

== General Notes about this assignment ==

Both left and right padding is applied when generating ngrams.

During initialization of dictionaries for each language, `defaultdict`  with argument 1 is used so that the entry will have a counter value 1 as the initial value. In a sense, it automatically takes care of one-smoothing. When generating ngrams, I keep them all in a set. Then I used `setdefault` to add other ngrams not found in respective language model so that those who are already present won't change, but those who are not present will have a counter value 1.

During calculation of probability, I use summation of logarithms (as suggested in the forum) instead of multiplying the values since the values are very tiny.

After buliding the language models and population of respective ngrams, the `model` variable would look like.
```
  model = {
    'malaysian' : {(None, None, None, 'a'), ...}
    'indonesian' : {(None, None, None, 'M'), ...}
    'tamil' : {(None, None, None, 'k'), ...}
  }
```
And for each input text, I generate ngrams in the similar manner, calculate probability for all three languages and take the maximum and identify the respective language. Moreover, I also keep track of rouge ngrams (those that are not present in the language dictionary. After checking with the input.correct.txt, for the entires that should have been identified as `others`, I notice that there is a significant increase in the number of rouge tokens for those entries. Therefore, I decided to use a ratio threshold and if the ration of rouge ngrams to total number of ngrams is greater than 0.5, identify as `others` language.

                                                                                                                                                                                                                                    To run it with different ngram sizes and/or token-based/character based, change the two global variables (NGRAM_SIZE, WORD_BASED) at the top accordingly. By default, it is 4 gram character based. 

== Files included with this submission ==

build_test_LM.py  -   containing code for language prediction, building ngrams and languge model
eval.py           -   unchanged
ESSAY.txt         -   Answers for essay questions
README.txt        -   This file
Makefile          -   To automate tasks.


== Statement of individual work ==

Please initial one of the following statements.

[I] I, A0105860L, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

== References ==

IVLE Forum post suggesting to use logarithm summations 
https://ivle.nus.edu.sg/forum/forum.aspx?forumid=40c7eba9-a22f-4c9b-b8a9-d535f381b529

Python documentation and some stackoverflow questions particularly on (`itertools.groupby`, generators .etc)
http://stackoverflow.com/questions/2472001/how-can-i-use-python-itertools-groupby-to-group-a-list-of-strings-by-their-fir

http://stackoverflow.com/questions/102535/what-can-you-use-python-generator-functions-for
http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python
