#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <pthread.h>
#include <unistd.h>
#include <math.h>
#include <time.h>

long long primeSum = 0;

void* findNPrimeNumbers(void* N);

int main() {

    int n;
    printf("Enter the N value:  ");
    scanf("%d", &n);  
    pthread_t thread;

    clock_t start1 = clock();
    findNPrimeNumbers(&n);
    clock_t end1 = clock();

    double functionTime = (double)(end1 - start1) / CLOCKS_PER_SEC;
    long long normalSum = primeSum;

    clock_t start2 = clock();
    pthread_create(&thread, NULL, findNPrimeNumbers, &n);
    pthread_join(thread, NULL);
    clock_t end2 = clock();

    double threadTime = (double)(end2 - start2) / CLOCKS_PER_SEC;
    long long threadSum = primeSum;

    printf("Prime Sum: %lld\n", normalSum);
    printf("Normal Function Time: %.6f seconds\n", functionTime);

    printf("Prime Sum: %lld\n", threadSum);
    printf("Thread Execution Time: %.6f seconds\n", threadTime);

    return 0;
}

void* findNPrimeNumbers(void* N) {

    int n = *(int*)N;

    int limit = n < 6 ? 15 : (int)(n * (log(n) + log(log(n))));
    int* primes = (int*)malloc(limit * sizeof(int));

    primes[0] = 2;
    int count = 1;
    long long sum = 2;

    for (int num = 3; count < n; num += 2) {

        int isPrime = 1;

        for (int i = 0; i < count; i++) {

            if (primes[i] * primes[i] > num)
                break;

            if (num % primes[i] == 0) {
                isPrime = 0;
                break;
            }
        }

        if (isPrime) {
            primes[count++] = num;
            sum += num;
        }
    }

    primeSum = sum;

    free(primes);
    return NULL;
}