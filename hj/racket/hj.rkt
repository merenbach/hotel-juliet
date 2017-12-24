#lang racket/base

(require "util.rkt")
(require racket/list)
(require racket/set)
(require racket/generator)
;(require memoize)
#| (require racket/string) |#


; TODO: improve duplicate removal and strict filtering to minimize duplicate tests

; NOTE: about mechanism
; While a hashmap (a=>d, b=>e, z=>c) makes great sense for monoalphabetic ciphers, it makes less sense for the Caesar-based polyalphabetic ones, which need a key to offset the translation.
; To use the same algorithm, it is suggested to use PT_ALPHA=>number, optional transform (incl. keyword offset), number=>CT_ALPHA; whether to PRE-compute the CT_ALPHA is the question, because the transform could be useful in monoalphabetic but will be less efficient--and it will not work for the keyword cipher in particular, and the affine cipher decryption process is very annoying to implement--although in Racket in particular, it is (interestingly) a one-liner in the math module.
; Perhaps just the keyword CT_ALPHA should be precomputed, and then additional transforms can be built upon it.  This may enable keyed Caesar, or maybe that should be for PT_ALPHA.
; So whether to store a generated ciphertext alphabet depends on how optimized we want to be; and whether we want logic only in the encoding direction, and to reverse much like a hash table.

