#lang racket/base
(require racket/list)
(require racket/string)
#| (require srfi/13) |#
(define ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
(define (make-alphabet s)
  (list->string
    (remove-duplicates
      (string->list s))))


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

(define (xpair a b)
  (let ([a (string->list a)]
        [b (string->list b)])
    (cons (make-immutable-hash (map cons a b))
          (make-immutable-hash (map cons b a)))))

#| (define (filterab2 mesh kw) |#
#|   (filter (lambda (c) (member c mesh)) kw)) |#

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


#| (define ATBASH_ALPHABET |#
#|   (make-atbash ALPHABET)) |#

#| (define ATPAIR |#
#|   (xpair ALPHABET ATBASH_ALPHABET)) |#

(define (encrypt-char xtb chr)
  (hash-ref (car xtb) chr chr))
(define (decrypt-char xtb chr)
  (hash-ref (cdr xtb) chr chr))

(define (encrypt-string xtb strict s)
  (xlate encrypt-char xtb strict s))
(define (decrypt-string xtb strict s)
  (xlate decrypt-char xtb strict s))


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

(define (xlate nfunc xtb strict s)
  (list->string
    (for/list
      ([c (in-string s)]
       #:when (or (not strict) (hash-has-key? FROM_ALPHA_MAPPING c)))
      (nfunc xtb c))))



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

(provide ALPHABET encrypt-string decrypt-string make-affine-alphabet xpair xlate)
