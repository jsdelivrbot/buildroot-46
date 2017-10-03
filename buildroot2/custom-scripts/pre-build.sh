  #!/bin/sh
  
  cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
  chmod +x $BASE_DIR/target/etc/init.d/S41network-config

  #Compile the syscall_test.c
  BUILDROOT_DIR=$BASE_DIR/..
  COMPILER=$BUILDROOT_DIR/output/host/bin/i686-buildroot-linux-uclibc-gcc
  $COMPILER -o $BUILDROOT_DIR/output/target/bin/syscall_test $BUILDROOT_DIR/custom-scripts/syscall_test.c

  #Install drivers
  make -C $BASE_DIR/../../hello_world_driver/
  #make -C $BASE_DIR/../../my_driver/

  #Compile 
  $COMPILER -o $BUILDROOT_DIR/custom-scripts/helloWorld $BUILDROOT_DIR/custom-scripts/helloWorld.c
  cp $BUILDROOT_DIR/custom-scripts/helloWorld $BUILDROOT_DIR/output/target/bin
  make -C $BASE_DIR/../../sstf-iosched/
