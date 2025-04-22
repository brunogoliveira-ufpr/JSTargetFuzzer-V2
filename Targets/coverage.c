// Definições de macros para comunicação via pipes e compartilhamento de memória.
#define REPRL_CRFD 100
#define REPRL_CWFD 101
#define REPRL_DRFD 102
#define REPRL_DWFD 103

#define SHM_SIZE 0x100000
#define MAX_EDGES ((SHM_SIZE - 4) * 8)

#define CHECK(cond)                                \
    if (!(cond))                                   \
    {                                              \
        fprintf(stderr, "\"" #cond "\" failed\n"); \
        _exit(-1);                                 \
    }

// Estrutura que define a área de memória compartilhada.
// `num_edges` guarda o número total de edges instrumentados,
// `num_branches` guarda o total de branches cobertos, e `edges` armazena o bitmap de cobertura.
struct shmem_data
{
    uint32_t num_edges;
    uint32_t num_branches; // Novo campo para rastrear o total de branches cobertos
    unsigned char edges[];
};

// Ponteiros globais para o início e o fim dos edge guards
struct shmem_data *__shmem;
uint32_t *__edges_start, *__edges_stop;

// Função que inicializa todos os edge guards para que possamos monitorar transições
void __sanitizer_cov_reset_edgeguards()
{
    uint64_t N = 0;
    for (uint32_t *x = __edges_start; x < __edges_stop && N < MAX_EDGES; x++)
        *x = ++N; // Atribui um número único a cada edge guard
}

// Função chamada para inicializar a cobertura quando o binário começa a rodar
extern "C" void __sanitizer_cov_trace_pc_guard_init(uint32_t *start, uint32_t *stop)
{
    // Evita inicializações duplicadas
    if (start == stop || *start)
        return;

    if (__edges_start != NULL || __edges_stop != NULL)
    {
        fprintf(stderr, "Coverage instrumentation is only supported for a single module\n");
        _exit(-1);
    }

    // Define o intervalo dos edge guards
    __edges_start = start;
    __edges_stop = stop;

    // Mapeia a região de memória compartilhada para registrar a cobertura
    const char *shm_key = getenv("SHM_ID");
    if (!shm_key)
    {
        puts("[COV] no shared memory bitmap available, skipping");
        __shmem = (struct shmem_data *)malloc(SHM_SIZE);
    }
    else
    {
        int fd = shm_open(shm_key, O_RDWR, S_IREAD | S_IWRITE);
        if (fd <= -1)
        {
            fprintf(stderr, "Failed to open shared memory region: %s\n", strerror(errno));
            _exit(-1);
        }

        __shmem = (struct shmem_data *)mmap(0, SHM_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
        if (__shmem == MAP_FAILED)
        {
            fprintf(stderr, "Failed to mmap shared memory region\n");
            _exit(-1);
        }
    }

    // Reseta e inicializa os edge guards
    __sanitizer_cov_reset_edgeguards();

    // Define o número total de edges e inicializa branches como zero
    __shmem->num_edges = stop - start;
    __shmem->num_branches = 0; // Inicializa como zero para contar branches cobertos
    printf("[COV] edge counters initialized. Shared memory: %s with %u edges and %u branches\n", shm_key, __shmem->num_edges, __shmem->num_branches);
}

// Função chamada toda vez que um edge guard é executado
extern "C" void __sanitizer_cov_trace_pc_guard(uint32_t *guard)
{
    uint32_t index = *guard; // Índice do edge guard
    if (!index)
        return;                                    // Retorna se não houver guard ativo
    __shmem->edges[index / 8] |= 1 << (index % 8); // Marca o edge como coberto no bitmap
    *guard = 0;                                    // Desativa o guard após a execução para evitar duplicação de contagem
}

// Nova função para rastrear branches específicos
extern "C" void __sanitizer_cov_trace_branch(uint32_t *branch_id)
{
    uint32_t index = *branch_id; // Índice do branch guard
    if (!index)
        return;                                    // Retorna se não houver branch ativo
    __shmem->edges[index / 8] |= 1 << (index % 8); // Marca o branch no bitmap
    *branch_id = 0;                                // Desativa o branch guard para evitar contagens duplicadas
    __shmem->num_branches++;                       // Incrementa a contagem de branches cobertos
}
