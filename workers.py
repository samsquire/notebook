def allequal(data):
    equality = data[0]
    for item in data:
        if item != equality:
            return False
    return True

def get_words_sentences(filename):
    sentence = open(filename).read()
    sentence = sentence.lower()
    sentence = sentence.replace("\n", ".")
    print("New lines replaced with sentences")
    sentences = sentence.split(".")
    print("Got {} sentences".format(len(sentences)))
    remove_sentences = sentence.replace(".", "")
    all_words = remove_sentences.split(" ")
    words = list(set(filter(lambda x: len(x) > 0, all_words)))
    return sentences, words
    
def work(q, quit):
    sentences, words = get_words_sentences("data2.txt")
    print("Worker started")
    
    sys.stdout.flush()
    while not quit.is_set():
        word1, word2 = q.get()
        word1data = []
        word2data = []
        word1verdict = 0
        word2verdict = 0
        run_correlation = True
        for current_sentence in sentences:
            this_words = current_sentence.split(" ")
            word1verdict = 0
            word2verdict = 0
            for word in this_words:
                if word == word1:
                    word1verdict = 1
                elif word == word2:
                    word2verdict = 1
            if word1verdict == 1:
                word1data.append(1)
            else:
                word1data.append(0)
            if word2verdict == 1:
                word2data.append(1)
            else:
                word2data.append(0)
        if allequal(word1data):
            # print("{} always appears with {}".format(word1, word2))
            run_correlation = False
        if allequal(word2data):
            # print("{} always appears with {}".format(word2, word1))
            run_correlation = False
        if run_correlation == True:
            correlation, _ = spearmanr(word1data, word2data)
            if correlation > 0:
                print("is {} correlated with {} = {}".format(word1, word2, correlation))
