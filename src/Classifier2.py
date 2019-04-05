import os
import re
import Parser as p
import math

directory_in_str = "../files/test/"


def remove_stop_words():
    f = open("../files/stop words.txt", 'r')
    data = f.read()
    data = data.split('\n')
    for word in data:
        if word in p.vocab:
            # print(word)
            stop_word = p.vocab.pop(word)
            # print(stop_word)
            p.spam_word_count -= stop_word['spam']
            p.ham_word_count -= stop_word['ham']
            # print('------')


def parse_test_files():
    directory = os.fsencode(directory_in_str)

    ret = []

    for file in os.listdir(directory):
        testing_set = {}
        filename = os.fsdecode(file)

        if filename.endswith(".txt"):
            # print(filename)
            txt_file = directory_in_str + filename
            f = open(txt_file, 'r')
            try:
                # print(f.read())
                data = f.read().lower()
                data = re.split('[^a-zA-Z]', data)
            except UnicodeDecodeError:
                f = open(txt_file, 'r', encoding='cp850')
                data = f.read().lower()
                data = re.split('[^a-zA-Z]', data)

            for word in data:
                if word not in testing_set:
                    testing_set[word] = 1
                else:
                    testing_set[word] = testing_set[word] + 1

            # score_ham = math.log10(p.ham_word_count / p.ham_count)  # Should be number of spam emails
            # score_spam = math.log10(p.spam_word_count / p.spam_count)

            score_ham = math.log10(p.ham_count / p.ham_count + p.spam_count)  # Should be number of spam emails
            score_spam = math.log10(p.spam_count / p.ham_count + p.spam_count)

            for word, word_count in testing_set.items():
                # Skip the words that we have not seen in training set
                if word not in p.vocab:
                    # print('word not in data')
                    # print(word)
                    continue
                score_spam += math.log10(word_count / p.spam_word_count)  # Should be number of spam words
                score_ham += math.log10(word_count / p.ham_word_count)

            if 'ham' in filename:
                classification = 'ham'
            else:
                classification = 'spam'
            ret.append({'filename': filename, 'spam_score': score_spam, 'ham_score': score_ham,
                        'classification': classification})
        else:
            continue

    return ret


def write_baseline_file():
    f = open("baseline-result2.txt", 'w+')
    line = 1

    results = parse_test_files()

    for result in results:
        spam_score = str(result['spam_score'])
        ham_score = str(result['ham_score'])
        correct_classification = result['classification']

        if result['spam_score'] > result['ham_score']:
            classification = 'spam'
        else:
            classification = 'ham'

        if classification == correct_classification:
            classification_result = 'right'
        else:
            classification_result = 'wrong'

        f.write(str(line) + ' ' + result['filename'] + ' ' + classification + ' ' + ham_score + ' ' + spam_score + ' '
                + correct_classification + ' ' + classification_result + '\n')
        line += 1


remove_stop_words()

write_baseline_file()

print('Done classifier2')
