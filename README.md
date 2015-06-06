# Hotel Juliet

## What is it?

Hotel Juliet is a framework for classic cryptographic ciphers.  Currently this means various monoalphabetic substitution, polyalphabetic substitution, and transposition ciphers.

If your project requirements include such terms as `AES`, `DES`, `block`, `stream`, or `asymmetric`, it is possible (if not probable) that this framework will disappoint.

This started out as a PHP/JavaScript project long ago. Throughout the years it has transitioned through Perl to its current incarnation in Python.

## What does *Hotel Juliet* mean?

I have no idea where the initialism `HJ`, expanded to the above phrase with the [NATO phonetic alphabet] [1], originated, but [this page] [2] indicates that *Hotel Juliet* occurs when it is time to change one’s keys in an organized (i.e., government-sponsored) program of cryptography.  It seemed memorable enough so I ran with it.

  [1]: http://en.wikipedia.org/wiki/NATO_phonetic_alphabet "NATO phonetic alphabet"
  [2]: http://jproc.ca/crypto/terms.html "Common Crypto Terms"

## What ciphers are supported?

The underlying frameworks are a bit of a playground for me right now.  The code may is messy and under-documented and APIs remain subject to change.  Current ciphers include:

  * Substitution
    * Monoalphabetic
      * Affine
      * Atbash
      * Caesar
      * Keyword
    * Polyalphabetic
      * Beaufort
      * Della Porta
      * Gronsfeld
      * Trithemius
      * Variant Beaufort
      * Vigenère
    * Transposition
      * Scytale (prototype)

# [TODO]: Allow shifting a la
    # http://rumkin.com/tools/cipher/caesar-keyed.php

TODO:
Handle translation in subclasses for cipher, then pass alphabet_ to super() instead of list of ops?
autotranslate to upper case?
- use dict of individual dicts instead of str.maketrans (which also makes dicts)? seems less efficient
    {'a': {'a':'q', 'b':'r'...
  - test whether keys/alphas actually have to be strings


## Notes

* This project uses the [NumPy/SciPy] [3] documentation style.

* More robust tests are needed on everything, including utility classes (alphabet, flexible sequence mixin, etc.).


  [3]: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
