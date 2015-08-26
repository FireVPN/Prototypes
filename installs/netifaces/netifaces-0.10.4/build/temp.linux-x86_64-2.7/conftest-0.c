
            #include <sys/types.h>
            #include <sys/socket.h>
            #include <ifaddrs.h>
            int main(void) {
              struct ifaddrs *addrs;
              int ret;
              ret = getifaddrs(&addrs);
              freeifaddrs (addrs);
              return 0;
            }
            