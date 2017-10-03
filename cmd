  sudo qemu-system-i386 --device e1000,netdev=eth0,mac=aa:bb:cc:dd:ee:ff \
  	--netdev tap,id=eth0,script=buildroot2/custom-scripts/qemu-ifup \
  	--kernel buildroot2/output/images/bzImage \
  	--hda buildroot2/output/images/rootfs.ext2 \
  	--nographic \
  	--append "console=ttyS0 root=/dev/sda" \
    --hdb sdb.bin
  

modprobe sstf-iosched

echo sstf > /sys/block/sdb/queue/scheduler

sector_read
