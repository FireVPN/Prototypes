
            #include <asm/types.h>
            #include <sys/socket.h>
            #include <linux/netlink.h>
            #include <linux/rtnetlink.h>

            int main (void) {
              int s = socket (PF_NETLINK, SOCK_RAW, NETLINK_ROUTE);
              return 0;
            }
            