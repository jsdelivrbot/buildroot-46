obj-m := hello_driver.o
KDIR := ../buildroot2/output/build/linux-master
COMPILER := ../buildroot2/output/host/bin/i686-buildroot-linux-uclibc-gcc

all:
	$(MAKE) -C $(KDIR) M=$$PWD
	$(MAKE) -C $(KDIR) M=$$PWD modules_install INSTALL_MOD_PATH=../../target
	$(COMPILER) -o test_hello_char test_hello_char.c
	cp test_hello_char ../buildroot2/output/target/bin
	
clean:
	rm -f *.o *.ko
	rm -f modules.order
	rm -f Module.symvers
	rm -f hello_driver.mod.c
	rm -f test_hello_char

