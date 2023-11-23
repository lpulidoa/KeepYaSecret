import numpy as np
from scipy.optimize import linprog
from itertools import product
import string

ALPHABET = string.ascii_uppercase
#test="BVKAHSEZUTEYIEOTBDOKPEOESKQCNNAELTUEYTINGFIELSBMEKPIAGTFAAGISWGMRUGYMVRNTYWUTHYFCRRBAUNOEMEZSNBWYFCRRTHVWNRTHRBIZTHZVKVNGFBMRFEVTIASOZVCEEDZJLRWOLTDLOUDQNQMAPJEYINBQNYOVVUEYOVVUEOABPIRRYOLLOJNCRVYBULVBMRKNFELBVEDMTUANBGOHLERDEZEPLBIGDONVTUENZBSGIMVBOTOGVBIGLIBMYBULFDEZEBLBYBUDFVTOOYZBSWUSKNOESHFETNKEZBOELERDEVTYFCGBTTRBAXEIKWRYEAMMIGLIBMUUDOEBWNNTPWUVNMPJLBODCQNRYERPJHSTNINAAHRDENGOFLTVMEPMAUANUVOAEEUBONPOCWGVZEEWBHTYFCGBNHRDEGOLVBTUISJPIGGOUWNGWAEBYBUIEUYOLOFLLVNEPMAUNOKBRLNADIKRYOLILYMIEMYRAHRVDAONVMDGOAGWLBGIQMNBBUKGOHGOEPAIETFTEGTHZASUITXWYRAHEWWRWOEBBRTACSIAGTYMNRXTUIYVAIEBGBTNFBHVNTFAALHECTNNHIRQNGLOFSIAFOIUYBNEKZURLOMMYRAHKPAGSHZXSNILVLAJAY"

#test=input("Message\n\n")


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def gcd_counts(numbers, gcd_dict):
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            common_divisor = gcd(numbers[i], numbers[j])

            if common_divisor not in gcd_dict:
                gcd_dict[common_divisor] = 1
            else:
                gcd_dict[common_divisor] += 1

    return gcd_dict

def factorize_number(number, factors_dict):
    # Factorize the number and update the factors_dict
    
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            # If i is a factor, store it in the dictionary with its pair
            factors_dict[i] = factors_dict.get(i, 0) + 1
            factors_dict[number // i] = factors_dict.get(number // i, 0) + 1

def find_repeating_distances(input_string, min_length=3, max_length=5):
    repeating_distances = []
    substring_positions = {}
    for length in range(min_length, max_length + 1):
       for i in range(len(input_string) - length + 1):
          substring = input_string[i:i+length]
          if substring in substring_positions:
              distance = i - substring_positions[substring]
              repeating_distances.append(distance)
          substring_positions[substring] = i

    return repeating_distances


def factorize_or_gcd(numbers,output_size):
    factors_dict = {}

    # Try to factorize each number
    for number in numbers:
        try:
            factorize_number(number, factors_dict)
        except TimeoutError:
            print("Factorization took too long. Calculating GCD instead.")
            return gcd_counts(numbers, factors_dict)

    array_factors = [[key, value] for key, value in factors_dict.items()]
    array_factors.append([1,0])
    # Sort the array in descending order based on the values
    sorted_factors = sorted(array_factors, key=lambda x: x[1], reverse=True)[:output_size]
    return sorted_factors



def kasiski_test(input_string, min_length=3, max_length=5,output_number=5):
    # Step 1: Find repeating distances
    distances = find_repeating_distances(input_string, min_length, max_length)

    # Step 2: Use Kasiski test to find potential key lengths
    potential_key_lengths = [row[0] for row in factorize_or_gcd(distances,output_number)]

    return potential_key_lengths

##Finished Kasiski's test
# 
#     
def arrange_text_in_matrix(text, m):
    # Initialize the 2D matrix with empty strings
    matrix = ['' for _ in range(m)]

    # Populate the matrix with characters from the text
    for i, char in enumerate(text):
        row_index = i % m
        matrix[row_index] += char

    return matrix

def char_freq(input_string):
    # Uses dictionary to store frequencies
    frequencies = {}
    for char in input_string:
        # Skip non-alphabetic characters
        if char.isalpha():
            frequencies[char] = frequencies.get(char, 0) + 1
    return frequencies


def IC(text):
    # Calculate frequencies of characters in the text
    char_frequencies = char_freq(text)

    # Calculate the sum of freq comb 2
    sum_of_squares = sum(freq*(freq-1) for freq in char_frequencies.values())

    # Calculate the index of coincidence
    text_length = len(text)
    ic = round(sum_of_squares / (text_length * (text_length - 1)),3)

    return ic




def best_key_sizes(plain_text, num_sizes,target_IC):
    # Returns list of tuples of (key, IC(key))
    # best key sizes begining with highes scoring key in IC key
    # Create dictionary {key size: IC(key size)}
    possible_sizes=kasiski_test(plain_text)
    keys_score={}

    for m in possible_sizes:
        
        matrix_text=arrange_text_in_matrix(plain_text, m)
        average_ic =0

        for i in range(len(matrix_text)):
            average_ic+=IC(matrix_text[i])

        average_ic/=len(matrix_text)
        keys_score[m]=round(average_ic,3) 
    # Sort the list by index_of_coincidence in descending order
    sorted_ic = sorted([(m,keys_score[m], round(abs(keys_score[m] - target_IC),3)) for m in keys_score.keys()], key=lambda x: x[2], reverse=False)
    #Take the num_sizes best key sizes excluding unlikely options like 1 or 2
    best_lens=[]
    for l in sorted_ic:
        if l[0] not in {1,2}:
            best_lens.append(l[:2])
        if len(best_lens)==num_sizes:
            break
    #if there are no other options, add the best one available  
    if(len(best_lens)==0): #or len(best_lens)==1):
          best_lens.append(sorted_ic[0][:2])
    return best_lens

spanish_frequencies = [0.1253, 0.0142, 0.0468, 0.0586, 0.1368, 0.0069, 0.0101, 0.007, 0.0625, 0.0044, 0.0002, 0.0497, 0.0315, 0.0702, 0.0868, 0.0251, 0.0088, 0.0687, 0.0798, 0.0463, 0.0393, 0.009, 0.0001, 0.0022, 0.009, 0.0052]
english_frequencies = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]
english_value=round(sum([i**2 for i in english_frequencies]),3)
spanish_value=round(sum([i**2 for i in spanish_frequencies]),3)
languages={'english':[english_frequencies,english_value],'spanish':[spanish_frequencies,spanish_value]}
random_value=0.038

