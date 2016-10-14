/*
 * Use pcap_open_live() to open a packet capture device.
 * Use pcap_dump() to output the packet capture data in
 * binary format to a file for processing later.
 */
 
#include <unistd.h>
#include <stdio.h>
#include <pcap.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <errno.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netinet/if_ether.h> 
#include <net/ethernet.h>
#include <netinet/ether.h> 
#include <libgen.h>
#include <string.h>

#define IFSZ 16
#define FLTRSZ 120
#define MAXHOSTSZ 256
#define PCAP_SAVEFILE "./pcap_savefile"

extern char *inet_ntoa();

int
usage(char *progname)
{
        printf("Usage: %s <interface> [<savefile name>]\n", basename(progname));
        exit(11);
}

int
main(int argc, char **argv)
{
        pcap_t *p;               /* packet capture descriptor */
        struct pcap_stat ps;     /* packet statistics */
        pcap_dumper_t *pd;       /* pointer to the dump file */
        char ifname[IFSZ];       /* interface name (such as "en0") */
        char filename[80];       /* name of savefile for dumping packet data */
        char errbuf[PCAP_ERRBUF_SIZE];  /* buffer to hold error text */
        char lhost[MAXHOSTSZ];   /* local host name */
        char fltstr[FLTRSZ];     /* bpf filter string */
        char prestr[80];         /* prefix string for errors from pcap_perror */   
        struct bpf_program prog; /* compiled bpf filter program */
        int optimize = 1;        /* passed to pcap_compile to do optimization */
        //int snaplen = 80;        /* amount of data per packet */
        int promisc = 1;         /* do not change mode; if in promiscuous */
                                 /* mode, stay in it, otherwise, do not */
        int to_ms = -1;        /* timeout, in milliseconds */
        int count = 20000;          /* number of packets to capture */
        uint32_t net = 0;         /* network IP address */
        uint32_t mask = 0;        /* network address mask */
        char netstr[INET_ADDRSTRLEN];   /* dotted decimal form of address */
        char maskstr[INET_ADDRSTRLEN];  /* dotted decimal form of net mask */
        int linktype = 0;        /* data link type */
        int pcount = 0;          /* number of packets actually read */

        /*
         * For this program, the interface name must be passed to it on the
         * command line. The savefile name may be optionally passed in
         * as well. If no savefile name is passed in, "./pcap_savefile" is
         * used. If there are no arguments, the program has been invoked
         * incorrectly.
         */
        if (argc < 2)
                usage(argv[0]);

        if (strlen(argv[1]) > IFSZ) {
                fprintf(stderr, "Invalid interface name.\n");
                exit(1);
        }
        strcpy(ifname, argv[1]);

        /*
         * If there is a second argument (the name of the savefile), save it in
         * filename. Otherwise, use the default name.
         */
        if (argc >= 3)
                strcpy(filename,argv[2]);
        else
                strcpy(filename, PCAP_SAVEFILE);

        /*
         * Open the network device for packet capture. This must be called
         * before any packets can be captured on the network device.
         */
        if (!(p = pcap_open_live(ifname, BUFSIZ, promisc, to_ms, errbuf))) {
                fprintf(stderr, "Error opening interface %s: %s\n",
                        ifname, errbuf);
                exit(2);
        }

        /*
         * Look up the network address and subnet mask for the network device
         * returned by pcap_lookupdev(). The network mask will be used later 
         * in the call to pcap_compile().
         */
        /*if (pcap_lookupnet(ifname, &net, &mask, errbuf) < 0) {
                fprintf(stderr, "Error looking up network: %s\n", errbuf);
                exit(3);
        }*/

        /*
         * Create the filter and store it in the string called 'fltstr.'
         * Here, you want only incoming packets (destined for this host),
         * which use port 69 (tftp), and originate from a host on the
         * local network.
         */

        /* First, get the hostname of the local system */
        if (gethostname(lhost,sizeof(lhost)) < 0) {
                fprintf(stderr, "Error getting hostname.\n");
                exit(4);
        }

        /*
         * Second, get the dotted decimal representation of the network address
         * and netmask. These will be used as part of the filter string.
         */
        //inet_ntop(AF_INET, (char*) &net, netstr, sizeof netstr);
        //inet_ntop(AF_INET, (char*) &mask, maskstr, sizeof maskstr);

        /* Next, put the filter expression into the fltstr string. */
        /*sprintf(fltstr,"dst host %s and src net %s mask %s",
                lhost, netstr, maskstr);*/
        sprintf(fltstr,"dst host %s", lhost);

        /*
         * Compile the filter. The filter will be converted from a text
         * string to a bpf program that can be used by the Berkely Packet
         * Filtering mechanism. The fourth argument, optimize, is set to 1 so
         * the resulting bpf program, prog, is compiled for better performance.
         */
        //if (pcap_compile(p,&prog,fltstr,optimize,mask) < 0) {
                /*
                 * Print out appropriate text, followed by the error message
                 * generated by the packet capture library.
                 */
        //        fprintf(stderr, "Error compiling bpf filter on %s: %s\n",
        //                ifname, pcap_geterr(p));
        //        exit(5);
        //}

        /*
         * Load the compiled filter program into the packet capture device.
         * This causes the capture of the packets defined by the filter
         * program, prog, to begin.
         */
        //if (pcap_setfilter(p, &prog) < 0) {
                /* Copy appropriate error text to prefix string, prestr */
        //        sprintf(prestr, "Error installing bpf filter on interface %s",
        //                ifname);
                /*
                 * Print error to screen. The format will be the prefix string,
                 * created above, followed by the error message that the packet 
                 * capture library generates.
                 */
        //        pcap_perror(p,prestr);
        //        exit(6);
        //}

        /*
         * Open dump device for writing packet capture data. In this sample,
         * the data will be written to a savefile. The name of the file is
         * passed in as the filename string.
         */
        if ((pd = pcap_dump_open(p,filename)) == NULL) {
                /*
                 * Print out error message if pcap_dump_open failed. This will
                 * be the below message followed by the pcap library error text,
                 * obtained by pcap_geterr().
                 */
                fprintf(stderr,
                        "Error opening savefile \"%s\" for writing: %s\n",
                        filename, pcap_geterr(p));
                exit(7);
        }

        /*
         * Call pcap_dispatch() to read and process a maximum of count (20)
         * packets. For each captured packet (a packet that matches the filter
         * specified to pcap_compile()), pcap_dump() will be called to write
         * the packet capture data (in binary format) to the savefile specified
         * to pcap_dump_open(). Note that packet in this case may not be a
         * complete packet. The amount of data captured per packet is
         * determined by the snaplen variable which is passed to
         * pcap_open_live().
         */
        if ((pcount = pcap_loop(p, count, &pcap_dump, (u_char *)pd)) < 0) {
                /*
                 * Print out appropriate text, followed by the error message
                 * generated by the packet capture library.
                 */
                sprintf(prestr,"Error reading packets from interface %s",
                        ifname);
                pcap_perror(p,prestr);
                //exit(8);
        }
        printf("Packets received and successfully passed through filter: %d.\n",
                pcount);

        /*
         * Get and print the link layer type for the packet capture device,
         * which is the network device selected for packet capture.
         */
        if (!(linktype = pcap_datalink(p))) {
                fprintf(stderr,
                        "Error getting link layer type for interface %s",
                        ifname);
                exit(9);
        }
        printf("The link layer type for packet capture device %s is: %d.\n",
                ifname, linktype);

        /*
         * Get the packet capture statistics associated with this packet
         * capture device. The values represent packet statistics from the time
         * pcap_open_live() was called up until this call.
         */
        if (pcap_stats(p, &ps) != 0) {
                fprintf(stderr, "Error getting Packet Capture stats: %s\n",
                        pcap_geterr(p));
                exit(10);
        }

        /* Print the statistics out */
        printf("Packet Capture Statistics:\n");
        printf("%d packets received by filter\n", ps.ps_recv);
        printf("%d packets dropped by kernel\n", ps.ps_drop);

        /*
         * Close the savefile opened in pcap_dump_open().
         */
        pcap_dump_close(pd);
        /*
         * Close the packet capture device and free the memory used by the
         * packet capture descriptor.
         */     
        pcap_close(p);
}
