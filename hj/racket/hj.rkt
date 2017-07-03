#lang racket/base
(require racket/list)
(require racket/set)
#| (require racket/string) |#

; NOTE: about mechanism
; While a hashmap (a=>d, b=>e, z=>c) makes great sense for monoalphabetic ciphers, it makes less sense for the Caesar-based polyalphabetic ones, which need a key to offset the translation.
; To use the same algorithm, it is suggested to use PT_ALPHA=>number, optional transform (incl. keyword offset), number=>CT_ALPHA; whether to PRE-compute the CT_ALPHA is the question, because the transform could be useful in monoalphabetic but will be less efficient--and it will not work for the keyword cipher in particular, and the affine cipher decryption process is very annoying to implement--although in Racket in particular, it is (interestingly) a one-liner in the math module.
; Perhaps just the keyword CT_ALPHA should be precomputed, and then additional transforms can be built upon it.  This may enable keyed Caesar, or maybe that should be for PT_ALPHA.
; So whether to store a generated ciphertext alphabet depends on how optimized we want to be; and whether we want logic only in the encoding direction, and to reverse much like a hash table.

(define DEFAULT_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
(define ALPHABET DEFAULT_ALPHABET)

; very nice done functions

(define (coprime? . rest-id)
  ;; Are all arguments coprime?
  (= 1 (apply gcd rest-id)))
#| (define (member? v lst [is-equal? equal?]) |#
#|   (ormap (lambda (i) (is-equal? v i)) lst)) |#

; end nice done functions

#| (require srfi/13) |#
#| (member? 3 '(1 2 3)) |#



#| (struct tableau (pt ct)) |#
#| (define xlateify (tableau (lambda (i) (+ 3 i)) 7)) |#
#| ((tableau-pt xlateify) 3) |#







#| (define (lrotate s n) |#
#|   (define ss1 (substring s 0 n)) |#
#|   (define ss2 (substring s n)) |#
#|   (string-append ss2 ss1)) |#
; (for ([i s])
; (printf "~a... ~x" i x))

(define (to-number alphabet)
  ; what is the index of element in lst? otherwise return #f
  (make-immutable-hash
  (for/list ([k (in-naturals)]
             [c (in-string alphabet)])
    (cons c k))))

(define (from-number lst num)
  ; what is the element at position num in lst?
  (list-ref lst num))



(define (make-affine a b m)
  ; Store affine parameters to operate on individual numbers
  (lambda (k)
    (modulo (+ b (* k a)) m)))


;; [TODO] create only numeric mappings for alphabets, then transform with string->num and num->string at the end?
#| (define (strposmap s lst) |#
#|   (map (lambda (i) (string-ref s i)) lst)) |#
#| (strposmap "HELLO, WORLD" '(0 3 2 7 100)) |#

(define (affinal s a b)
  (let ([alphalen (string-length s)])
    (cond
      [(coprime? a alphalen)
       (map
         (lambda (k)
           (string-ref s k))
         (map (make-affine a b alphalen) (range alphalen)))]
       #| (for/list ([k (range alphalen)]) |#
       #|   (string-ref s k) |#
       #|   )] |#
      [else error "multiplier and alphabet length must be coprime"])))

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
#| (define (filterbc mesh kw) |#
     #|   (filter set-member? |# 

#| (filterab "ABCDEFGHIJKLMNOPQRSTUVWXYZ" "MONKEyb2MonkeySeeMonkeyDo") |#

;; [TODO] alphamaker store alphabet string but accept params after...?
#| (define (make-affine-alphabet s) |#
#|   (lambda (a b) |#
#|     (list->string |#
#|       (remove-duplicates |#
#|         (affinal s a b))))) |#
(define (make-affine-alphabet s a b)
  (let ([s (list->string (remove-duplicates (string->list s)))])
    (remove-duplicates
      (affinal s a b))))
(define (make-atbash-alphabet s)
  (make-affine-alphabet s -1 -1))
(define (make-caesar-alphabet s b)
  (make-affine-alphabet s 1 b))
(define (make-rot13-alphabet s)
  (make-caesar-alphabet s 13))
(define (make-decimation-alphabet s a)
  (make-affine-alphabet s a 0))
(define (make-keyword-alphabet ab kw)
  (remove-duplicates
    (string->list
      (string-append (filterab ab kw) ab))))


#| (define my-affine (make-affine 5 8 26)) |#
#| (define (test-encryption s) |#
#|   (let ([alpha (string->list ALPHABET)]) |#
#|     (list->string |#
#|       (for/list ([c (in-string s)]) |#
#|           (from-number alpha |#
#|                        (my-affine |#
#|                          (hash-ref (to-number ALPHABET) c c) |#
#|                          )) c)))) |#

#| (test-encryption "HELLO, WORLD") |#

#| (define (make-encode-table func s rest-id) |#
#|   (make-immutable-hash |#
#|     (map cons s (apply func s rest-id)))) |#
#| (define (make-decode-table func s rest-id) |#
#|   (make-immutable-hash |#
#|     (map cons (apply func s rest-id) s))) |#


#| (define (string-map a b) |#
#|   (make-immutable-hash |#
#|     (map cons (string->list a) (string->list b)))) |#
#| (define (transcrypt-char a b chr t-or-f) |#
#|   (hash-ref (make-immutable-hash (map cons (if (t-or-f) '(b a) '(a b)) chr chr)))) |#

#| (define (transcode s xfunc) |#
#|   ;; take a string and apply xfunc to its characters, filtering out any #f values that result |#
#|   (filter values (map xfunc s))) |#

        #| pos = src.index(e) |#
        #| if callable(transform): |#
        #|     pos = transform(pos) |#
        #| return dst[pos % len(dst)] |#

#| (define (char-transcode c a b [transform ()]) |#
#|   (b substr (modulo |#
#|     (transform |#
#|       (index a c)), len b))) |#

#| (define (counterpart e lst1 lst2) |#
#|   ;; Return the same-index counterpart of an element in one list in another. |#
#|   (list-ref lst2 (index-of lst1 e))) |#

#| (define (counterpart-finder* a b) |#
#|   ;; Return the same-index counterpart of an element in one list in another. |#
#|   (lambda (e [transform (lambda (i) i)]) |#
#|     (list-ref b |#
#|               (transform |#
#|                 (index-of a e))))) |#

#| (define (counterpart-finder a b) |#
#|   (counterpart-finder* (string->list a) (string->list b))) |#

#| (define n (counterpart-finder "ABCDEFG" "HIJKLMN")) |#
#| (n #\C sub1) |#

#| (define transcode-outer |#
#|   (list->string |#
#|     (map transcodeify |#
#|       (string->list s))) |#

#| (define (list-intersect lst someset) |#
#|   (reverse |#
#|     (set-intersect lst someset))) |#

#| (define (restrict-membership lst someset) |#
#|   (let ([valid-elements (set-intersect lst someset)]) |#
#|     (for/list ([e lst] |#
#|                #:when (member e valid-elements)) |#
#|       e))) |#

#| ABCDEFGHIJKLMNOPQRSTUVWXYZ |#
#| MONKEY2 |#
#| MONKEY2ABCDEFGHIJKLMNOPQRSTUVWXYZ |#
#|       ^ |#

#| (list->string (reverse (set-intersect (string->list "MONKeY2qbABCDEFGHIJKLMNOPQRSTUVWXYZ")(string->list "ABCDEFGHIJKLMNOPQRSTUVWXYZ") ))) |#
#| (restrict-membership '(1 2 3 b 4 5 8 9 a b c d e) '( a b 5)) |#

; TODO filter out chars before they even make it here?
;      this way we can use strict elsewhere in a stored lambda?
(define (make-transcoder alphamaker rev)
  (lambda (s #:strict strict #:alphabet [alphabet DEFAULT_ALPHABET] . rest-id)
    (list->string
      (let* ([alpha1 (string->list alphabet)]
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

#| (define (make-encoder alphamaker) |#
#|   (lambda (s #:strict strict #:alphabet [alphabet DEFAULT_ALPHABET] . rest-id) |#
#|     (list->string |#
#|       (let ([s (string->list s)] |#
#|              [alpha1 (string->list alphabet)] |#
#|              [alpha2 (apply alphamaker alphabet rest-id)]) |#
#|         (for/list ([c s] |#
#|           #:when (member c s) |#
#|           (counterpart c alpha1 alpha2)))))) |#
; [TODO] use -affine instead of /affine and append /strict for strict variant??
; [TODO] unreadable symbol for separators?

#| (define (makeit a b) |#
#|   (for/hash ([c1 (in-string a)] |#
#|              [c2 (in-string b)]) |#
#|     (values c1 c2))) |#

#| (makeit "ABCDE" "12345") |#
#| (make-immutable-hash (map cons (string->list "ABCDE") (string->list "12345"))) |#

#| (define (string-index s c) |#
#|   (for/and ([k (in-naturals)] |#
#|         [char (in-string s)] |#
#|         #:break (equal? char c)) |#
#|     k)) |#

#| (string-index "HELLO" #\H) |#
; [TODO] memoize results with promise?

(define string-encrypt/affine
  (make-transcoder make-affine-alphabet #f))
(define string-decrypt/affine
  (make-transcoder make-affine-alphabet #t))

(define string-encrypt/atbash
  (make-transcoder make-atbash-alphabet #f))
(define string-decrypt/atbash
  (make-transcoder make-atbash-alphabet #t))

(define string-encrypt/caesar
  (make-transcoder make-caesar-alphabet #f))
(define string-decrypt/caesar
  (make-transcoder make-caesar-alphabet #t))

(define string-encrypt/rot13
  (make-transcoder make-rot13-alphabet #f))
(define string-decrypt/rot13
  (make-transcoder make-rot13-alphabet #t))

(define string-encrypt/decimation
  (make-transcoder make-decimation-alphabet #f))
(define string-decrypt/decimation
  (make-transcoder make-decimation-alphabet #t))

(define string-encrypt/keyword
  (make-transcoder make-keyword-alphabet #f))
(define string-decrypt/keyword
  (make-transcoder make-keyword-alphabet #t))



#| (define (lrotated s i) |#
#|   (let ([i (modulo i (string-length s))]) |#
#|     (string-append |#
#|       (substring s i) |#
#|       (substring s 0 i)))) |#

#| (define (first-instance s c) |#
#|   (for/last ([char s] |#
#|              #:when (not(equal? char c))) |#
#|             char) |#
#|   ) |#

; GENERAL FLOW:
; CREATE ALPHABET HASH:
;   ALPHA-to-NUM mapping
;   encode using lambda indicating what to do per index
;     this saves us from having to use the fn to create a different string
;   NUM-to-ALPHA mapping for CT alphabet
;   CREATE HASH PT2CT and CT2PT
; NOW apply PT2CT and CT2PT for bidirectional awesomeness
; this is necessary over using math _during_ the translation to avoid needing to do advanced math with, for instance, the affine cipher, whose decryption step is horrible; and also lets us monkey-patch in things like the keyword cipher, where math is less relevant


#| (define (xlate s a b) |#
#|   (list->string (for/list ([c (in-string s)]) |#
#|     (define npos (string-index a c)) |#
#|     (string-ref b npos) |#
#|     )) |#
#|   ) |#

; could be variadic...
#| (define (zip xs) |#
#|   (apply map list xs)) |#

#| (define (zip p q) |#
#|   (map cons p q)) |#
#| (define (hmap p q) |#
#|   (make-immutable-hash |#
#|     (map cons p q))) |#

#| (define (xtable p q) |#
#|   (hmap (string->list p) |#
#|         (string->list q))) |#

#| (define (xlate2 somextable strict s) |#
#|   (list->string |#
#|     (map |#
#|       (lambda(i) |#
#|         (cond |#
#|           [(equal? strict #f) (hash-ref somextable i i)] |#
#|           [(hash-has-key? somextable i) (hash-ref somextable i i)] |#
#|           [else (hash-ref somextable i #"")] |#
#|           ) |#
#|         ) (string->list s)))) |#

#| (define (index s char) |#
#|   (for/first ([c s] |#
#|               [i (in-naturals)] |#
#|               #:when (char=? c char)) |#
#|              i)) |#
#| (define (xxx lammie c) |#
#|   #1| (define idx (index ALPHABET c)) |1# |#
#|   (define idx (hash-ref FROM_ALPHA_MAPPING c #f)) |#
#|   (cond |#
#|     [idx (string-ref ALPHABET |#
#|                      (modulo (lammie idx) |#
#|                              (string-length ALPHABET)))] |#
#|     [else c])) |#



#| (define (make_caesar_alphabet n) |#
#|   (lrotated ALPHABET n)) |#
#| (define (xform_atbash) |#
#|   (lambda (n) |#
#|     (- (length ALPHABET) n))) |#

#| (define CAESAR_ALPHABET (make_caesar_alphabet 3)) |#
#| (printf "PT: ~a\nCT: ~a\n" ALPHABET CAESAR_ALPHABET) |#

#| (define encxtable (xtable ALPHABET CAESAR_ALPHABET)) |#
#| (define decxtable (xtable CAESAR_ALPHABET ALPHABET)) |#

#| (display (xlate s ALPHABET CAESAR_ALPHABET)) |#

#|   (list->string (for/list ([c (in-string s)]) |#
#| (define DST (string-ref CAESAR_ALPHABET npos)) |#

#| (list->string (xlate2 encxtable #t "HELLO, WORLD!")) |#
#| (list->string (xlate2 encxtable #f "HELLO, WORLD!")) |#
#| (struct cipher-suite |#
#|                         (encrypt/affine decrypt/affine |#
#|                          encrypt/atbash decrypt/atbash |#
#|                          encrypt/caesar decrypt/caesar |#
#|                          encrypt/decimation decrypt/decimation |#
#|                          encrypt/keyword decrypt/keyword)) |#

#| (define cipher (cipher-suite string-encrypt/affine string-decrypt/affine |#
#|          string-encrypt/atbash string-decrypt/atbash |#
#|          string-encrypt/caesar string-decrypt/caesar |#
#|          string-encrypt/decimation string-decrypt/decimation |#
#|          string-encrypt/keyword string-decrypt/keyword)) |#

#| (provide cipher) |#

#| (struct cipher (encrypt decrypt)) |#
#| (define my-affine-encrypt (lambda() "WE ARE ENCRYPTING")) |#
#| (define my-affine-decrypt (lambda() "WE ARE DECRYPTING")) |#
#| (define affine (cipher my-affine-encrypt my-affine-decrypt)) |#
#| (affine-encrypt) |#

(provide string-encrypt/affine string-decrypt/affine
         string-encrypt/atbash string-decrypt/atbash
         string-encrypt/caesar string-decrypt/caesar
         string-encrypt/rot13 string-decrypt/rot13
         string-encrypt/decimation string-decrypt/decimation
         string-encrypt/keyword string-decrypt/keyword)
