import os
import re
import Parser as p
import math

directory_in_str = "../files/test/"


def parse_test_files():
    directory = os.fsencode(directory_in_str)

    info_of_files = []

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
                if word in p.vocab:
                    score_ham += math.log10(word_count / p.ham_word_count)
                    score_spam += math.log10(word_count / p.spam_word_count)  # Should be number of spam words

            if 'ham' in filename:
                classification = 'ham'
            else:
                classification = 'spam'
            info_of_files.append({'filename': filename, 'spam_score': score_spam, 'ham_score': score_ham,
                                  'classification': classification})
        else:
            continue

    return info_of_files


def write_baseline_file():
    f = open("baseline-result.txt", 'w+')
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


# parse_test_files()
write_baseline_file()

print(p.ham_word_count)
print(p.spam_word_count)
print('Done classifier1')
