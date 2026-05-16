#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <pthread.h>

void* findNPrimeNumbers(void* N);
void* runTill100Seconds(void* N);

int main() {
    int n1 = 10, n2 = 2, n3 = 3;
    pthread_t thread1, thread2, thread3; 
    
    pthread_create(&thread1, NULL, findNPrimeNumbers, &n1);

    pthread_create(&thread2, NULL, runTill100Seconds, &n2);

    pthread_create(&thread3, NULL, runTill100Seconds, &n3);
}