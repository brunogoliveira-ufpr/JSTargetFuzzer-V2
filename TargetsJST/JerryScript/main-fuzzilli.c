#include "main-fuzzilli.h"

#include <assert.h>
#include <fcntl.h>
#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/mman.h>

#include "jerryscript.h"
#include "jerryscript-ext/debugger.h"
#include "jerryscript-ext/handler.h"
#include "jerryscript-port.h"
#include "jerryscript-port-default.h"

#include <sanitizer/common_interface_defs.h>
#include "main-utils.h"

#define REPRL_CRFD 100
#define REPRL_CWFD 101
#define REPRL_DRFD 102
#define REPRL_DWFD 103

#define SHM_SIZE 0x100000
#define MAX_EDGES ((SHM_SIZE - 4) * 8)

#ifndef DCHECK
#define DCHECK(condition) { assert(condition); abort(); }
#endif

#ifndef CHECK
#define CHECK DCHECK
#endif

/**
 * Register a JavaScript function in the global object.
 */
static void
main_register_global_function (const char *name_p, /**< name of the function */
                               jerry_external_handler_t handler_p) /**< function callback */
{
  jerry_value_t result_val = jerryx_handler_register_global ((const jerry_char_t *) name_p, handler_p);
  assert (!jerry_value_is_error (result_val));
  jerry_release_value (result_val);
} /* main_register_global_function */

struct shmem_data {
    uint32_t num_edges;
    uint32_t num_seccov;
    double num_seccov_total;
    uint32_t num_sec_per_edge;
    double num_sec_per_edge_total;
    uint32_t usedCount;
    uintptr_t foundAddresses[10000];
    //bool found_seccov = false;
    //unsigned char current_edges[];
    //unsigned char seccov[];
    unsigned char edges[];
};

struct shmem_data* __shmem;
uint32_t *__edges_start, *__edges_stop;

void __sanitizer_cov_reset_edgeguards() {
    uint32_t N = 0;
    for (uint32_t *x = __edges_start; x < __edges_stop && N < MAX_EDGES; x++)
        *x = ++N;
}

