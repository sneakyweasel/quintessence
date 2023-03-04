''' Process the results of the quantum circuit into GPT3 inputs. '''
import numpy as np


def filter_errors(result):
    ''' Detect errors and remove it from the results '''
    return {key: value for key, value in result.items() if key.count('1') == 1}


def get_error_percentage(result):
    ''' Get the percentage of errors in the results '''
    errors = 0
    for key, value in result.items():
        if key.count('1') != 1:
            errors += value
    return errors / sum(result.values())


def convert_binary_to_index(binary_string):
    ''' Convert binary strings to indices (e.g. '00010' -> 1 and '10000' -> 4) '''
    if '1' in binary_string:
        return len(binary_string) - binary_string.index('1') - 1
    raise ValueError('Binary string must contain at least one 1')


def convert_index_to_binary(index, qbit_count):
    ''' Convert index to binary string (e.g. 3 -> '01000' and 4 -> '10000') '''
    zero_str = "0" * qbit_count
    zero_str = zero_str[:index] + "1" + zero_str[index + 1:]
    return zero_str[::-1]


def add_missing_results(result, qbit_count):
    ''' Add missing results to the result dictionary '''
    for i in range(qbit_count):
        binary_string = convert_index_to_binary(i, qbit_count)
        if binary_string not in result:
            result[binary_string] = 0
    return result


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


def compute_entropy(results):
    '''Compute the normed entropy of the probability distribution.'''
    probabilities = [line[1] for line in results]
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
    elif 0.1 <= normed_entropy < 0.2:
        return "boring"
    elif 0.2 <= normed_entropy < 0.3:
        return "regular"
    elif 0.3 <= normed_entropy < 0.5:
        return "exciting"
    elif 0.5 <= normed_entropy < 1.0:
        return "chaotic"
    else:
        raise ValueError('Entropy must be between 0 and 1.')


def create_gpt3_prompt(results, entropy):
    '''Method to create the GPT-3 prompt.'''

    # Initial place
    initial_place = results[0][0]

    # Convert numerical values to words
    entropy_adjective = convert_entropy_to_words(entropy)

    # Sort top 3 results
    results.sort(key=lambda x: x[1], reverse=True)
    results = results[:3]
    print(results)

    # Convert probabilities to readable GPT3 strings
    worded_results = []
    for result in results:
        likelyhood = convert_probability_to_likelyhood(result[1])
        place = result[0].lower()
        worded_results.append(likelyhood + place)

    prompt = '''Mr. Quanta cannot remember how he got here. Tell the story of him trying to
                remember how he got here in 3 steps and be descriptive.
                He only remembers a few things, and considers each possible place one at a time. 
                Use grandiose language. Embelish everything and paint a picture with words. 
                Make the descriptions drip with imagery. '''
    prompt += f"He had a { entropy_adjective } time before "
    prompt += f"awakening at the { initial_place.lower() }, and before that "

    # Append probability strings in the prompt
    for worded_result in worded_results:
        prompt += worded_result + ', '
    prompt += "."

    return prompt
