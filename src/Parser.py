import os
import re

directory_in_str = "../files/train/"

ham_word_count = 0
spam_word_count = 0
ham_count = 0
spam_count = 0
vocab = {}
delta = 0.5


def parse():
    directory = os.fsencode(directory_in_str)
    global ham_count
    global spam_count

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            # print(filename)
            txt_file = directory_in_str + filename
            f = open(txt_file, 'r')
            # print(f.read())
            data = f.read().lower()
            data = re.split('[^a-zA-Z]', data)

            if 'ham' in filename:
                __update_training_set(data, 'ham')
                ham_count += 1

            elif 'spam' in filename:
                __update_training_set(data, 'spam')
                spam_count += 1

            # print(os.path.join(directory, filename))
            # continue
        else:
            continue


def __update_training_set(data, filetype):
    global spam_word_count
    global ham_word_count

    for word in data:
        if "spam" == filetype:
            spam_word_count += 1
        elif "ham" == filetype:
            ham_word_count += 1

        if word not in vocab:
            if "spam" == filetype:
                vocab.update({word: {'spam': 1, 'ham': 0}})
            elif "ham" == filetype:
                vocab.update({word: {'spam': 0, 'ham': 1}})
        else:
            vocab[word][filetype] = vocab[word][filetype] + 1


def __smooth_probabilities():
    global ham_word_count
    global spam_word_count

    for key, value in vocab.items():
        value['ham'] = value['ham'] + delta
        value['spam'] = value['spam'] + delta

        spam_word_count += delta
        ham_word_count += delta


def write_file():
    f = open("model.txt", 'w+')
    line = 1
    global spam_word_count
    global ham_word_count

    __smooth_probabilities()

    for key, value in sorted(vocab.items()):
        # print(key)
        # value = vocab[key]
        ham_conditional = value['ham'] / ham_word_count
        spam_conditional = value['spam'] / spam_word_count

        # ham_conditional = "%.7f" % round(ham_conditional, 2)
        # spam_conditional = "%.7f" % round(spam_conditional, 2)

        f.write(str(line) + '  ' + key + '  ' + str(value['ham']) + '  ' + str(ham_conditional) + '  ' + str(
            value['spam']) + '  ' + str(spam_conditional))
        f.write('\n')
        line += 1

    f.write('\n')


parse()
write_file()
print('done')

# f = open("../files/train/train-ham-00009.txt", 'r')
# data = f.read().lower()
# data = re.split('[^a-zA-Z]', data)
#
# for word in data:
#     print(word)
