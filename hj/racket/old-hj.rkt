#lang racket/base

> (for/list ([k (in-naturals)]
             [x (in-range 10)])
    (list k x))
'((0 0) (1 1) (2 2) (3 3) (4 4) (5 5) (6 6) (7 7) (8 8) (9 9))
