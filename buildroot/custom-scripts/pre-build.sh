  #!/bin/sh
  
  cp $BASE_DIR/../custom-scripts/S41network-config $BASE_DIR/target/etc/init.d
  chmod +x $BASE_DIR/target/etc/init.d/S41network-config
  mkdir -p $BASE_DIR/target/home/server
  chmod +x $BASE_DIR/../custom-scripts/setUpServer.py
  cp $BASE_DIR/../custom-scripts/setUpServer.py $BASE_DIR/target/home/server
  cp $BASE_DIR/../custom-scripts/ServerConfig $BASE_DIR/target/etc/init.d
  chmod +x $BASE_DIR/target/etc/init.d/ServerConfig
