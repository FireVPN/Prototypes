
            #include <sys/types.h>
            #include <sys/socket.h>
            #include <net/route.h>

            int main (void) {
              struct rt_msghdr msg;
              int s = socket (PF_ROUTE, SOCK_RAW, 0);
              return 0;
            }
            