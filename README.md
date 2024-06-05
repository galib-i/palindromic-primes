## Palindromic Primes Finder
An Algorithms and Data Structures assignment of developing a *unique* "special number" finder program - finding palindromic primes within a given range:
- Acceptance of only positive inputs
- Display of the count of special numbers
- Display of the first and last three special numbers; if the total is less than six, all are displayed
- Limited to a maximum of five hardcoded values
- Utilization of exclusively built-in libraries

Although the time complexity is O(n^3), it outperforms other solutions with the same requirements, especially for extremely large ranges (e.g. 1 to 1 trillion in ~1 second). The key aspects are palindrome generation and primality check.

They are explained in the code itself, but in short:

#### Palindrome Generation
For each palindrome with three or more digits, there exists a shorter palindrome nested within it. For example, the palindrome 13231 contains the palindrome 323, which in turn contains the digit 2. Even-digit palindromes are avoided as they are all multiples of 11.

#### Primality Check
Utilises Fermat's Little Theorem on a filtered list of palindromes, avoiding all failures (false positives).

```python
pow(2, number - 1, number) == 1  # 2^(number-1) ≡ 1 MOD number
```
