# https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk

# Libraries
import random
import re
import string

import emoji
from emosent import get_emoji_sentiment_rank
from googletrans import Translator
from nltk import classify, NaiveBayesClassifier
from nltk.corpus import twitter_samples, stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from textblob import TextBlob


# Functions
# Analysis Emoji and Remove it from text
def remove_emoji(source_entry):
    for removable_emoji in source_entry:
        if removable_emoji in emoji.UNICODE_EMOJI:
            source_entry = source_entry.replace(removable_emoji, '')
    return source_entry


def extract_emoji(data_entry):
    return ''.join(emojis for emojis in data_entry if emojis in emoji.UNICODE_EMOJI)


def analysis_emoji(tweet_entry):
    try:
        weight = 0
        total_score = 0
        analytic_emoji = extract_emoji(tweet_entry)
        analytic_emoji.split()
        for c in analytic_emoji:
            score = get_emoji_sentiment_rank(analytic_emoji[weight])
            total_score += score['sentiment_score']
            weight += 1
    except:
        weight = 0
        total_score = 0
    finally:
        return total_score, weight


# Removing Noise Function
def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|' \
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


# Get All Words
def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token


# Get tweets For Model
def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


# Homogenizing input data such as language
def source_homogenization(nlp_entry):
    translator = Translator()
    data_list = remove_emoji(nlp_entry)
    custom_tweet = translator.translate(data_list, src='auto', dest='en').text
    custom_tokens = remove_noise(word_tokenize(custom_tweet))
    return custom_tweet, custom_tokens


# data Training Function
def data_training():
    # Fill Data for Data Set
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]
    tweet_tokens.append(twitter_samples.tokenized('negative_tweets.json')[0])
    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    # Removing Noise
    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    # Fill DataSet
    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset
    random.shuffle(dataset)

    # Train DataSet
    train_data = dataset[:12500]
    test_data = dataset[7500:]
    classifier = NaiveBayesClassifier.train(train_data)

    # Accuracy Result Printing
    print('Result accuracy cannot understand the meaning of sentence yet')
    print("Accuracy is:", classify.accuracy(classifier, test_data))
    return classifier


# Result Function
def nlp_processing(tweet_entry):
    custom_tweet, custom_tokens = source_homogenization(tweet_entry)
    # tagged_tweet = pos_tag(custom_tokens)         ##unused
    result = (custom_tweet, classifier.classify(dict([token, True] for token in custom_tokens)))
    # return translated sentence and its polarity
    return result[0], result[1]


# Value of Polarity
def tweet_assessment(data_entry):
    global sentiment
    custom_tweet, polarity = nlp_processing(data_entry)
    blob = TextBlob(custom_tweet)
    blob.tags
    blob.noun_phrases
    sentiment = 0
    for sentence in blob.sentences:
        value = sentence.sentiment.polarity
        sentiment += value
    emoji_score, emoji_weight = analysis_emoji(data_entry)
    final_value = (sentiment + emoji_score) / (emoji_weight + 1)
    if final_value == 0:
        polarity = 1003
    if final_value > 0 and polarity != 'Positive':
        polarity = 1001
    if final_value < 0 and polarity != 'Negative':
        polarity = 1002
    if polarity == 'Positive':
        polarity = 1001
    if polarity == 'Negative':
        polarity = 1002
    return final_value, polarity


# final functions is tweet_assessment

# train data for one time
classifier = data_training()
