#lang racket/base

(require rackunit
         "hj.rkt")

(require "util.rkt")
(require racket/list)


; [TODO] check more util output values

; modinv
;; (check-equal? 9 (modinv 5 11))
;; (check-equal? 5 (modinv 9 11))
;; (check-equal? 8 (modinv 7 11))
;; (check-equal? #f (modinv 8 12))
;; (check-equal? 5 (modinv 5 12))

; [TODO] break out into utils
;; (let ([e (wrap-affineenc 26 5 8)]
;;       [p '(0 5 5 8 13 4 2 8 15 7 4 17)]
;;       [q '(8 7 7 22 21 2 18 22 5 17 2 15)]
;;       [alpha '(8 13 18 23 2 7 12 17 22 1 6 11 16 21 0 5 10 15 20 25 4 9 14 19 24 3)])
;;   (check-equal? q (map e p))
;;   (check-equal? alpha (map e (range 26))))

#| (check-equal? (my-+ 1 1) 2 "Simple addition") |#
#| (check-equal? (my-* 1 2) 2 "Simple multiplication") |#

(define MESSAGE-PLAIN "HELLO, WORLD!")
(define MESSAGE-STRICT "HELLOWORLD")

(check-equal? (string-encrypt/affine MESSAGE-PLAIN 7 3 #:strict #t) "AFCCXBXSCY")
(check-equal? (string-encrypt/affine MESSAGE-PLAIN 7 3 #:strict #f) "AFCCX, BXSCY!")
(check-equal? (string-decrypt/affine "AFCCXBXSCY" 7 3 #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/affine "AFCCX, BXSCY!" 7 3 #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/affine "AFCCX, BXSCY!" 7 3 #:strict #f) MESSAGE-PLAIN)

(check-equal? (string-encrypt/atbash MESSAGE-PLAIN #:strict #t) "SVOOLDLIOW")
(check-equal? (string-encrypt/atbash MESSAGE-PLAIN #:strict #f) "SVOOL, DLIOW!")
(check-equal? (string-decrypt/atbash "SVOOLDLIOW" #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/atbash "SVOOL, DLIOW!" #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/atbash "SVOOL, DLIOW!" #:strict #f) MESSAGE-PLAIN)

(check-equal? (string-encrypt/caesar MESSAGE-PLAIN 3 #:strict #t) "KHOORZRUOG")
(check-equal? (string-encrypt/caesar MESSAGE-PLAIN 3 #:strict #f) "KHOOR, ZRUOG!")
(check-equal? (string-decrypt/caesar "KHOORZRUOG" 3 #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/caesar "KHOOR, ZRUOG!" 3 #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/caesar "KHOOR, ZRUOG!" 3 #:strict #f) MESSAGE-PLAIN)

(check-equal? (string-encrypt/decimation MESSAGE-PLAIN 7 #:strict #t) "XCZZUYUPZV")
(check-equal? (string-encrypt/decimation MESSAGE-PLAIN 7 #:strict #f) "XCZZU, YUPZV!")
(check-equal? (string-decrypt/decimation "XCZZUYUPZV" 7 #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/decimation "XCZZU, YUPZV!" 7 #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/decimation "XCZZU, YUPZV!" 7 #:strict #f) MESSAGE-PLAIN)

(check-equal? (string-encrypt/rot13 MESSAGE-PLAIN #:strict #t) "URYYBJBEYQ")
(check-equal? (string-encrypt/rot13 MESSAGE-PLAIN #:strict #f) "URYYB, JBEYQ!")
(check-equal? (string-decrypt/rot13 "URYYBJBEYQ" #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/rot13 "URYYB, JBEYQ!" #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/rot13 "URYYB, JBEYQ!" #:strict #f) MESSAGE-PLAIN)

(check-equal? (string-encrypt/keyword MESSAGE-PLAIN "KANGAROO" #:strict #t) "CRHHLWLQHG")
(check-equal? (string-encrypt/keyword MESSAGE-PLAIN "KANGAROO" #:strict #f) "CRHHL, WLQHG!")
(check-equal? (string-decrypt/keyword "CRHHLWLQHG" "KANGAROO" #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/keyword "CRHHL, WLQHG!" "KANGAROO" #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/keyword "CRHHL, WLQHG!" "KANGAROO" #:strict #f) MESSAGE-PLAIN)

;(check-equal? (string-encrypt/vigenere MESSAGE-PLAIN "OCEANOGRAPHY" #:strict #t) "DRHHLWLQHG")
