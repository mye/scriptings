#lang pollen/mode racket/base
(require
	"pollen-rkt.scrbl"
	pollen/tag)



(provide (all-from-out "pollen-rkt.scrbl"))

(module setup racket/base
  (provide (all-defined-out)) ;; <- don't forget this line in your config submodule!
  (require pollen/setup racket/path)
  (define (omitted-path? p) (path-has-extension? p #".sh")))
