# Hotel Juliet

## What is it?

Hotel Juliet is a framework for classic cryptographic ciphers.  Currently this means various monoalphabetic substitution, polyalphabetic substitution, and transposition ciphers.

If your project requirements include such terms as `AES`, `DES`, `block`, `stream`, or `asymmetric`, it is possible (if not probable) that this framework will disappoint.

This started out as a PHP/JavaScript project long ago. Throughout the years it has transitioned through Perl to its current incarnation in Python.

## What does _Hotel Juliet_ mean?

I have no idea where the initialism `HJ`, expanded to the above phrase with the [NATO phonetic alphabet] [1], originated, but [this page] [2] indicates that *Hotel Juliet* occurs when it is time to change one’s keys in an organized (i.e., government-sponsored) program of cryptography.  It seemed memorable enough so I ran with it.

  [1]: http://en.wikipedia.org/wiki/NATO_phonetic_alphabet "NATO phonetic alphabet"
  [2]: http://jproc.ca/crypto/terms.html "Common Crypto Terms"


## Why are keys specified upon cipher instantiation, rather than at encoding/decoding time?

In many cipher implementations, necessary keys and parameters are specified at encode/decode time, which represents more of a procedural or function-based (as opposed to object-oriented) standpoint.  Hotel Juliet takes a different approach, with the keys and parameters being specified when cipher objects are created.  For example:

    from ciphers import CaesarCipher
    c = CaesarCipher(4)
    c.encode('HELLO, WORLD!')
    CaesarCipher(4).encode('HELLO, WORLD!')  # or do it on one line

    from ciphers import VigenereCipher
    v = VigenereCipher('OCEANOGRAPHYWHAT')
    v.encode('HELLO, WORLD!')
    v = VigenereCipher('OCEANOGRAPHYWHAT').encode('HELLO, WORLD!')  # one line

This separation of concerns allows any cipher, once created, to be employed in exactly the same fashion as the others, with simple methods for encoding and decoding.

This may be revisited in the future if advantages can be found in combining or rearranging steps.


## What's with the keyword `alphabet` arguments everywhere?

Cryptography at its heart is little more than (often basic) mathematics, a universal language that transcends cultural and ethnic differences.  A properly-implemented cipher has little to fear from allowing an alphabet of 33 letters (e.g., Russian Cyrillic) or a set of 3,500 Chinese characters.

Even when restricted to cryptography of standard English, much can be accomplished by not relying on translating ASCII values directly, but instead by using lookup tables in some way, shape, or form, as alphabet variants now become possible with whitespace, basic punctuation, or digits.


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
      * Vigenère (text autokey)
      * Vigenère (key autokey)
    * Transposition
      * Scytale (prototype)

## Todo

  - Allow shifting a la <http://rumkin.com/tools/cipher/caesar-keyed.php>
  - Autotranslate to upper case?
  - Test whether keys/alphas actually have to be strings.
  - Add keyed Vigenere.
  - Tests should account for non-string and non-sequence keys.
  - Cardano cipher
  - Larrabee cipher
  - More cleanup of strict: does it belong in translation table, or elsewhere?
  - Redo all encipherment/decipherment using math?  For instance, polyalphabetic
    encryption/decryption can be done with mod(len alphabet) arithmetic,
    and the monoalphabetic is very simple.
  - More specifically, is the whole "translation table" idea inherently difficult
    to maintain and wrap one's head around?  Classes including classes that
    delegating to other classes...
  - Put countersign specification into encode/decode?
  - Support vigenere cube
  - Keyword cipher
  - Offset/shift using enumerate() in tabula recta
  - Customizable null padding char?
  - Modular arithmetic on negatives
    - Atbash multiplier and/or offset
    - CipherTableau transpose
    - Mod ring/mod\_sequence in utils

## DONE! but needs unit tests...

  - Handle block grouping and nulls again.


## Notes

  * This project endeavors to use the [NumPy/SciPy] [3] documentation style.
  * More robust tests are needed on everything, including utility classes (alphabet, flexible sequence mixin, etc.).


  [3]: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
