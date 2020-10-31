#include <sys/types.h>
#include <sys/socket.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <malloc.h>
#include <string.h>
#include <dirent.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#ifndef SERVER
#define SERVER

#define PORT 4412

char connectedClients[10][30];
int countConnectedClients = 0;
char i[30];

struct loginInput{
	char username[20];
	char password[20];
};

struct loginInput L;

void startServer(){
     int sockfd, ret;
	 struct sockaddr_in serverAddr;

	int newSocket;
	struct sockaddr_in newAddr;

	socklen_t addr_size;

	char buffer[1024];

	pid_t childpid;

	sockfd = socket(AF_INET, SOCK_STREAM, 0);
	if(sockfd < 0){
		close(sockfd);
		printf("[SERVER]Eroare la crearea socket-ului\n");
		exit(1);
	}
	printf("[SERVER]Socket-ul server-ului a fost creat!\n");

	memset(&serverAddr, '\0', sizeof(serverAddr));
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(PORT);
	serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

	ret = bind(sockfd, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
	if(ret < 0){
		printf("[SERVER]Eroare la bind\n");
		exit(1);
	}
	printf("[SERVER]Bind la port-ul %d\n", PORT);

	if(listen(sockfd, 10) == 0){
		printf("[SERVER]Listening....\n");
	}else{
		close(sockfd);
		printf("[SERVER]Eroare la bind!\n");
	}


	while(1){
		newSocket = accept(sockfd, (struct sockaddr*)&newAddr, &addr_size);
		if(newSocket < 0){
			exit(1);
		}

		countConnectedClients++;
		printf("[SERVER]Clientul cu ip-ul %s:%d s-a conectat!\n", inet_ntoa(newAddr.sin_addr), ntohs(newAddr.sin_port));

		if((childpid = fork()) == 0){
			close(sockfd);

			while(1){
				sprintf(i,"%d",countConnectedClients);
				int checkClientConnection = recv(newSocket, buffer, 1024, 0);
				if(strcmp(buffer, ":exit") == 0 || checkClientConnection == 0){
					printf("[SERVER]Clientul cu ip-ul %s:%d s-a deconectat!\n", inet_ntoa(newAddr.sin_addr), ntohs(newAddr.sin_port));
					break;
				}  else if(strcmp(buffer, "?")==0){
					send(newSocket,i,strlen(i),0);
					printf("Fsalut\n");
				} else if(strcmp(buffer,":login")==0){
					recv(newSocket, L.username, 20, 0);
					recv(newSocket, L.password, 20, 0);
					printf("[SERVER]%s %s\n",L.username,L.password);
		     	} else{	
					printf("[SERVER]: %s\n", buffer);
					send(newSocket, buffer, strlen(buffer), 0);
					bzero(buffer, sizeof(buffer));
				}
			}
		}

	}

	close(newSocket);

}

#endif