#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Day {
    char dayName [10];
    char tasks [3][100];
} Day;

int main() {
    Day days[7];

    for (int i = 0; i < 7; i++) {
        days[i].dayName[0] = '\0';
        for (int j = 0; j < 3; j++) {
            days[i].tasks[j][0] = '\0';
        }
    }

    while(1) {
        char input[10];
        printf("Enter a day of the week (or 'exit' to quit): ");
        fgets(input, sizeof(input), stdin);
        input[strcspn(input, "\n")] = '\0';

        if (strcmp(input, "exit") == 0) {
            break;
        }

        int index = -1;
        if (strcmp(input, "Monday") == 0) index = 0;
        else if (strcmp(input, "Tuesday") == 0) index = 1;
        else if (strcmp(input, "Wednesday") == 0) index = 2;
        else if (strcmp(input, "Thursday") == 0) index = 3;
        else if (strcmp(input, "Friday") == 0) index = 4;
        else if (strcmp(input, "Saturday") == 0) index = 5;
        else if (strcmp(input, "Sunday") == 0) index = 6;

        if (index != -1) {
            strcpy(days[index].dayName, input);
            taskInput:
            printf("Enter the number of tasks for %s: ", input);
            int numTasks;
            scanf("%d%*c", &numTasks);
            
            if(numTasks > 3){
                fprintf(stderr, "No. of tasks is greater than 3, give tasks less than 3\n");
                goto taskInput;
            }
            
            while(numTasks--) {
                char task[100];
                printf("Enter a task: ");
                fgets(task, sizeof(task), stdin);
                task[strcspn(task, "\n")] = '\0';
                if(strlen(task) >= 100){
                    fprintf(stderr, "Task name is too long, give task name less than 100 characters\n");
                    numTasks++;
                    continue;
                }
                strcpy(days[index].tasks[numTasks], task);
            }
        }
    }

    printf("\nWeekly Schedule:\n");
    for (int i = 0; i < 7; i++) {
        if (strlen(days[i].dayName) > 0) {
            printf("%s:\n", days[i].dayName);
            for (int j = 0; j < 3; j++) {
                if (strlen(days[i].tasks[j]) > 0) {
                    printf("  - %s\n", days[i].tasks[j]);
                }
            }
        }
    }

}