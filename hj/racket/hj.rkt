#lang racket/base
(require racket/list)
#| (require racket/string) |#


(define DEFAULT_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
(define ALPHABET DEFAULT_ALPHABET)


(define (coprime . rest-id)
  ;; Are all arguments coprime?
  (equal? 1 (apply gcd rest-id)))


#| (require srfi/13) |#



#| (struct tableau (pt ct)) |#
#| (define xlateify (tableau (lambda (i) (+ 3 i)) 7)) |#
#| ((tableau-pt xlateify) 3) |#







#| (define (lrotate s n) |#
#|   (define ss1 (substring s 0 n)) |#
#|   (define ss2 (substring s n)) |#
#|   (string-append ss2 ss1)) |#
; (for ([i s])
; (printf "~a... ~x" i x))


(define (affinity a b m)
  (lambda (k)
    (modulo (+ b (* k a)) m)))


;; [TODO] create only numeric mappings for alphabets, then transform with string->num and num->string at the end?
#| (define (strposmap s lst) |#
#|   (map (lambda (i) (string-ref s i)) lst)) |#
#| (strposmap "HELLO, WORLD" '(0 3 2 7 100)) |#

(define (affinal s a b)
  (let ([alphalen (string-length s)])
    (cond
      [(coprime a alphalen)
       (map
         (lambda (k)
           (string-ref s k))
         (map (affinity a b alphalen) (range alphalen)))]
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
    (for/list ([c (in-string kw)]
      #:when (member c mesh))
      c)))

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
(define (make-decimation-alphabet s a)
  (make-affine-alphabet s a 0))
(define (make-keyword-alphabet ab kw)
  (remove-duplicates
    (string-append (filterab ab kw) ab)))


#| (define (string-map a b) |#
#|   (make-immutable-hash |#
#|     (map cons (string->list a) (string->list b)))) |#
#| (define (transcrypt-char a b chr t-or-f) |#
#|   (hash-ref (make-immutable-hash (map cons (if (t-or-f) '(b a) '(a b)) chr chr)))) |#

(define (transcode s xfunc)
  ;; take a string and apply xfunc to its characters, filtering out any #f values that result
  (filter values (map xfunc s)))

        #| pos = src.index(e) |#
        #| if callable(transform): |#
        #|     pos = transform(pos) |#
        #| return dst[pos % len(dst)] |#

#| (define (char-transcode c a b [transform ()]) |#
#|   (b substr (modulo |#
#|     (transform |#
#|       (index a c)), len b))) |#

(define (counterpart-finder* a b)
  ;; Return the same-index counterpart of an element in one list in another.
  (lambda (e [transform (lambda (i) i)])
    (list-ref b
              (transform
                (index-of a e)))))

(define (counterpart-finder a b)
  (counterpart-finder* (string->list a) (string->list b)))

#| (define n (counterpart-finder "ABCDEFG" "HIJKLMN")) |#
#| (n #\C sub1) |#

#| (define transcode-outer |#
#|   (list->string |#
#|     (map transcodeify |#
#|       (string->list s))) |#

(define (make-transcoder alphamaker rev)
  (lambda (s #:strict strict #:alphabet [alphabet DEFAULT_ALPHABET] . rest-id)
    (list->string
      (let* ([s (string->list s)]
             [alpha1 (string->list alphabet)]
             [alpha2 (apply alphamaker alphabet rest-id)]
             [forwards-assoc (map cons alpha1 alpha2)]
             [reverse-assoc (map cons alpha2 alpha1)]
             [current-map (make-immutable-hash (if rev reverse-assoc forwards-assoc))]
             [xfunc (lambda(char) (hash-ref current-map char (if (not strict) char #f)))])
        (transcode s xfunc)))))
; [TODO] use -affine instead of /affine and append /strict for strict variant??
; [TODO] unreadable symbol for separators?

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

(define string-encrypt/decimation
  (make-transcoder make-decimation-alphabet #f))
(define string-decrypt/decimation
  (make-transcoder make-decimation-alphabet #t))

(define string-encrypt/keyword
  (make-transcoder make-keyword-alphabet #f))
(define string-decrypt/keyword
  (make-transcoder make-keyword-alphabet #t))


#| (struct bigbadmofo (alphabet) |#
#|   (bingbangboom ( |#
#|   (define x 3) |#
#|    (define y 7) |#
#|    (+ x y)))) |#

#| (define ATBASH_ALPHABET |#
#|   (make-atbash ALPHABET)) |#

#| (define ATPAIR |#
#|   (xpair ALPHABET ATBASH_ALPHABET)) |#


#| (define enumerate |#
#|   (lambda (iterable [rev #f]) |#
#|     (for/list ([k (in-naturals)] |#
#|                [x iterable]) |#
#|       (cond |#
#|         [rev (cons x k)] |#
#|         [else (cons k x)])))) |#
#| (define (enumerate iterable) |#
#|     (for/list ([k (in-naturals)] |#
#|                [x iterable]) |#
#|       (cons k x))) |#
#| (define (char-index iterable) |#
#|     (for/list ([k (in-naturals)] |#
#|                [x iterable]) |#
#|       (cons x k))) |#


#| (define FROM_ALPHA_MAPPING |#
#|   (make-immutable-hash |#
#|     (char-index ALPHABET))) |#


#| (define (xform s mm) |#
#|   (map (lambda (c) |#
#|          (or c c) |#
#|          ) |#
#|   (string->list s))) |#

#| (define AFF (affinal ALPHABET 5 8)) |#
#| (printf "AFF: ~a\n\n\n" AFF) |#

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

#| (define (xlate2 somextable strict s) |#
#|   (map (lambda (i) |#
#|          (hash-ref somextable i i)) |#
#|        (string->list s))) |#

#| (map (lambda (i) |#
#| (map list a b)) |#
#| (define (zip xs) (apply map list xs)) |#

#| (define zip2 |#
#|   (lambda xs |#
#|     (display xs))) |#
#| (define (xtable s a b) |#
#|   (zip (string->list a) (string->list b))) |#

#| (define z (xtable s ALPHABET CAESAR_ALPHABET)) |#
#| (printf "~a\n" (#hash(z))) |#
#| (define p1 '(1 2 3 4 12)) |#
#| (define p2 '(6 7 8 9 10)) |#
#| (define p3 '(11 12 13 14 15)) |#
#| (define assns (xtable s ALPHABET CAESAR_ALPHABET)) |#
#| (display assns) |#
#| (cdr (assoc 6 ngoo)) |#

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
         string-encrypt/decimation string-decrypt/decimation
         string-encrypt/keyword string-decrypt/keyword)
