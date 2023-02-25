''' Process the results of the quantum circuit into GPT3 inputs. '''
import numpy as np


def filter_errors(result):
    ''' Detect errors and remove it from the results '''
    return {key: value for key, value in result.items() if key.count('1') == 1}


def convert_binary_to_index(binary_string):
    ''' Convert binary strings to indices (e.g. '00010' -> 1 and '10000' -> 4) '''
    if '1' in binary_string:
        return len(binary_string) - binary_string.index('1') - 1
    raise ValueError('Binary string must contain at least one 1')


def order_results(result):
    ''' Order results using the original index '''
    ordered_result = []
    for key, value in result.items():
        index = convert_binary_to_index(key)
        ordered_result.append([index, key, value])
    ordered_result.sort()
    return ordered_result


def convert_to_places(result, places, total_shots):
    ''' Convert quantum results to places (e.g. [1, '00010', 85] -> ['Opera', 0.085]) '''
    readable_result = []
    for line in result:
        place = places[line[0]][0]
        probability = line[2] / total_shots
        readable_result.append([place, probability])
    return readable_result


def convert_probability_to_likelyhood(probability):
    ''' Method to convert probabilities to likelyhoods strings.'''
    if 0 <= probability < 0.25:
        return "wasn't at the "
    elif 0.25 <= probability < 0.75:
        return "may have gone to the "
    elif 0.75 <= probability <= 1.0:
        return "likely went to the "
    else:
        raise ValueError('Probability must be between 0 and 1.')


def entropy(probabilities):
    '''Compute the normed entropy of the probability distribution.'''
    if isinstance(probabilities, list):
        probabilities = np.array(probabilities)
    scaled = -probabilities * np.log(probabilities)
    scaled[np.isnan(scaled)] = 0

    entropy_max = np.log(len(probabilities))
    entropy_val = np.sum(scaled)
    return entropy_val / entropy_max


def convert_entropy_to_words(normed_entropy):
    '''Convert the entropy value to a word.'''
    if 0 <= normed_entropy < 0.1:
        return "uneventful"
    elif 0.1 <= normed_entropy < 0.4:
        return "boring"
    elif 0.4 <= normed_entropy < 0.6:
        return "regular"
    elif 0.6 <= normed_entropy < 0.9:
        return "exciting"
    elif 0.9 <= normed_entropy < 1.0:
        return "chaotic"
    else:
        raise ValueError('Entropy must be between 0 and 1.')
