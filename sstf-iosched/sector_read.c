/*
 * Simple disc I/O generator - Implemented by Carlos Moratelli
 *
 */

#include<stdio.h>
#include<stdlib.h>
#include<errno.h>
#include<fcntl.h>
#include<string.h>
#include<unistd.h>

#define BUFFER_LENGTH 256
#define DISC_SZ	1073741824

int main(){
	int ret, fd, pid, i;
	unsigned int pos;
	char buf[BUFFER_LENGTH] = "oi";

	printf("Starting sector read example...\n");
	
	printf("Cleanning disc cache...\n");
	system("echo 3 > /proc/sys/vm/drop_caches");		
	
	srand(getpid());
	
	fd = open("/dev/sdb", O_RDWR);             // Open the device with read/write access
	if (fd < 0){
		perror("Failed to open the device...");
		return errno;
	}
	
    for (int i=0; i<6; i++) {
        fork();
    }
    sleep(1);
    srand(getpid());
    //for(int i =0; i<50; i++){

	    /* Random position on disc */
	    pos = rand()%DISC_SZ;

	    /* Set position */
	    lseek(fd, pos, SEEK_SET);

    	read(fd, buf, 20);

	//}
	close(fd);
	
	return 0;
}
