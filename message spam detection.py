import re
import math
data = [
    ("Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&C's apply 08452810075over18's", "spam"),
    ("Nah I don't think he goes to usf, he lives around here though", "ham"),
    ("Win a brand new car just by participating in our survey!", "spam"),
    ("Hello, how have you been?", "ham"),
    ("Free tickets to the concert available now!", "spam"),
    ("Are we still meeting up for lunch tomorrow?", "ham")
]


def preprocess(text):
    text = text.lower() 
    text = re.sub(r'[^a-z\s]', '', text)
    words = text.split()
    return words

def count_words(data):
    spam_words = {}
    ham_words = {}
    spam_count = 0
    ham_count = 0
    
    for text, label in data:
        words = preprocess(text)
        if label == "spam":
            spam_count += 1
            for word in words:
                if word in spam_words:
                    spam_words[word] += 1
                else:
                    spam_words[word] = 1
        else:
            ham_count += 1
            for word in words:
                if word in ham_words:
                    ham_words[word] += 1
                else:
                    ham_words[word] = 1
    
    return spam_words, ham_words, spam_count, ham_count

def calculate_probability(word, word_count, total_words, vocab_size):
    return (word_count.get(word, 0) + 1) / (total_words + vocab_size)


def classify(text, spam_words, ham_words, spam_count, ham_count):
    words = preprocess(text)
    total_count = spam_count + ham_count
    spam_prob = math.log(spam_count / total_count)
    ham_prob = math.log(ham_count / total_count)
    
    vocab_size = len(set(list(spam_words.keys()) + list(ham_words.keys())))
    spam_total_words = sum(spam_words.values())
    ham_total_words = sum(ham_words.values())
    
    for word in words:
        spam_prob += math.log(calculate_probability(word, spam_words, spam_total_words, vocab_size))
        ham_prob += math.log(calculate_probability(word, ham_words, ham_total_words, vocab_size))
    
    return "spam" if spam_prob > ham_prob else "ham"


spam_words, ham_words, spam_count, ham_count = count_words(data)


test_message = "Congratulations! You've won a free ticket to Bahamas!"
classification = classify(test_message, spam_words, ham_words, spam_count, ham_count)

print(f"The message '{test_message}' is classified as {classification}.")
