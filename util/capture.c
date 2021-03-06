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
FILE *fp;

int usage(char *progname)
{
        printf("Usage: %s <interface> [<savefile name>] [<sample time(ms)>]\n", basename(progname));
        exit(11);
}

void my_callback(u_char *sample_time,const struct pcap_pkthdr* pkthdr,const u_char*
        packet)
{
    struct timeval time=pkthdr->ts;
    static int count = 1;
    static int pkt_count=1;
    static double start_time;
    static double end_time;
    double t;
    float sample=(float)(*sample_time)/1000.0;
    if(count==1)
    {
		start_time=time.tv_sec+time.tv_usec/(1000000.0);
		end_time=start_time+sample;	
		}
	else
	{
		t=time.tv_sec+time.tv_usec/(1000000.0);
		if(t<end_time)
		{
			pkt_count++;
			}
		else
		{
			printf("packets: %d \n",pkt_count);
			fprintf(fp,"%d\n",pkt_count);
			pkt_count=1;
			end_time+=sample;
			
			}
		
		}

    fprintf(stdout,"%d, ",count);
    fflush(stdout);
    count++;
    
    /*printf("the time is: %f \n", t);
    printf("the seconds: %ld \n",time.tv_sec );
    printf("the milliseconds: %ld \n", time.tv_usec);*/
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
        //u_char sample=5;
        //u_char * sample_time=&sample;
        u_char * sample_time;

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
            {	strcpy(filename,argv[2]);
                sample_time=&argv[3];
                }
        else
                strcpy(filename, PCAP_SAVEFILE);

		/*
        if ((fp = fopen(filename,"w")) == NULL) {
                fprintf(stderr,
                        "Error opening savefile \"%s\" for writing\n",
                        filename);
                fclose(fp);
                exit(7);
        }*/
        //online reading
        /*if (!(p = pcap_open_live(ifname, BUFSIZ, promisc, to_ms, errbuf))) {
                fprintf(stderr, "Error opening interface %s: %s\n",
                        ifname, errbuf);
                exit(2);
        }*/
        /*offline reading */
        if(!(p = pcap_open_offline(argv[2], errbuf)))
        {
			fprintf(stderr, "Error opening file %s: %s\n",
                        filename, errbuf);
            exit(2);
			}
	



        if ((pcount = pcap_loop(p, count, &my_callback, sample_time)) < 0) {
                /*
                 * Print out appropriate text, followed by the error message
                 * generated by the packet capture library.
                 */
                sprintf(prestr,"Error reading packets from interface %s",
                        ifname);
                pcap_perror(p,prestr);
                fclose(fp);
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
  
        pcap_close(p);
}
