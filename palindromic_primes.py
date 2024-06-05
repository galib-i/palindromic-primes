"""
Author: Galib Islam
Description: a university assignment on a unique method for finding "special numbers"
            (palindromic primes) within a range, meeting all specified requirements
"""

from bisect import bisect_left, bisect_right
from time import time


def is_prime(number):
    """Uses a modified Fermat's Little Theorem for primality - all weaknesses are avoided
    by removing prior primes' multiples through the filter criteria"""
    return pow(2, number - 1, number) == 1  # 2^(number-1) ≡ 1 MOD number


def generate_filter_criteria(digit_count):
    """Returns a list of primes based on the upper limit's digit count, to filter out their
    multiples and Fermat's Little Theorem's false positives"""
    filter_length_limit = min(100, digit_count * 4)

    filter_criteria = [n for n in range(3, (filter_length_limit), 2) if is_prime(number=n)]
    filter_criteria.insert(0, 2)  # is_prime needs n > 2

    return filter_criteria


def trim_filter_criteria(values, lower_limit, upper_limit):
    """Removes primes that are not within the range of m and n and/or palindromes"""
    del values[5:]

    left_index = bisect_left(values, lower_limit)
    right_index = bisect_right(values, upper_limit)

    return values[left_index:right_index]


def generate_palindromes_in_digit(current_digit, upper_limit, palindromes):
    """Returns palindromes using palindromes with lesser digits
    e.g. 5 digit palindrome 13231 is created using 3 digit palindrome 323:
    - outer digits 10001 are generated
    - existing palindrome 323 is multiplied by 10^1, to get 3230
    - 3230 is added to 10001 to get 13231

    Args:
        current_digit (int): numbers of digits for the palindrome to be generated
                             e.g. 1 -> single digit, 3 -> triple digit
        upper_limit (int): end of the range
        palindromes (list): palindromes with less than the current number of digits

    Returns:
        list: palindromes with the current number of digits
    """
    if current_digit % 2 == 0:  # skip even digt palindromes - they're multiples of 11
        return []

    if current_digit == 1:  # single digit palindromes (including zero)
        return [n for n in range(10) if n <= upper_limit]

    # odd digit palindromes > 10
    # how many times the previous palindromes can be used to create new ones
    iterations = (current_digit - 1) // 2  # 1 iteration per 2 extra digits

    # palindromes with less than the current number of digits
    # the difference of the digit count is always a multiple of 2
    subdigit_palindromes = [palindromes[current_digit - (2 * i) - 3]  # simplified  "- (2 * (i + 1)) - 1"
                            for i in range(iterations)]

    current_digit_palindromes = []  # palindromes with the current number of digits

    for i in range(1, 10):  # populating current_digit_palindromes
        outer_digits = (i * (10**(current_digit - 1))) + i  # outer digits e.g. 1_ _ _1
        # generate inner digits, opposite direction to ensure palindromes are calculated in order
        for j in range(iterations - 1, -1, -1):
            position = 10**(j + 1)  # placeholder used to put inner digits in the correct place

            for k in subdigit_palindromes[j]:  # create new palindromes using subdigit_palindromes
                inner_digits = k * position
                palindrome = outer_digits + inner_digits

                if palindrome > upper_limit:  # don't add palindromes greater than n
                    return current_digit_palindromes

                current_digit_palindromes.append(palindrome)

    return current_digit_palindromes


def generate_palindromes(upper_limit, digits):
    """Returns a flattened list of palindromes between 1 and n, populate with sublists
    of palindromes with the same digit count - as per iteration"""
    palindromes = []

    for digit_count in range(1, digits + 1):
        palindromes.append(generate_palindromes_in_digit(current_digit=digit_count,
                                                         upper_limit=upper_limit,
                                                         palindromes=palindromes))
    return [element for sublist in palindromes for element in sublist]


def generate_special_numbers(lower_limit, upper_limit):
    """Finds all palindromic primes between m and n

    Args:
        lower_limit (int): start of the range (m)
        upper_limit (int): end of the range (n)

    Returns:
        list: palindromic primes between m and n
    """
    digit_count = len(str(upper_limit))

    special_numbers = generate_palindromes(upper_limit=upper_limit, digits=digit_count)

    left_index = bisect_left(special_numbers, lower_limit)  # remove numbers below lower limit
    del special_numbers[:left_index]

    filter_criteria = generate_filter_criteria(digit_count=digit_count)
    for filter_number in filter_criteria:  # reduce the amount of numbers to check for primality
        special_numbers = [n for n in special_numbers if n % filter_number != 0]

    special_numbers = [n for n in special_numbers if is_prime(number=n)]
    filter_criteria = trim_filter_criteria(values=filter_criteria, lower_limit=lower_limit,
                                           upper_limit=upper_limit)

    special_numbers = filter_criteria + special_numbers

    return special_numbers


def main():
    """Prompts the user for the range of numbers to find palindromic primes within"""
    while True:
        try:
            m = int(input("Enter the lower limit: "))
            n = int(input("Enter the upper limit: "))

        except ValueError:
            print("Both limits must be valid integers!\n")

        else:
            if n > m > 0:
                start_time = time()

                special_numbers = generate_special_numbers(lower_limit=m, upper_limit=n)
                special_numbers_amount = len(special_numbers)
                del special_numbers[3:-3]  # only keep the first 3 and last 3 numbers / all if < 6

                end_time = time()

                print(f"{special_numbers_amount}: {', '.join(map(str, special_numbers))}")
                print(f"Time taken: {end_time - start_time} seconds")
                break

            print("Lower limit must be less than the upper limit and both greater than 0!\n")


if __name__ == "__main__":
    main()
