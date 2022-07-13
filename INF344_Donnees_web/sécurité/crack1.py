"""The goal of this lab is to crack passwords with different standard methods. 
Each student has their own set of passwords waiting to be cracked. 

1) Put your name (as it appears in the password file name) in the variable NAME below.
2) Implement the functions at the bottom of this template,
   calling check_password(.) with each possible password.

The deadline is today at the end of the lab!
"""

import hashlib
from urllib.request import urlopen
from urllib.parse import urlencode


# TODO: write your last name here (must match the name of the password file)
NAME = "samir".lower()

# This file contains original passwords but encrypted.
# It is used for validating passwords your cracked locally.
# If there is a match, this match is sent to the server.
ENCFILE = "INF344_2021_2022_enc/" + NAME + ".enc"

# Leaderboard address
SERVER_ADD = 'http://137.194.211.123/' # DO NOT CHANGE THIS VALUE!!!

import string
import itertools

class Crack:
    """Password Cracking"""

    def __init__(self, filename, name):
        """
        -------------------
        This method should not be modified !!
        ------------------

        Initialize the cracking session
        :param filename: The file with the encrypted passwords
        :param name: Your name
        :return: Nothing
        """
        self.name = name.lower()

        # load the encrypted passwords
        self.passwords = self.get_passwords(filename)

    def get_passwords(self, filename):
        """
        -------------------
        This method should not be modified !!
        ------------------

        Get the passwords from a file
        :param filename: The name of the file which stores the passwords
        :return: The set of passwords
        """
        passwords = set()
        with open(filename, "r") as f:
            for line in f:
                passwords.add(line.strip())
        return passwords

    def check_password(self, password):
        """
        -------------------
        This method should not be modified !!
        ------------------

        Checks if the password you give is correct
        :param password: A string representing the password
        :return: Whether the password is correct or not
        """
        password = str(password)
        cond = hashlib.md5(bytes(password, "utf-8")).hexdigest() in \
               self.passwords
        if cond:
            args = {"name": self.name,
                    "password": password}
            args = urlencode(args, "utf-8")
            page = urlopen(SERVER_ADD + 'submit?' + args)
            if b'True' in page.read():
                print("You found the password: " + password)
                return True
        return False

    def evaluate(self):
        """
        -------------------
        This method should not be modified !!
        ------------------

        Retrieve the grade from the server,
        """
        args = {"name": NAME}
        args = urlencode(args, "utf-8")
        page = urlopen(SERVER_ADD + 'evaluate?' + args)
        print("Grade :=>> " + page.read().decode('ascii').strip())

    def crack(self):
        """
        -------------------
        This method should be modified carefully !!
        ------------------

        Cracks the passwords. YOUR CODE GOES IN THE METHODS BELOW.

        We suggest you use one function per question. Once a password is found,
        it is memorized by the server, thus YOU CAN COMMENT THE CALL to the
        corresponding function once you find all the corresponding passwords.
        """
        self.bruteforce_digits()
        #self.bruteforce_letters()
        #self.dictionary_passwords()
        #self.dictionary_passwords_leet()
        #self.dictionary_words_hyphen()
        #self.dictionary_words_digits()

    # You code goes here.
    # Call the function check_password(.) with all possible passwords
    def bruteforce_digits(self):
        # Via brute-force, find passwords with *up to* 9 digits (max is 999,999,999)
        # [4 passwords / 1 point]
        for i in range(9):
            for cb in itertools.product(string.digits, repeat=i+1):
                self.check_password("".join(cb))

    def bruteforce_letters(self):
        # Via brute-force, find passwords with *up to* 5 letters in upper or lower case, e.g, zPLsD
        # [4 passwords / 1 point]
        # TODO: Your code here
        for i in range(1,6):
            for pw in itertools.product(string.ascii_letters, repeat=i):
                self.check_password("".join(pw))

    def dictionary_passwords(self):
        # Use the list of the 1k most common passwords and try all of them (lowercase)
        # [1k most common passwords]
        # [2 passwords / 1 point]
        for pw in open("1000-most-common-passwords.txt","r").read().split("\n"):
            self.check_password(pw)

    def dictionary_passwords_leet(self):
        # Reuse the 1k most common passwords, and apply the transformations e -> 3, l -> 1, a -> @, i -> 1, o -> 0 -- to all possible combinations of possible positions
        # [1k most common passwords]
        # [3 passwords / 1 point]
        ch = ["e","l","a","i","o"]
        dict_ = {"e":"3", "l":"1", "a":"@", "i":"1", "o":"0"}
        for pw in open("1000-most-common-passwords.txt","r").read().split("\n"):
            indices = [i for i, ltr in enumerate(pw) if ltr in ch]
            for repl in itertools.product(["0","1"],repeat=len(indices)):
                pwcp = list(pw)
                for r, i in zip(repl, indices):
                    if r=="1":
                        pwcp[i] = dict_[pwcp[i]]
                self.check_password("".join(pwcp))

    def dictionary_words_hyphen(self):
        # Use the 10k most common English words (lowercase) with up to 3 randomly added hyphens inside the word, as in h-e-ll-o
        # Passwords CANNOT begin or end with '-', and there CANNOT be two '-' in a row
        # [10k most common English words]
        # [3 passwords / 1 point]
        for pw in open("google-10000-english.txt","r").read().split("\n"):
            for j in range(3):
                for idx in itertools.combinations(list(range(len(pw)-1, 0,-1)),j+1):
                    pwc = pw
                    for i in idx:
                        pwc = pwc[:i] +"-"+ pwc[i:] 
                        self.check_password(pwc)

    def dictionary_words_digits(self):
        # Concatenate the 10k most common English words (lowercase) to a minimum length of 19, plus a two-digit number
        # [10k most common English words]
        # e.g., computers + democrates + 01 -> computersdemocrates01
        # len(computersdemocrates) >= 19
        # [4 passwords / 1 point]
        words = open("google-10000-english.txt","r").read().split("\n")
        for word1, word2 in itertools.permutations(words, 2):
            if len(word1+word2) < 19: continue
            for j in range(100):
                digit = str(j).zfill(2)
                self.check_password(word1+word2+digit)

if __name__ == "__main__":
    crack = Crack(ENCFILE, NAME)
    crack.crack()
    crack.evaluate()
