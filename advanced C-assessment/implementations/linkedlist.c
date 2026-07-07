#include <stdio.h>
#include <stdlib.h>

typedef struct SinglyLinkedList {
    int data;
    struct SinglyLinkedList* next;
} SinglyLinkedList;

void insert(SinglyLinkedList **head, int n) {

    SinglyLinkedList *node = malloc(sizeof(*node));

    // check allocation of memory 
    if (node == NULL) {
        printf("Memory allocation failed!");
        return;
    }

    node->data = n;
    node->next = NULL;

    // handle empty list
    if (*head == NULL) {
        *head = node;
        return;
    }

    // insert at last logic
    SinglyLinkedList* temp = *head;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = node;
}

void delete(SinglyLinkedList **head, int n) {

    /* head - reference to the address of pointer pointing to the linked List
        n - the number to be deleted from the list
    */
    
    // handle empty list
    if (*head == NULL)
        return;
    
    // if the node to be deleted is head
    if ((*head)->data == n) {
        SinglyLinkedList *temp = *head;
        *head = (*head)->next;
        free(temp);
        return;
    }
    SinglyLinkedList *temp = *head, *prev = NULL;

    while(temp != NULL && temp->data != n) {
        prev = temp;
        temp = temp->next;
    }

    if(temp == NULL) {
        printf("Number not found");
        return;
    }

    prev->next = temp->next;
    free(temp);

}

void update(SinglyLinkedList **head, int oldVal, int newVal) {

    // check empty list
    if (*head == NULL) {
        printf("Empty List");
    }

    SinglyLinkedList *temp = *head;
    
    // loop to find the values
    while (temp != NULL) {
        if (temp->data == oldVal) {
            temp->data = newVal;
            return;
        }
        temp = temp->next; 
    }
            
}

void read(SinglyLinkedList **head) {
    SinglyLinkedList *temp = *head;

    while(temp != NULL) {
        if(temp->next != NULL)
            printf("[%d | %p]->", temp->data, temp->next);
        else
            printf("[%d | %p]", temp->data, temp->next);

        temp = temp->next;
    }        
}

int main() {
    // switch based menu driven program
    SinglyLinkedList *head = NULL;
    int choice, n, oldVal, newVal;
    while (1) {
        printf("\n1. Insert\n2. Delete\n3. Update\n4. Read\n5. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter the number to insert: ");
                scanf("%d", &n);
                insert(&head, n);
                break;
            case 2:
                printf("Enter the number to delete: ");
                scanf("%d", &n);
                delete(&head, n);
                break;
            case 3:
                printf("Enter the old value: ");
                scanf("%d", &oldVal);
                printf("Enter the new value: ");
                scanf("%d", &newVal);
                update(&head, oldVal, newVal);
                break;
            case 4:
                read(&head);
                break;
            case 5:
                exit(0);
            default:
                printf("Invalid choice! Please try again.");
        }
    }
}