void __sanitizer_cov_trace_pc_guard_init(uint32_t *start, uint32_t *stop) {
    // Avoid duplicate initialization
    if (start == stop || *start)
        return;

    if (__edges_start != NULL || __edges_stop != NULL) {
        fprintf(stderr, "Coverage instrumentation is only supported for a single module\n");
        _exit(-1);
    }

    __edges_start = start;
    __edges_stop = stop;

    // Map the shared memory region
    const char* shm_key = getenv("SHM_ID");
    if (!shm_key) {
        puts("[COV] no shared memory bitmap available, skipping");
        __shmem = (struct shmem_data*) malloc(SHM_SIZE);
    } else {
        int fd = shm_open(shm_key, O_RDWR, S_IRUSR | S_IWUSR);
        if (fd <= -1) {
            fprintf(stderr, "Failed to open shared memory region: %s\n", strerror(errno));
            _exit(-1);
        }

        __shmem = (struct shmem_data*) mmap(0, SHM_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
        if (__shmem == MAP_FAILED) {
            fprintf(stderr, "Failed to mmap shared memory region\n");
            _exit(-1);
        }
    }

    __sanitizer_cov_reset_edgeguards();

    __shmem->num_edges = (uint32_t) (stop - start);
    printf("[COV] edge counters initialized. Shared memory: %s with %u edges\n", shm_key, __shmem->num_edges);
    __shmem->num_sec_per_edge = 0;
    __shmem->num_sec_per_edge_total = 0;
}

void __sanitizer_cov_trace_pc_guard(uint32_t *guard) {
    uint32_t index = *guard;

    if (!index) return;
    index--;

 
    void *PC = __builtin_return_address(0); 


    void *ParserStart = (void*)0x555555599093; //vm.c
    void *ParserEnd = (void*)0x5555555d68c9;

  
    __shmem->edges[index / 8] |= 1 << (index % 8);


        if((((uintptr_t)PC < (uintptr_t)ParserEnd) && (uintptr_t)PC >= (uintptr_t)ParserStart)) { //|| (((uintptr_t)PC < (uintptr_t)LowerEnd) && ((uintptr_t)PC >= (uintptr_t)LowerStart))){

            __shmem->num_seccov_total += 1;
            __shmem->num_sec_per_edge_total += 1;


            bool isNewAddress = true;

            
            for (size_t j = 0; j < __shmem->usedCount; j++) {
                if (__shmem->foundAddresses[j] == (uintptr_t)PC) {
                    isNewAddress = false;  
                    break;                
                }
            }

            
            if (isNewAddress) {
                __shmem->foundAddresses[__shmem->usedCount] = (uintptr_t)PC;
                __shmem->usedCount++;  
                __shmem->num_seccov += 1; 
                __shmem->num_sec_per_edge += 1;

               
            }
 
        }
    //}
    *guard = 0; 

}

// We have to assume that the fuzzer will be able to call this function e.g. by
// enumerating the properties of the global object and eval'ing them. As such
// this function is implemented in a way that requires passing some magic value
// as first argument (with the idea being that the fuzzer won't be able to
// generate this value) which then also acts as a selector for the operation
// to perform.
jerry_value_t
jerryx_handler_fuzzilli (const jerry_value_t func_obj_val, /**< function object */
                      const jerry_value_t this_p, /**< this arg */
                      const jerry_value_t args_p[], /**< function arguments */
                      const jerry_length_t args_cnt) /**< number of function arguments */
{
  (void) func_obj_val; /* unused */
  (void) this_p; /* unused */

  jerry_char_t operation[256] = {0};
  jerry_value_t ret_val = jerry_create_undefined ();

  if (args_cnt > 0 && jerry_value_is_string(args_p[0]))
  {
    jerry_value_t str_val;
    str_val = jerry_value_to_string (args_p[0]);

    if (!jerry_value_is_error(str_val))
    {
      jerry_length_t length = jerry_get_utf8_string_length (str_val);

      if (length > 0 && length < 256)
      {
        jerry_string_to_utf8_char_buffer(str_val, operation, length);
      }
    }

    jerry_release_value (str_val);
  }

  if (strcmp((char *)operation, "FUZZILLI_CRASH") == 0)
  {
    if (args_cnt == 2 && jerry_value_is_number(args_p[1]))
    {
      int arg = (int) jerry_get_number_value(args_p[1]);
      switch (arg)
      {
        case 0:
          *((int*)0x41414141) = 0x1337;
          break;
        default:
          DCHECK(false);
          break;
      }
    }
  }
  else if (strcmp((char *)operation, "FUZZILLI_PRINT") == 0)
  {
    static FILE* fzliout;
    fzliout = fdopen(REPRL_DWFD, "w");
    if (!fzliout) {
      fprintf(stderr, "Fuzzer output channel not available, printing to stdout instead\n");
      fzliout = stdout;
    }

    /* Based on the jerryx_handler_print handler */
    const char * const null_str = "\\u0000";

    for (jerry_length_t arg_index = 1; arg_index < args_cnt; arg_index++)
    {
      jerry_value_t str_val;

      if (jerry_value_is_symbol (args_p[arg_index]))
      {
        str_val = jerry_get_symbol_descriptive_string (args_p[arg_index]);
      }
      else
      {
        str_val = jerry_value_to_string (args_p[arg_index]);
      }

      if (jerry_value_is_error (str_val))
      {
        /* There is no need to free the undefined value. */
        ret_val = str_val;
        break;
      }

      jerry_length_t length = jerry_get_utf8_string_length (str_val);
      jerry_length_t substr_pos = 0;
      jerry_char_t substr_buf[256];

      do
      {
        jerry_size_t substr_size = jerry_substring_to_utf8_char_buffer (str_val,
                                                                        substr_pos,
                                                                        length,
                                                                        substr_buf,
                                                                        256 - 1);

        jerry_char_t *buf_end_p = substr_buf + substr_size;

        /* Update start position by the number of utf-8 characters. */
        for (jerry_char_t *buf_p = substr_buf; buf_p < buf_end_p; buf_p++)
        {
          /* Skip intermediate utf-8 octets. */
          if ((*buf_p & 0xc0) != 0x80)
          {
            substr_pos++;
          }
        }

        if (substr_pos == length)
        {
          *buf_end_p++ = (arg_index < args_cnt - 1) ? ' ' : '\n';
        }

        for (jerry_char_t *buf_p = substr_buf; buf_p < buf_end_p; buf_p++)
        {
          char chr = (char) *buf_p;

          if (chr != '\0')
          {
            putc (chr, fzliout);
            continue;
          }

          for (jerry_size_t null_index = 0; null_str[null_index] != '\0'; null_index++)
          {
            putc (null_str[null_index], fzliout);
          }
        }
      }
      while (substr_pos < length);

      jerry_release_value (str_val);
    }

    if (args_cnt == 0 || jerry_value_is_error (ret_val))
    {
      putc ('\n', fzliout);
    }
    fflush(fzliout);
  }
  return ret_val;
}

int main_run_fuzzilli(main_args_t* arguments) {
  char helo[] = "HELO";
  if (write(REPRL_CWFD, helo, 4) != 4 ||
    read(REPRL_CRFD, helo, 4) != 4) {
    _exit(-1);
  }

  if (memcmp(helo, "HELO", 4) != 0) {
    jerry_port_log(JERRY_LOG_LEVEL_ERROR, "Invalid response from parent");
    _exit(-1);
  }

  while (1) {
    main_init_engine(arguments);
    main_register_global_function ("fuzzilli", jerryx_handler_fuzzilli);

    unsigned action = 0;
    ssize_t nread = read(REPRL_CRFD, &action, 4);
    fflush(0);
    if (nread != 4 || action != 0x63657865) { // 'exec'
      fprintf(stderr, "Unknown action %x\n", action);
      _exit(-1);
    }

    size_t script_size = 0;
    read(REPRL_CRFD, &script_size, 8);

    char* buf = malloc(script_size + 1);

    char* source_buffer_tail = buf;
    ssize_t remaining = (ssize_t) script_size;
    while (remaining > 0) {
      ssize_t rv = read(REPRL_DRFD, source_buffer_tail, (size_t) remaining);
      if (rv <= 0) {
        fprintf(stderr, "Failed to load script\n");
        _exit(-1);
      }
      remaining -= rv;
      source_buffer_tail += rv;
    }

    buf[script_size] = '\0';

    if (!jerry_is_valid_utf8_string((jerry_char_t*) buf, (jerry_size_t) script_size)) {
      jerry_port_log (JERRY_LOG_LEVEL_ERROR, "Error: Input must be a valid UTF-8 string.\n");
      _exit(-1);
    }

    jerry_value_t ret_value = jerry_parse (NULL, 0, (jerry_char_t *) buf, script_size, JERRY_PARSE_NO_OPTS);

    // Check and execute
    if (!jerry_value_is_error(ret_value)) {
      jerry_value_t func_val = ret_value;
      ret_value = jerry_run(func_val);
      jerry_release_value(func_val);
    }

    int is_error = jerry_value_is_error(ret_value);

    if (is_error) {
      // The following line also releases ret_value
      main_print_unhandled_exception(ret_value);
    } else {
      jerry_release_value(ret_value);

      ret_value = jerry_run_all_enqueued_jobs ();

      if (jerry_value_is_error(ret_value)) {
        main_print_unhandled_exception(ret_value);
      }
    }

    jerry_cleanup();

    is_error <<= 8;
    if (write(REPRL_CWFD, &is_error, 4) != 4) {
      _exit(1);
    }
    __sanitizer_cov_reset_edgeguards();
  }

  return 0;
}
