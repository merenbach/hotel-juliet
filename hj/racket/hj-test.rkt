#lang racket/base
 
(require rackunit
         "hj.rkt")

#| (check-equal? (my-+ 1 1) 2 "Simple addition") |#
#| (check-equal? (my-* 1 2) 2 "Simple multiplication") |#


(define AFFINE_ALPHABET
  (make-affine ALPHABET 5 8))

(define AFPAIR
  (xpair ALPHABET AFFINE_ALPHABET))

(check-equal? (encrypt-string AFPAIR #t "AFFINE CIPHER") "IHHWVCSWFRCP")
(check-equal? (encrypt-string AFPAIR #f "AFFINE CIPHER") "IHHWVC SWFRCP")

(check-equal? (decrypt-string AFPAIR #t "IHHWVCSWFRCP") "AFFINECIPHER")
(check-equal? (decrypt-string AFPAIR #f "IHHWVC SWFRCP") "AFFINE CIPHER")
