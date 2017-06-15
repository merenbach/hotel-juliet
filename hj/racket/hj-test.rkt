#lang racket/base
 
(require rackunit
         "hj.rkt")

#| (check-equal? (my-+ 1 1) 2 "Simple addition") |#
#| (check-equal? (my-* 1 2) 2 "Simple multiplication") |#


(check-equal? (string-encrypt-affine "AFFINE CIPHER" 5 8 #:strict #t) "IHHWVCSWFRCP")
(check-equal? (string-encrypt-affine "AFFINE CIPHER" 5 8 #:strict #f) "IHHWVC SWFRCP")

(check-equal? (string-decrypt-affine "IHHWVCSWFRCP" 5 8 #:strict #t) "AFFINECIPHER")
(check-equal? (string-decrypt-affine "IHHWVC SWFRCP" 5 8 #:strict #f) "AFFINE CIPHER")
