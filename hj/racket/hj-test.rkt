#lang racket/base

(require rackunit
         "hj.rkt")

#| (check-equal? (my-+ 1 1) 2 "Simple addition") |#
#| (check-equal? (my-* 1 2) 2 "Simple multiplication") |#

(define MESSAGE-PLAIN "HELLO, WORLD!")
(define MESSAGE-STRICT "HELLOWORLD")

(check-equal? (string-encrypt/affine MESSAGE-PLAIN 7 3 #:strict #t) "AFCCXBXSCY")
(check-equal? (string-encrypt/affine MESSAGE-PLAIN 7 3 #:strict #f) "AFCCX, BXSCY!")

(check-equal? (string-decrypt/affine "AFCCXBXSCY" 7 3 #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/affine "AFCCX, BXSCY!" 7 3 #:strict #f) MESSAGE-PLAIN)

(check-equal? (string-encrypt/atbash MESSAGE-PLAIN #:strict #t) "SVOOLDLIOW")
(check-equal? (string-encrypt/atbash MESSAGE-PLAIN #:strict #f) "SVOOL, DLIOW!")
(check-equal? (string-decrypt/atbash "SVOOLDLIOW" #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/atbash "SVOOL, DLIOW!" #:strict #f) MESSAGE-PLAIN)

(check-equal? (string-encrypt/caesar MESSAGE-PLAIN 3 #:strict #t) "KHOORZRUOG")
(check-equal? (string-encrypt/caesar MESSAGE-PLAIN 3 #:strict #f) "KHOOR, ZRUOG!")
(check-equal? (string-decrypt/caesar "KHOORZRUOG" 3 #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/caesar "KHOOR, ZRUOG!" 3 #:strict #f) MESSAGE-PLAIN)

(check-equal? (string-encrypt/decimation MESSAGE-PLAIN 7 #:strict #t) "XCZZUYUPZV")
(check-equal? (string-encrypt/decimation MESSAGE-PLAIN 7 #:strict #f) "XCZZU, YUPZV!")
(check-equal? (string-decrypt/decimation "XCZZUYUPZV" 7 #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/decimation "XCZZU, YUPZV!" 7 #:strict #f) MESSAGE-PLAIN)

(check-equal? (string-encrypt/rot13 MESSAGE-PLAIN #:strict #t) "URYYBJBEYQ")
(check-equal? (string-encrypt/rot13 MESSAGE-PLAIN #:strict #f) "URYYB, JBEYQ!")
(check-equal? (string-decrypt/rot13 "URYYBJBEYQ" #:strict #t) MESSAGE-STRICT)
(check-equal? (string-decrypt/rot13 "URYYB, JBEYQ!" #:strict #f) MESSAGE-PLAIN)
