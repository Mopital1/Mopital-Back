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