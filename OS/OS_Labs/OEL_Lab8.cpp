#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>

#define VECLEN 1000000
#define NUM_THREADS 4

typedef struct {
    double *a;
    double *b;
    double sum;
    int veclen;
} DOTDATA;

DOTDATA dotstr;
pthread_mutex_t mutexsum;

typedef struct {
    int start;
    int end;
} THREADDATA;

void *dotprod(void *arg) {
    THREADDATA *tdata = (THREADDATA *)arg;
    double *x = dotstr.a;
    double *y = dotstr.b;
    double mysum = 0.0;

    for (int i = tdata->start; i < tdata->end; i++) {
        mysum += (x[i] * y[i]);
    }

    // Protect shared sum
    pthread_mutex_lock(&mutexsum);
    dotstr.sum += mysum;
    pthread_mutex_unlock(&mutexsum);

    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    int len = VECLEN;
    double *a = (double *)malloc(len * sizeof(double));
    double *b = (double *)malloc(len * sizeof(double));
    pthread_t threads[NUM_THREADS];
    THREADDATA thread_data[NUM_THREADS];
    int chunk = len / NUM_THREADS;

    for (int i = 0; i < len; i++) {
        a[i] = 1.0;
        b[i] = a[i];
    }

    dotstr.veclen = len;
    dotstr.a = a;
    dotstr.b = b;
    dotstr.sum = 0.0;

    pthread_mutex_init(&mutexsum, NULL);

    // --- Time Measurement Start ---
    clock_t start = clock();

    // Create threads
    for (int t = 0; t < NUM_THREADS; t++) {
        thread_data[t].start = t * chunk;
        thread_data[t].end = (t == NUM_THREADS - 1) ? len : (t + 1) * chunk;
        pthread_create(&threads[t], NULL, dotprod, (void *)&thread_data[t]);
    }

    // Wait for all threads
    for (int t = 0; t < NUM_THREADS; t++) {
        pthread_join(threads[t], NULL);
    }

    // --- Time Measurement End ---
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;

    printf("Multi-threaded Execution Finished.\n");
    printf("Sum = %f\n", dotstr.sum);
    printf("Execution Time: %f seconds\n", time_spent);

    pthread_mutex_destroy(&mutexsum);
    free(a);
    free(b);

    pthread_exit(NULL);
}
