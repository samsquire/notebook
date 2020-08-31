from itertools import combinations
import multiprocessing
from multiprocessing import Process, Queue, Event, JoinableQueue
from scipy.stats import pearsonr, spearmanr
import sys
import workers
                
if __name__ == '__main__':
    quit = Event()
    work_queue = JoinableQueue()
    processes = []
    print(multiprocessing.cpu_count())
    for i in range(0, multiprocessing.cpu_count()):
        print("Creating worker...")
        process = Process(target=workers.work, args=(work_queue, quit))
        process.daemon = True
        processes.append(process)
        process.start()



    sentences, words = workers.get_words_sentences("data2.txt")
    import sys
    sys.stdout.flush()
    for word1, word2 in combinations(words, 2):
        work_queue.put((word1, word2))
    work_queue.join()
    quit.set()
    print("Finished correlating text")