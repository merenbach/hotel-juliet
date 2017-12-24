#lang racket/base

;(require math/number-theory)
;(require memoize)

; [TODO] can define affine as lcg, as well

;(define/memo (affineenc a b m x)
(define (affineenc a b m x)
  ; y = (ax + b) % m
  (modulo (+ b (* x a)) m))

;;(define/memo (affinedec a b m x)
;(define (affinedec a b m x)
;  ; Store affine decryption parameters to operate on individual numbers
;  (modulo (* (modular-inverse a m) (- x b)) m))

(define (hash-affineenc a b m)
  ; map n => fun(n) sequentially
  (for/hash ([k (in-range m)])
    (values k (affineenc a b m k))))

(define (hash-affinedec a b m)
  ; map fun(n) => n sequentially
  (for/hash ([k (in-range m)])
    (values (affineenc a b m k) k)))


(define (wrap-affineenc m a b)
  ; Store affine enc parameters to operate on individual numbers
  (hash-affineenc a b m))

(define (wrap-affinedec m a b)
  ; Store affine enc parameters to operate on individual numbers
  (hash-affinedec a b m))

(define (wrap-atbashenc m)
  (wrap-affineenc m -1 -1))
(define (wrap-atbashdec m)
  (wrap-affinedec m -1 -1))

(define (wrap-caesarenc m b)
  (wrap-affineenc m 1 b))
(define (wrap-caesardec m b)
  (wrap-affinedec m 1 b))

(define (wrap-rot13enc m)
  (wrap-affineenc m 1 13))
(define (wrap-rot13dec m)
  (wrap-affinedec m 1 13))

(define (wrap-decimationenc m a)
  (wrap-affineenc m a 0))
(define (wrap-decimationdec m a)
  (wrap-affinedec m a 0))

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

(provide wrap-affineenc wrap-affinedec
         wrap-atbashenc wrap-atbashdec
         wrap-caesarenc wrap-caesardec
         wrap-rot13enc wrap-rot13dec
         wrap-decimationenc wrap-decimationdec)
