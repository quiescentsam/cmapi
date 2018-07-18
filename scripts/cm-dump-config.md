

```
/anaconda3/envs/python27/bin/python /Users/ssiddiqui/Desktop/SAMEER2.0/WORK/CODE/cmapi/scripts/cm-dump-config.py
CLUSTER [CDH, Running: 5.14.4, URL: https://ip-172-31-94-88.ec2.internal:7183/cmf/clusterRedirect/CDH]
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  SERVICE : [HDFS - HDFS-1, URL: https://ip-172-31-94-88.ec2.internal:7183/cmf/serviceRedirect/CD-HDFS-UqLSrvgj]
==================================================================================================================================
  hadoop_group_mapping_ldap_keystore                                    : {{CM_AUTO_TLS}}
  hadoop_group_mapping_ldap_keystore_passwd                             : {{CM_AUTO_TLS}}
  hadoop_group_mapping_ldap_use_ssl                                     : true
  hdfs_hadoop_ssl_enabled                                               : true
  ssl_client_truststore_location                                        : {{CM_AUTO_TLS}}
  ssl_client_truststore_password                                        : {{CM_AUTO_TLS}}
  ssl_server_keystore_keypassword                                       : {{CM_AUTO_TLS}}
  ssl_server_keystore_location                                          : {{CM_AUTO_TLS}}
  ssl_server_keystore_password                                          : {{CM_AUTO_TLS}}
  -------------------------------------------------------------  ROLE  -------------------------------------------------------------
  Role name                                                             : CD-H8307a14c-SECONDARYNAMENODE-04c86cd31a11f0444db3718888764a32
  Role hostId                                                           : 961b1bab-b023-49e4-8182-9893856bae6f
  fs_checkpoint_dir_list                                                : /dfs/snn
  secondary_namenode_java_heapsize                                      : 2700083200
  -------------------------------------------------------------  ROLE  -------------------------------------------------------------
  Role name                                                             : CD-HDFS-UqLSrvgj-BALANCER-04c86cd31a11f0444db3718888764a32
  Role hostId                                                           : 961b1bab-b023-49e4-8182-9893856bae6f
  balancer_java_heapsize                                                : 1073741824
  -------------------------------------------------------------  ROLE  -------------------------------------------------------------
  Role name                                                             : CD-HDFS-UqLSrvgj-DATANODE-04c86cd31a11f0444db3718888764a32
  Role hostId                                                           : 961b1bab-b023-49e4-8182-9893856bae6f
  datanode_java_heapsize                                                : 1073741824
  dfs_data_dir_list                                                     : /dfs/dn
  dfs_datanode_du_reserved                                              : 5367553638
  dfs_datanode_failed_volumes_tolerated                                 : 0
  dfs_datanode_max_locked_memory                                        : 3510632448
  -------------------------------------------------------------  ROLE  -------------------------------------------------------------
  Role name                                                             : CD-HDFS-UqLSrvgj-NAMENODE-04c86cd31a11f0444db3718888764a32
  Role hostId                                                           : 961b1bab-b023-49e4-8182-9893856bae6f
  dfs_name_dir_list                                                     : /dfs/nn
  dfs_namenode_handler_count                                            : 30
  dfs_namenode_service_handler_count                                    : 30
  dfs_namenode_servicerpc_address                                       : 8022
  namenode_java_heapsize                                                : 2700083200

Process finished with exit code 0
```