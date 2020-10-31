#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 4412

int clientSpeed = 0;
int checkServerConnection;
struct loginInput{
	char username[20];
	char password[20];
};

struct loginInput L;

int main(){

	int clientSocket, ret;
	struct sockaddr_in serverAddr;
	char buffer[1024];

	clientSocket = socket(AF_INET, SOCK_STREAM, 0);
	if(clientSocket < 0){
		printf("[CLIENT]Eroare la creare socket-ului!\n");
		exit(1);
	}
	printf("[CLIENT]Socket-ul clientului a fost creat!\n");

	memset(&serverAddr, '\0', sizeof(serverAddr));
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(PORT);
	serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

	ret = connect(clientSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
	if(ret < 0){
		printf("[CLIENT]Erroare la conectare.\n");
		exit(1);
	}
	printf("[CLIENT]Te-ai conectat cu succes la server!\n");

	while(1){
		printf("[CLIENT]Client: \t");
		scanf("%[^\n]%*c",buffer);
	    send(clientSocket, buffer, strlen(buffer), 0);

		if(strcmp(buffer, ":exit") == 0){
			close(clientSocket);
			printf("[CLIENT]Te-ai deconectat de la server!.\n");
			exit(1);
		}

		if(strcmp(buffer, ":login") == 0){
			printf("[CLIENT]Username: "),scanf("%s",L.username);
			printf("[CLIENT]Password: "),scanf("%s",L.password);
			send(clientSocket, L.username, strlen(L.username), 0);
		//	send(clientSocket, L.password, strlen(L.password), 0);
		}

		if((checkServerConnection = recv(clientSocket, buffer, 1024, 0)) < 0){
			printf("[CLIENT]Eroare la primirea datelor!\n");
		}else if(checkServerConnection > 0){
			printf("[CLIENT]Server: \t%s\n", buffer);
		} else if(checkServerConnection == 0){
			printf("[CLIENT]Server-ul este inchis!\n");
			close(clientSocket);
			exit(1);
		}
	}

	return 0;
} 