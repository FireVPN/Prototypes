
            #include <sys/types.h>
            #include <sys/socket.h>
            #include <sys/sysctl.h>
            #include <net/route.h>

            int main (void) {
              int mib[] = { CTL_NET, PF_ROUTE, 0, AF_INET, NET_RT_FLAGS,
                            RTF_UP | RTF_GATEWAY };
              return 0;
            }
            