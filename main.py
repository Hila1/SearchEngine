import pickle
import re
import shutil


def review_order(input_file_name, output_details_file_name):
    dictionary_reviews = {}
    dictionary_review_details = {}
    input_file = open(input_file_name, 'r')
    counter = 1
    #for every review in the reviews file
    for line in input_file:
        product_id = re.search(r'product/productId.*', line)
        helpfulness = re.search(r'review/helpfulness.*', line)
        score = re.search(r'review/score.*', line)
        # if productID is separated into 2 lines -> connect them into one line
        if product_id is not None:
            product_id = re.sub(r'^product/productId:', "", line)
            product_id = product_id.replace("\n", "")
            dictionary_review_details["productId"] = product_id
        # if helpfulness is separated into 2 lines -> connect them into one line
        elif helpfulness is not None:
            helpfulness = re.sub(r'^review/helpfulness:', "", line)
            helpfulness = helpfulness.replace("\n", "")
            dictionary_review_details["helpfulness"] = helpfulness.split("/")
        # if score is separated into 2 lines -> connect them into one line
        elif score is not None:
            score = re.sub(r'^review/score:', "", line)
            score = score.replace("\n", "")
            dictionary_review_details["score"] = score
            dictionary_reviews[counter]=dictionary_review_details
            dictionary_review_details= {}
            counter+=1

    save_obj(dictionary_reviews, output_details_file_name)
    print(load_obj(output_details_file_name))


def text_order(input_file_name, output_file_name):
    counter = 1
    dictionary_text = {}
    input_file = open(input_file_name, 'r')
    for line in input_file:
        text = re.search(r'review/text.*', line)
        product_id = re.search(r'product/productId.*', line)
        # if text is separated into 2 lines -> connect them into one line
        if text is not None:
            if product_id is None:
                for line2 in input_file:
                    if re.search(r'^product', line2) is not None:
                        break
                    line += line2
            text = re.sub(r'^review/text:', "", line)
            text = text.lower()
            text = text.strip()
            text = re.split(r'\W+', text)
            text = set(text)#need aa fix!!!!
            text.discard('')
            for word in text:
                if word in dictionary_text:
                    reviews_list = dictionary_text[word]
                else:
                    reviews_list = []
                reviews_list.append(counter)
                dictionary_text[word]= reviews_list
            counter += 1
    save_obj(dictionary_text, output_file_name)
    print(load_obj(output_file_name))

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
class SlowIndexWriter:
    """
    Given product review data, creates an on
    disk index
    inputFile is the path to the file containing
    the review data
    dir is the directory in which all index files
    will be created
    if the directory does not exist, it should be
    created"""
    def slowWrite(self, inputFile, dir):
        slash = "\\"
        output_file_name = "dictionary_index"
        output_details_file_name = "details_review_output"
        output_file_name = dir + slash + output_file_name if dir != "" else output_file_name
        output_details_file_name = dir + slash + output_details_file_name if dir != "" else output_details_file_name
        input_file = open(inputFile, 'r')
        review_order(inputFile, output_details_file_name)
        text_order(inputFile, output_file_name)
        input_file.close()

    def removeIndex(self, dir):
        """Delete all index files by removing the given
    directory"""
        shutil.rmtree(dir, ignore_errors=True)
    class IndexReader:
        def __init__(self):
            __dictionary_reviews = {}
            __dictionary_text = {}

        @property
        def dictionary_reviews(self):
            return self.dictionary_reviews

        @property
        def __dictionary_text(self):
            return self.__dictionary_text

        def IndexReader(self, dir):
            """Creates an IndexReader which will read from
        the given directory"""
            output_details_review_name = "details_review_output.pkl"
            output_index_file_name ="dictionary_index.pkl"
            self.dictionary_reviews = save_obj(dir+"//"+output_details_review_name)
            self.dictionary_text = save_obj(dir+"//"+output_index_file_name)
        def getProductId(self, reviewId):
            """Returns the product identifier for the given
        review
        Returns null if there is no review with the
        given identifier"""
            product_id  = self.dictionary_reviews[reviewId]["productId"]
            return product_id if product_id !=None else None
        def getReviewScore(self, reviewId):
            """Returns the score for a given review
        Returns -1 if there is no review with the given
        identifier"""
            score  = self.dictionary_reviews[reviewId]["score"]
            return score if score !=None else -1
        def getReviewHelpfulnessNumerator(self, reviewId):
            """Returns the numerator for the helpfulness of
        a given review
        Returns -1 if there is no review with the given
        identifier"""
            numerator  = self.dictionary_reviews[reviewId]["helpfulness"][0]
            return numerator if numerator !=None else -1
        def getReviewHelpfulnessDenominator(self, reviewId):
            """Returns the denominator for the helpfulness
        of a given review
        Returns -1 if there is no review with the given
        identifier"""
            numerator  = self.dictionary_reviews[reviewId]["helpfulness"][1]
            return numerator if numerator !=None else -1
        def getReviewLength(self, reviewId):
            """Returns the number of tokens in a given
        review
        Returns -1 if there is no review with the given
        identifier"""
            counter = 0
            tokens = {}
            tokens = self.dictionary_text
            keys = tokens.keys()
            for key in keys:
                if tokens[key].contains[reviewId]:
                    counter += 1

        def getTokenFrequency(self, token):
            """Return the number of reviews containing a
        given token (i.e., word)
        Returns 0 if there are no reviews containing
        this token"""
            freq = len(self.dictionary_text[token])
            return freq if freq > 0 else 0
        def getTokenCollectionFrequency(self, token):
            """Return the number of times that a given
        token (i.e., word) appears in
        the reviews indexed
        Returns 0 if there are no reviews containing
        this token"""
        def getReviewsWithToken(self, token):
            """Returns a series of integers of the form id1, freq-1, id-2, freq-2, ... such
        that id-n is the n-th review containing the
        given token and freq-n is the
        number of times that the token appears in
        review id-n
        Note that the integers should be sorted by id
        Returns an empty Tuple if there are no reviews
        containing this token"""
        def getNumberOfReviews(self, ):
            """Return the number of product reviews
        available in the system"""
        def getTokenSizeOfReviews(self, ):
            """Return the number of tokens in the system
        (self, Tokens should be counted as many times as they
        appear)"""
        def getProductReviews(self, productId):
            """Return the ids of the reviews for a given
        product identifier
        Note that the integers returned should be
        sorted by id
        Returns an empty Tuple if there are no reviews
        for this product"""


s = SlowIndexWriter()
file_name= "100.txt"
directory= ""
s.slowWrite(file_name, directory)
