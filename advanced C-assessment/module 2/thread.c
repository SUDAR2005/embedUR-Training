#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <math.h>
#include <stdlib.h>

void* sumOfNPrimes(void* N);

void* threadRunFor100Seconds(void* N);

int main() {
    pthread_t thread1, thread2, thread3;
    int n1 = 10;
    // n2 and n3 are sleep time for thread 2 and thread 3
    int n2 = 2;
    int n3 = 3;

    pthread_create(&thread1, NULL, sumOfNPrimes, &n1);
    pthread_create(&thread2, NULL, threadRunFor100Seconds, &n2);
    pthread_create(&thread3, NULL, threadRunFor100Seconds, &n3);

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    pthread_join(thread3, NULL);

    return 0;
}

void* sumOfNPrimes(void* N) {
    int n = *(int*)N;
    if (n < 1) {
        printf("N must be greater than 0.\n");
        return NULL;
    }
    // Upper bound
    int limit = (n < 6) ? 15 : (int)(n * (log(n) + log(log(n))));
    int* primes = (int*)malloc(limit * sizeof(int));
    
    primes[0] = 2;
    int count = 1;
    long long sum = 2;
    
    printf("Prime 1: 2\n");

    for (int num = 3; count < n; num += 2) {
        int isPrime = 1;
        for (int i = 0; i < count; i++) {
            if (primes[i] * primes[i] > num) {
                break;
            }
            if (num % primes[i] == 0) {
                isPrime = 0;
                break;
            }
        }
        
        if (isPrime) {
            primes[count++] = num;
            sum += num;
            printf("Prime %d: %d\n", count, num);
        }
    }
    printf("\nTotal Sum = %lld for n primes is %d\n\n", sum, n);

    free(primes);
    return NULL;
}


void* threadRunFor100Seconds(void* N) {
    int interval = *(int*)N;
    int elapsed = 0;


    while (elapsed < 100) {
        int chunk = interval;

        if (elapsed + chunk > 100) {
            chunk = 100 - elapsed;
        }

        sleep(chunk);
        elapsed += chunk;
        printf("Thread running every %d seconds.\n", interval);
    }

    printf("Thread finished after 100 seconds.\n");
    return NULL;
}