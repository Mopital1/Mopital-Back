import re
import unicodedata
import random

def remove_special_characters(string):
    string = "".join(c for c in unicodedata.normalize("NFD", string) if unicodedata.category(c) != "Mn")
    return re.sub(r"[!@#$%'^&*()-+?_=,<>/]", "", string)


def get_user_email(first_name, last_name):
    """

    :param increment:
    :param first_name:
    :param last_name:
    :param year:
    :return:
    """
    # enlever les espaces au debut et a la fin
    last_name = last_name.strip().lower()   
    first_name = first_name.strip().lower()
    # enlever les accents
    last_name = remove_special_characters(last_name)
    first_name = remove_special_characters(first_name)
    #last_name = unidecode(last_name.replace("'", ""))
    #first_name = unidecode(first_name.replace("'", ""))
    # si le nom a des espaces, prendre le 1er mot
    if " " in last_name:
        last_name = last_name.split(" ")[0]
    # si le prenom a des espaces, prendre le 1er mot
    if " " in first_name:
        first_name = first_name.split(" ")[0]
    # si le prenom est vide, mettre un nom aleatoire
    if not first_name:
        first_name = "pat"
    # mettre un nombre aleatoire
    num = random.randint(1, 100)    
    user_email = f'{last_name}.{first_name}{num}@mopital.com'

    return user_email


def permutation(mpi, last, new):
    """
    This function swaps the values of two elements in a list at specified indices.
    
    :param mpi: The list in which elements are to be swapped.
    :param last: The index of the first element to be swapped.
    :param new: The index of the second element to be swapped.
    """
    last_tab = mpi[last]
    mpi[last] = mpi[new]
    mpi[new] = last_tab

def enc_decrypt_permutation(phrase):
    """
    Encrypts a phrase of maximum 6 characters by permuting its characters two by two using the permutation function.
    
    :param phrase: The phrase to be encrypted.
    :return: The encrypted phrase.
    """
    if len(phrase) > 6:
        raise ValueError("Phrase cannot be more than 6 characters.")
    encrypted_phrase = list(phrase)
    for i in range(0, len(phrase) - 1, 2):
        permutation(encrypted_phrase, i, i + 1)
    return "".join(encrypted_phrase)

# def decrypt_permutation(phrase):
#     """
#     Decrypts a phrase that was encrypted using the encrypt_permutation function.
    
#     :param phrase: The encrypted phrase to be decrypted.
#     :return: The decrypted phrase.
#     """
#     if len(phrase) > 6:
#         raise ValueError("Phrase cannot be more than 6 characters.")
#     decrypted_phrase = list(phrase)
#     for i in range(len(phrase) - 1, 0, -2):
#         permutation(decrypted_phrase, i, i - 1)
#     return "".join(decrypted_phrase)