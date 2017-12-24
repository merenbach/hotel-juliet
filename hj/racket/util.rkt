#lang racket/base

;(require math/number-theory)
;(require memoize)

; [TODO] can define affine as lcg, as well

;(define/memo (tabularectaenc b m . rest-id)
(define (tabularectaenc b m . rest-id)
  ; Store tabula recta encryption parameters to operate on individual numbers
  (modulo (apply + b rest-id) m))

;(define/memo (tabularectadec b m . rest-id)
(define (tabularectadec b m . rest-id)
  ; Store tabula recta decryption parameters to operate on individual numbers
  (modulo (- b (apply + rest-id)) m))

(define (wrap-tabularectaenc m)
  (lambda (b . rest-id)
    (apply tabularectaenc b m rest-id)))
(define (wrap-tabularectadec m)
  (lambda (b . rest-id)
    (apply tabularectadec b m rest-id)))


;; to encode:
;; zeroeth: convert alphabet to list
;; first, get to-number/from-number for alphabet
;; second, convert message to numbers with above mechanism
;; third, map these numbers to output
;; fourth, map output to letters/chars again
;; --> question: what about strict?  takes place between steps one and three?

;; (define (coprime? . rest-id)
;;   ;; Are all arguments coprime?
;;   (= 1 (apply gcd rest-id)))

;; ; from https://stackoverflow.com/questions/13096491/multiplicative-inverse-of-modulo-m-in-scheme
;; (define (egcd a b)
;;   (if (zero? a)
;;       (values b 0 1)
;;       (let-values (((g y x) (egcd (modulo b a) a)))
;;         (values g (- x (* (quotient b a) y)) y))))
;;       ;(let-values (((g x y) (egcd (modulo b a) a)))
;;       ;  (values g (- y (* (quotient b a) x)) x))))

;; ; todo: use b n instead of a m
;; (define (modinv a m)
;;   (let-values (((g x y) (egcd a m)))
;;     (if (not (= g 1))
;;         #f
;;         (modulo x m))))

(provide wrap-tabularectaenc wrap-tabularectadec)