def shift_dict(dictionary, shift):
    alphabet = string.ascii_uppercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    shifted_dict = {k: dictionary.get(v, 0) for k, v in zip(alphabet, shifted_alphabet)}
    return shifted_dict

def MgFilter(mg_array, target):

    indexed_diff = [(i, mg_array[i], abs(mg_array[i] - target)) for i in range(len(mg_array))]

    # Sort the list by absolute difference in descending order
    sorted_indexed_diff = sorted(indexed_diff, key=lambda x: x[2], reverse=False)
    
    # Extract the sorted array
    sorted_array = [(index, value) for index, value, _ in sorted_indexed_diff]
    best_scores=sorted_array[:3]
    best_score=best_scores[0]
    # Filter other options based on closeness
    other_options=[mg for mg in best_scores[1:] if is_close_enough(random_value,target,mg[1])]
    # Combine best_score and other_options into a single list
    best_scores = [best_score] + other_options

    return best_scores

def dot_prod(list1,list2):
    result=0
    for j in range(len(list1)):
        result+=list1[j]*list2[j]


def calculate_Mg(input_string, key_size, language_frequencies,language_IC):
    matrix = arrange_text_in_matrix(input_string, key_size)
    best_keys = {}
    str_counter=0

    for string in matrix:
        Mgs = []
        char_freq_dict = char_freq(string)

        for g in range(26):

            shifted_char_freq_dict = shift_dict(char_freq_dict, g)
            dot_product = round(np.dot(language_frequencies, list(shifted_char_freq_dict.values())),3)
            Mg=round(dot_product/len(string),3)
            Mgs.append(Mg)
        Mgs=MgFilter(Mgs,language_IC)
        best_keys[str_counter]=Mgs
        str_counter+=1

    return best_keys

def is_close_enough(r_value,exp_value,test_value):
    max_distance=round(abs(r_value-exp_value)/2,3)
    good_IC= abs(exp_value-test_value)<max_distance
    return good_IC

def extract_keys(mg_dictionary):
    extracted_keys = []

    for combination in product(*mg_dictionary.values()):
        char_string = ''.join(chr(65 + int(pair[0])) for pair in combination)
        avg_score = round(sum(pair[1] for pair in combination) / len(combination))
        extracted_keys.append([char_string, avg_score])

    return extracted_keys

def vigenereDecryptKey(frase:str, clave): 

    if "".join(clave.split()).isalpha():
    
      clave_list = []
      for letra in clave.upper():
          clave_list.append(ALPHABET.index(letra))

      newFrase = ""

      contador = 0

      for letra in list(frase):
          letra = ALPHABET[(ALPHABET.index(letra) - clave_list[contador]) % len(ALPHABET)]
          newFrase = newFrase + letra
          contador = (contador + 1) % len(clave)
          

      return (newFrase) 
    else:
      print("The key must be a word or a phrase made up of letters.")

def output_format(last_dict):
    final_array=[(last_dict[key][1][0][2],last_dict[key][1][0][0],last_dict[key][0]) for key in last_dict.keys()]
    return final_array

def vigenere_cryptanalysis(input_text, lang_info=languages['english']):
    #1<=length of key_sizes<=3
    keys_dict={}
    key_sizes=best_key_sizes(input_text, 20,lang_info[1])
    if (len(key_sizes))>=1:
          best_key_size=[key_sizes[0],key_sizes[1]]
          second_options=[key for key in key_sizes[1:] if is_close_enough(random_value,lang_info[1],key[1])]
          key_sizes=best_key_size+second_options           
    besti=0
    for item in key_sizes:
        if besti==0:
            besti=item[0]
        m=item[0]
        value=item[1]
        # Call the calculate_Mg function for each key in size_scores
        mg_dict = calculate_Mg(input_text, m, lang_info[0],lang_info[1])
        keys=extract_keys(mg_dict)
        text_and_keys=[item+[vigenereDecryptKey(input_text,item[0])] for item in keys]
        # Append the corresponding value from size_scores and the mg_dict to the result list
        keys_dict[m] = [value, text_and_keys]
    keys_array=output_format(keys_dict)
    return keys_array

