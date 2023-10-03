#lang racket/base


(require ffi/unsafe
         ffi/unsafe/define)

(define llama (ffi-lib "F:\\local\\llama.cpp\\build\\bin\\Release\\llama"))
(define-ffi-definer define-llama llama)


;GGML_USE_CUBLAS = hasattr(_lib, "ggml_init_cublas")

;(define-llamacpp ggml_init_cublas)

(define GGML_USE_CUBLAS (get-ffi-obj 'ggml_init_cublas llama (_fun -> _void) (λ () #f)))

(define-llama ggml_init_cublas (_fun -> _void))
(define GGML_CUDA_MAX_DEVICES 16)

(define LLAMA_MAX_DEVICES
  (if GGML_USE_CUBLAS
      GGML_CUDA_MAX_DEVICES
      1))

;# #define LLAMA_FILE_MAGIC_GGJT        0x67676a74u // 'ggjt'
;LLAMA_FILE_MAGIC_GGJT = ctypes.c_uint(0x67676A74)
;# #define LLAMA_FILE_MAGIC_GGLA        0x67676c61u // 'ggla'
;LLAMA_FILE_MAGIC_GGLA = ctypes.c_uint(0x67676C61)
;# #define LLAMA_FILE_MAGIC_GGMF        0x67676d66u // 'ggmf'
;LLAMA_FILE_MAGIC_GGMF = ctypes.c_uint(0x67676D66)
;# #define LLAMA_FILE_MAGIC_GGML        0x67676d6cu // 'ggml'
;LLAMA_FILE_MAGIC_GGML = ctypes.c_uint(0x67676D6C)
;# #define LLAMA_FILE_MAGIC_GGSN        0x6767736eu // 'ggsn'
;LLAMA_FILE_MAGIC_GGSN = ctypes.c_uint(0x6767736E)
;
;# #define LLAMA_FILE_VERSION           3
;LLAMA_FILE_VERSION = c_int(3)
;LLAMA_FILE_MAGIC = LLAMA_FILE_MAGIC_GGJT
;LLAMA_FILE_MAGIC_UNVERSIONED = LLAMA_FILE_MAGIC_GGML
;LLAMA_SESSION_MAGIC = LLAMA_FILE_MAGIC_GGSN
;LLAMA_SESSION_VERSION = c_int(1)
;
;# #define LLAMA_DEFAULT_SEED           0xFFFFFFFF
;LLAMA_DEFAULT_SEED = c_int(0xFFFFFFFF)


(define _llama_model-pointer (_cpointer '_llama_model))
(define _llama_context-pointer (_cpointer 'llama_context))

;; typedef int llama_token;
(define _llama_token _int)
(define _llama_token-pointer (_cpointer '_llama_token))


;; typedef struct llama_token_data {
;;     llama_token id; // token id
;;     float logit;    // log-odds of the token
;;     float p;        // probability of the token
;; } llama_token_data;

(define-cstruct _llama_token_data ([id _llama_token]
                                   [logit _float]
                                   [p _float]))

;(define _llama_token_data-pointer (_cpointer '_llama_token_data))

;;# typedef struct llama_token_data_array {
;;#     llama_token_data * data;
;;#     size_t size;
;;#     bool sorted;
;;# } llama_token_data_array;

(define-cstruct _llama_token_data_array ([data _llama_token_data-pointer]
                                         [size _size]
                                         [sorted _bool]))

;; typedef void (*llama_progress_callback)(float progress, void *ctx);
;; (function-ptr ... ?)
(define _llama_progress_callback (_fun _float _void -> _void))


;;# struct llama_context_params {
;;#     uint32_t seed;                         // RNG seed, -1 for random
;;#     int32_t  n_ctx;                        // text context
;;#     int32_t  n_batch;                      // prompt processing batch size
;;#     int32_t  n_gpu_layers;                 // number of layers to store in VRAM
;;#     int32_t  main_gpu;                     // the GPU that is used for scratch and small tensors
;;#     float tensor_split[LLAMA_MAX_DEVICES]; // how to split layers across multiple GPUs
;;#     // called with a progress value between 0 and 1, pass NULL to disable
;;#     llama_progress_callback progress_callback;
;;#     // context pointer passed to the progress callback
;;#     void * progress_callback_user_data;
;;
;;
;;#     // Keep the booleans together to avoid misalignment during copy-by-value.
;;#     bool low_vram;   // if true, reduce VRAM usage at the cost of performance
;;#     bool f16_kv;     // use fp16 for KV cache
;;#     bool logits_all; // the llama_eval() call computes all logits, not just the last one
;;#     bool vocab_only; // only load the vocabulary, no weights
;;#     bool use_mmap;   // use mmap if possible
;;#     bool use_mlock;  // force system to keep model in RAM
;;#     bool embedding;  // embedding mode only
;;# };

(define-cstruct _llama_context_params ([seed _uint32]
                                       [n_ctx _int32]
                                       [n_batch _int32]
                                       [n_gpu_layers _int32]
                                       [main_gpu _int32]
                                       [tensor_split (_array _float LLAMA_MAX_DEVICES)]
                                       [progress_callback _llama_progress_callback]
                                       [progress_callback_user_data _void]
                                       [low_vram _bool]
                                       [f16_kv _bool]
                                       [logits_all _bool]
                                       [vocab_only _bool]
                                       [use_mmap _bool]
                                       [use_mlock _bool]
                                       [embedding _bool]))


;;# enum llama_ftype {
;;#     LLAMA_FTYPE_ALL_F32              = 0,
;;#     LLAMA_FTYPE_MOSTLY_F16           = 1, // except 1d tensors
;;#     LLAMA_FTYPE_MOSTLY_Q4_0          = 2, // except 1d tensors
;;#     LLAMA_FTYPE_MOSTLY_Q4_1          = 3, // except 1d tensors
;;#     LLAMA_FTYPE_MOSTLY_Q4_1_SOME_F16 = 4, // tok_embeddings.weight and output.weight are F16
;;#     // LLAMA_FTYPE_MOSTLY_Q4_2       = 5, // support has been removed
;;#     // LLAMA_FTYPE_MOSTLY_Q4_3       = 6, // support has been removed
;;#     LLAMA_FTYPE_MOSTLY_Q8_0          = 7, // except 1d tensors
;;#     LLAMA_FTYPE_MOSTLY_Q5_0          = 8, // except 1d tensors
;;#     LLAMA_FTYPE_MOSTLY_Q5_1          = 9, // except 1d tensors
;;#     LLAMA_FTYPE_MOSTLY_Q2_K          = 10,// except 1d tensors
;;#     LLAMA_FTYPE_MOSTLY_Q3_K_S        = 11,// except 1d tensors
;;#     LLAMA_FTYPE_MOSTLY_Q3_K_M        = 12,// except 1d tensors
;;#     LLAMA_FTYPE_MOSTLY_Q3_K_L        = 13,// except 1d tensors
;;#     LLAMA_FTYPE_MOSTLY_Q4_K_S        = 14,// except 1d tensors
;;#     LLAMA_FTYPE_MOSTLY_Q4_K_M        = 15,// except 1d tensors
;;#     LLAMA_FTYPE_MOSTLY_Q5_K_S        = 16,// except 1d tensors
;;#     LLAMA_FTYPE_MOSTLY_Q5_K_M        = 17,// except 1d tensors
;;#     LLAMA_FTYPE_MOSTLY_Q6_K          = 18,// except 1d tensors
;;# };

(define _llama_ftype
  (_enum '(LLAMA_FTYPE_ALL_F32
           LLAMA_FTYPE_MOSTLY_F16
           LLAMA_FTYPE_MOSTLY_Q4_0
           LLAMA_FTYPE_MOSTLY_Q4_1
           LLAMA_FTYPE_MOSTLY_Q4_1_SOME_F16
           LLAMA_FTYPE_MOSTLY_Q8_0 = 7
           LLAMA_FTYPE_MOSTLY_Q5_0    
           LLAMA_FTYPE_MOSTLY_Q5_1       
           LLAMA_FTYPE_MOSTLY_Q2_K       
           LLAMA_FTYPE_MOSTLY_Q3_K_S   
           LLAMA_FTYPE_MOSTLY_Q3_K_M   
           LLAMA_FTYPE_MOSTLY_Q3_K_L     
           LLAMA_FTYPE_MOSTLY_Q4_K_S  
           LLAMA_FTYPE_MOSTLY_Q4_K_M    
           LLAMA_FTYPE_MOSTLY_Q5_K_S      
           LLAMA_FTYPE_MOSTLY_Q5_K_M   
           LLAMA_FTYPE_MOSTLY_Q6_K)))
   


;;# // model quantization parameters
;;# typedef struct llama_model_quantize_params {
;;#     int nthread;                 // number of threads to use for quantizing, if <=0 will use std::thread::hardware_concurrency()
;;#     enum llama_ftype   ftype;    // quantize to this llama_ftype
;;#     bool allow_requantize;       // allow quantizing non-f32/f16 tensors
;;#     bool quantize_output_tensor; // quantize output.weight
;;# } llama_model_quantize_params;

(define-cstruct _llama_model_quantize_params ([nthread _int]
                                              [llama_ftype _llama_ftype]
                                              [allow_requantize _bool]
                                              [quantize_output_tensor _bool]))



;;# // performance timing information
;;# struct llama_timings {
;;#     double t_start_ms;
;;#     double t_end_ms;
;;#     double t_load_ms;
;;#     double t_sample_ms;
;;#     double t_p_eval_ms;
;;#     double t_eval_ms;
;;
;;
;;#     int32_t n_sample;
;;#     int32_t n_p_eval;
;;#     int32_t n_eval;
;;# };
(define-cstruct _llama_timings ([t_start_ms _double]
                                [t_end_ms _double]
                                [t_load_ms _double]
                                [t_sample_ms _double]
                                [t_p_eval_ms _double]
                                [t_eval_ms _double]
                                [n_sample _int32]
                                [n_p_eval _int32]
                                [n_eval _int32]))

;# LLAMA_API struct llama_context_params llama_context_default_params();
;def llama_context_default_params() -> llama_context_params:
;    return _lib.llama_context_default_params()







