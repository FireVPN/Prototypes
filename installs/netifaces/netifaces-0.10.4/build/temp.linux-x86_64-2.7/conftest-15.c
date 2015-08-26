
            #include <sys/types.h>
            #include <sys/socket.h>
            #include <net/if.h>

            int main (void) {
              struct sockaddr sa;
              sa.sa_len = 5;
              return 0;
            }
            