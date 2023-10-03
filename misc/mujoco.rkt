#lang racket/base
(require ffi/unsafe
         ffi/unsafe/define)
 
(define-ffi-definer define-mujoco (ffi-lib "F:\\local\\mujoco-2.3.6-windows-x86_64\\bin\\mujoco"))

(define _mjModel-pointer (_cpointer 'mjModel))

(define-mujoco mj_stateSize (_fun _mjModel-pointer -> _uint))