(define DEFAULT_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
(define ALPHABET DEFAULT_ALPHABET)

; very nice done functions
; [TODO] break out into utils
; end from stackoverflow

(define (new-make-xtable a b)
  ; Turn two lists into a hash
  (make-immutable-hash (map cons a b)))

(define (xtable-to lst)
  ; Convert from natural integers to lst
  (new-make-xtable (in-naturals) (in-range 26)))


(define (idx2fun fun limit)
  ; map n => fun(n) sequentially
  (for/hash ([n (in-range limit)])
    (values n (fun n))))

(define (fun2idx fun limit)
  ; map fun(n) => n sequentially
  (for/hash ([n (in-range limit)])
    (values (fun n) n)))

;(define abc (wrap-caesarenc 26 3))
;(define xyz (idx2fun abc 26))
;(println xyz)

;(define x (new-make-xtable '(2 3 4 5 6) '(8 9 10 11 12)))
;(println (hash-ref x 7 3))



;;; memoize affine output because we can
;; (define (lcg modulus a c seed)
;;   ;; a = multiplier, c = increment, m = modulus, seed is initial term (seed or start value)
;;   (generator ()
;;              (let loop ([seed seed])
;;                (yield seed)
;;                (loop (modulo (+ c (* seed a)) modulus)))))

#| (define (member? v lst [is-equal? equal?]) |#
#|   (ormap (lambda (i) (is-equal? v i)) lst)) |#

; end nice done functions

; closures
; end closures

;(map r '(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27))

#| (require srfi/13) |#
#| (member? 3 '(1 2 3)) |#


;; [TODO] create only numeric mappings for alphabets, then transform with string->num and num->string at the end?
#| (define (strposmap s lst) |#
#|   (map (lambda (i) (string-ref s i)) lst)) |#
#| (strposmap "HELLO, WORLD" '(0 3 2 7 100)) |#

#| (define (filterab2 mesh kw) |#
#|   (filter (lambda (c) (member c mesh)) kw)) |#

#| (define (xpair a b) |# 
#|   (let ([a (string->list a)] |#
#|         [b (string->list b)]) |#
#|     (cons (make-immutable-hash (map cons a b)) |#
#|           (make-immutable-hash (map cons b a))))) |#

(define (filterab mesh kw)
  (list->string
    (let ([mesh (string->list mesh)])
      (for/list ([c (in-string kw)]
                 #:when (set-member? mesh c))
        c))))

(define (make-keyword-alphabet ab kw)
  (remove-duplicates
   (string->list
    (string-append (filterab ab kw) ab))))

;; (define x (make-keyword-alphabet DEFAULT_ALPHABET "MONKEY"))
;; (define (make-keyword-nums s alphabet)
;;   (let ([alphabet (string->list alphabet)])
;;     (for/list ([char s]
;;                #:when (member char alphabet))
;;       (index-of alphabet char))))
;; (make-keyword-nums (make-keyword-alphabet DEFAULT_ALPHABET "MONKEY") DEFAULT_ALPHABET)
;; (define (wrap-keywordenc lst)
;;   (lambda (k)
;;     (list-ref lst k)))
#| (define (list-intersect lst someset) |#
#|   (reverse |#
#|     (set-intersect lst someset))) |#

#| (define (restrict-membership lst someset) |#
#|   (let ([valid-elements (set-intersect lst someset)]) |#
#|     (for/list ([e lst] |#
#|                #:when (member e valid-elements)) |#
#|       e))) |#

#| (restrict-membership '(1 2 3 b 4 5 8 9 a b c d e) '( a b 5)) |#

; TODO filter out chars before they even make it here?
;      this way we can use strict elsewhere in a stored lambda?
(define (old-make-transcoder alphamaker rev)
  (lambda (s #:strict strict #:alphabet [alphabet DEFAULT_ALPHABET] . rest-id)
    (list->string
      (let* ([alpha1 (remove-duplicates (string->list alphabet))]
             [alpha2 (apply alphamaker alphabet rest-id)]
             [source-alpha (if rev alpha2 alpha1)]
             [target-alpha (if rev alpha1 alpha2)]
             [current-map (make-immutable-hash (map cons source-alpha target-alpha))]
             )
        (filter values
          (for/list ([char (in-string s)]
            #:when (or (not strict) (hash-has-key? current-map char)))
            (hash-ref current-map char char)))))))
        #| (for/list ([char s] |#
        #|            #:when (or (not strict) (hash-has-key? current-map char))) |#
        #|            #1| #:when (or (not strict) (set-member? source-alpha char))) |1# |#
        #|   (hash-ref current-map char char)) |#

(define (make-affine-transcoder isrev alphamaker)
  (lambda (s #:strict strict #:alphabet [alphabet DEFAULT_ALPHABET] . rest-id)
    (list->string
     (let ([alphabet (string->list alphabet)]
           [forward (idx2fun (apply alphamaker (string-length alphabet) rest-id) (string-length alphabet))]
           [backward (fun2idx (apply alphamaker (string-length alphabet) rest-id) (string-length alphabet))]
           ;[xtable (apply alphamaker (string-length alphabet) rest-id)]
           )
       (for/list ([char (in-string s)]
                  #:when (or (not strict) (member char alphabet)))
         (if (member char alphabet)
             (list-ref alphabet
                       (hash-ref
                        (if isrev backward forward)
                        (index-of alphabet char)))
             char))))))

(define (make-vigenere-transcoder alphamaker)
  (lambda (s keystr #:strict strict #:alphabet [alphabet DEFAULT_ALPHABET])
    (list->string
     (let ([alphabet (string->list alphabet)]
           [transcoder (alphamaker (string-length alphabet))])
       (for/list ([char (in-string s)]
                  [kchar (in-string keystr)]
                  #:when (or (not strict) (member char alphabet)))
         (if (member char alphabet)
             (list-ref alphabet
                         (transcoder (index-of alphabet char) (index-of alphabet kchar)))
             char))))))

;        (filter values
;          (for/list ([char (in-string s)]
;                     #:when (or (not strict) (hash-has-key? current-map char)))
;            (hash-ref current-map char char)))))))

(define string-encrypt/affine
  (make-affine-transcoder #f wrap-affineenc))
(define string-decrypt/affine
  (make-affine-transcoder #t wrap-affineenc))

(define string-encrypt/atbash
  (make-affine-transcoder #f wrap-atbashenc))
(define string-decrypt/atbash
  (make-affine-transcoder #t wrap-atbashenc))

(define string-encrypt/caesar
  (make-affine-transcoder #f wrap-caesarenc))
(define string-decrypt/caesar
  (make-affine-transcoder #t wrap-caesarenc))

(define string-encrypt/rot13
  (make-affine-transcoder #f wrap-rot13enc))
(define string-decrypt/rot13
  (make-affine-transcoder #t wrap-rot13enc))

(define string-encrypt/decimation
  (make-affine-transcoder #f wrap-decimationenc))
(define string-decrypt/decimation
  (make-affine-transcoder #t wrap-decimationenc))

(define string-encrypt/keyword
  (old-make-transcoder make-keyword-alphabet #f))
  ;(make-transcoder wrap-keywordenc))
(define string-decrypt/keyword
  (old-make-transcoder make-keyword-alphabet #t))
  ;(make-transcoder wrap-keyworddec))

(define string-encrypt/vigenere
  (make-vigenere-transcoder wrap-tabularectaenc))
(define string-decrypt/vigenere
  (make-vigenere-transcoder wrap-tabularectadec))

;; (define string-encrypt/beaufort
;;   (make-transcoder wrap-tabularectaenc))
;; (define string-decrypt/beaufort
;;   (make-transcoder wrap-tabularectadec))
;; (define string-encrypt/variantbeaufort
;;   (make-transcoder wrap-tabularectaenc))
;; (define string-decrypt/variantbeaufort
;;   (make-transcoder wrap-tabularectadec))
;; (define string-encrypt/gronsfeld
;;   (make-transcoder wrap-tabularectaenc))
;; (define string-decrypt/gronsfeld
;;   (make-transcoder wrap-tabularectadec))
;; (define string-encrypt/trithemius
;;   (make-transcoder wrap-tabularectaenc))
;; (define string-decrypt/trithemius
;;   (make-transcoder wrap-tabularectadec))
;; (define string-encrypt/porta
;;   (make-transcoder wrap-tabularectaenc))
;; (define string-decrypt/porta
;;   (make-transcoder wrap-tabularectadec))

(provide string-encrypt/affine string-decrypt/affine
         string-encrypt/atbash string-decrypt/atbash
         string-encrypt/caesar string-decrypt/caesar
         string-encrypt/rot13 string-decrypt/rot13
         string-encrypt/decimation string-decrypt/decimation
         string-encrypt/keyword string-decrypt/keyword
         string-encrypt/vigenere string-decrypt/vigenere)

