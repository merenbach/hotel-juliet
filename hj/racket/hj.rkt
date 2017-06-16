#lang racket/base
(require racket/list)
(require racket/string)
#| (require srfi/13) |#
(define DEFAULT_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
(define ALPHABET DEFAULT_ALPHABET)

(define (make-alphabet s)
  (list->string
    (remove-duplicates
      (string->list s))))


(define qrx
  (lambda (a b c #:alphabet [alphabet DEFAULT_ALPHABET])
    (list a b c alphabet)))
(qrx 2 3 4)

#| (define (lrotate s n) |#
#|   (define ss1 (substring s 0 n)) |#
#|   (define ss2 (substring s n)) |#
#|   (string-append ss2 ss1)) |#
; (for ([i s])
; (printf "~a... ~x" i x))

#| (define (affinal s a b) |#
#|     (for/list ([c (in-string s)] |#
#|       (c)) |#
#|       )) |#
#| (define (affinal s a b) |#
#|   (list->string |#
#|     (for/list |#
#|       ([c (in-string s)]) |#
#|       (or c c)))) |#

(define (coprime a b)
  (equal? 1 (gcd a b)))

(define (affine n a b)
  (cond
    [(coprime a (string-length ALPHABET))
      (modulo
        (+ b (* n a))
        (string-length ALPHABET))]
      [else error "A MUST BE COPRIME WITH ALPHABET"]))

(define (affinal s a b)
  (list->string
    (for/list ([k (in-naturals)]
               [c (in-string s)])
      (string-ref s (affine k a b)))))

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

#| (define (make-alphabet a b) |#
#|   (xpair a b)) |#

(define (make-affine-alphabet s a b)
  (make-alphabet
    (affinal s a b)))
(define (make-atbash-alphabet s)
  (make-affine-alphabet s -1 -1))
(define (make-caesar-alphabet s b)
  (make-affine-alphabet s 1 b))
(define (make-decimation-alphabet s a)
  (make-affine-alphabet s a 0))
(define (make-keyword-alphabet ab kw)
  (make-alphabet
    (string-append (filterab ab kw) ab)))


#| (define (string-map a b) |#
#|   (make-immutable-hash |#
#|     (map cons (string->list a) (string->list b)))) |#
#| (define (transcrypt-char a b chr t-or-f) |#
#|   (hash-ref (make-immutable-hash (map cons (if (t-or-f) '(b a) '(a b)) chr chr)))) |#

(define (MAKE_TRANSCRYPT_FUNC what-tc-func-to-call what-alpha-to-call strict s alphabet . my-rest-id)
  (define alpha1 (string->list alphabet))
  (define alpha2 (string->list (apply what-alpha-to-call alphabet my-rest-id)))
    (for/list
      ([c (in-string s)]
       #:when (or (not strict) (hash-has-key? FROM_ALPHA_MAPPING c)))
      (what-tc-func-to-call c alpha1 alpha2)))

(define (make-transcoder alphamaker transfunc)
  (lambda (s #:strict strict #:alphabet [alphabet DEFAULT_ALPHABET] . rest-id)
    (list->string
      (apply MAKE_TRANSCRYPT_FUNC transfunc alphamaker strict s alphabet rest-id))))

(define (encrypt-char chr a b)
  (hash-ref (make-immutable-hash (map cons a b)) chr chr))
(define (decrypt-char chr a b)
  (hash-ref (make-immutable-hash (map cons b a)) chr chr))


#| (define (generic-make-tc s #:strict strict #:alphabet [alphabet DEFAULT_ALPHABET] . my-rest-id) |#
#|   (apply MAKE_TRANSCRYPT_FUNC encrypt-char make-affine-alphabet strict s alphabet my-rest-id)) |#

(define string-encrypt-affine
  (make-transcoder make-affine-alphabet encrypt-char))
(define string-decrypt-affine
  (make-transcoder make-affine-alphabet decrypt-char))

(define string-encrypt-atbash
  (make-transcoder make-atbash-alphabet encrypt-char))
(define string-decrypt-atbash
  (make-transcoder make-atbash-alphabet decrypt-char))

(define string-encrypt-caesar
  (make-transcoder make-caesar-alphabet encrypt-char))
(define string-decrypt-caesar
  (make-transcoder make-caesar-alphabet decrypt-char))

(define string-encrypt-decimation
  (make-transcoder make-decimation-alphabet encrypt-char))
(define string-decrypt-decimation
  (make-transcoder make-decimation-alphabet decrypt-char))

(define string-encrypt-keyword
  (make-transcoder make-keyword-alphabet encrypt-char))
(define string-decrypt-keyword
  (make-transcoder make-keyword-alphabet decrypt-char))


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
(define (char-index iterable)
    (for/list ([k (in-naturals)]
               [x iterable])
      (cons x k)))


(define FROM_ALPHA_MAPPING
  (make-immutable-hash
    (char-index ALPHABET)))


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
(define (hmap p q)
  (make-immutable-hash
    (map cons p q)))

(define (xtable p q)
  (hmap (string->list p)
        (string->list q)))

(define (xlate2 somextable strict s)
  (list->string
    (map
      (lambda(i)
        (cond
          [(equal? strict #f) (hash-ref somextable i i)]
          [(hash-has-key? somextable i) (hash-ref somextable i i)]
          [else (hash-ref somextable i #"")]
          )
        ) (string->list s))))

(define (index s char)
  (for/first ([c s]
              [i (in-naturals)]
              #:when (char=? c char))
             i))
(define (xxx lammie c)
  #| (define idx (index ALPHABET c)) |#
  (define idx (hash-ref FROM_ALPHA_MAPPING c #f))
  (cond
    [idx (string-ref ALPHABET
                     (modulo (lammie idx)
                             (string-length ALPHABET)))]
    [else c]))



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

(provide string-encrypt-affine string-decrypt-affine)
(provide string-encrypt-atbash string-decrypt-atbash)
(provide string-encrypt-caesar string-decrypt-caesar)
(provide string-encrypt-decimation string-decrypt-decimation)
(provide string-encrypt-keyword string-decrypt-keyword)
