#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> // For sysconf
#include <string.h> // For memset
#include <sys/mman.h>
#include <signal.h>
#include <x86intrin.h>
enum TEST_TYPE
{
    ZERO,         // ZERO page
    FIXED,        // complete memory block will made up of fixed character
    FIXED_RANDOM, // every page will have differnt character
    RANDOM        // every char is different allows for minimum page merging
};
volatile sig_atomic_t stop_flag = 0;
void handle_sigint(int signum)
{
    stop_flag = 1;
}
int main(int argc, char **argv)
{
    if (argc < 4)
    {
        printf("Usage: ./process NUM_PAGES NUM_ROUNDS ROUND_WAIT_TIME\n");
        exit(1);
    }

    signal(SIGINT, handle_sigint);

    int NUM_PAGES = atoi(argv[1]);
    int NUM_ROUNDS = atoi(argv[2]);
    int WAIT_TIME = atoi(argv[3]);

    long page_size = sysconf(_SC_PAGESIZE); // Get the system's page size
    if (page_size == -1)
    {
        perror("sysconf");
        return 1;
    }

    size_t pages = NUM_PAGES;
    size_t length = pages * page_size;

    char *addr = (char *)mmap(NULL, length, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (addr == MAP_FAILED)
    {
        perror("mmap");
        return 1;
    }
    // printf("Allocated memory of size %zu bytes (%zu pages)\n", length, pages);

    if (madvise(addr, length, MADV_MERGEABLE) == -1)
    {
        perror("madvise");
        return 1;
    }

    /*
    Fork Multiple Processes here of these kinds, define a memory usage pattern here and check KSM stats.
    */

    int round = 0;
    char c;
    while (!stop_flag && round != NUM_ROUNDS)
    {
        srand(__rdtsc());
        int test_type = RANDOM;
        switch (test_type)
        {
        case ZERO:
            memset(addr, 0, length);
            break;

        case FIXED:
            srand(__rdtsc());
            c = 'A' + rand() % 26;
            memset(addr, c, length);
            break;

        case FIXED_RANDOM:
            srand(__rdtsc());
            // printf("FIXED_RANDOM: ");
            for (int p = 0; p < pages; p++)
            {
                c = 'A' + rand() % 26;
                for (int b = 0; b < page_size; b++)
                {
                    addr[page_size * p + b] = c;
                }
            }
            break;

        case RANDOM:
            // printf("RANDOM: ");
            srand(__rdtsc());
            for (int p = 0; p < pages; p++)
            {
                for (int b = 0; b < page_size; b++)
                {
                    c = 'A' + rand() % 26;
                    addr[page_size * p + b] = c;
                }
            }
            break;
        default:
            break;
        }
        // for (int p = 0; p < 1; p++)
        // {
        //     for (int b = 0; b < 100; b++)
        //     {
        //         printf("%c", addr[page_size * p + b]);
        //     }
        //     printf("\n");
        // }

        sleep(WAIT_TIME);
        round++;
    }
    munmap(addr, length);
    return 0;
}
