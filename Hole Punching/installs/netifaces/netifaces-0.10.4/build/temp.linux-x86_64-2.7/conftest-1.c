
            #include <sys/types.h>
            #include <sys/socket.h>
            #include <arpa/inet.h>
            #include <netdb.h>
            #include <stdlib.h>
            int main(void) {
              struct sockaddr_in sin;
              char buffer[256];
              int ret;

              sin.sin_family = AF_INET;
              sin.sin_port = 0;
              sin.sin_addr.s_addr = htonl (INADDR_LOOPBACK);
              
              ret = getnameinfo ((struct sockaddr *)&sin, sizeof (sin),
                                 buffer, sizeof (buffer),
                                 NULL, 0,
                                 NI_NUMERICHOST);

              return 0;
            }
            