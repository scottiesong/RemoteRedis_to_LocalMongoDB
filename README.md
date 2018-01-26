# RemoteRedis_to_LocalMongoDB
redis in tencent cloud, mongodb in local, transform redis to mongo, by python 2.7.

Files' Description:
  count_lines.py: calculate lines about whole log files in localhost.
  eating_data.py: lpop the redis data in development.

  config.py: 
      basic configure constants, variables and functions.
  
  redis_write_disk.py: 
      reading redis data, and write log files per 10k/20k rows.
      
  zip_log_file.py: 
      compress the log files, one log file one zip pack, and calculate md5 value of per log files and writing other file.
      
  pull_zip_redis_to_mongo.py: 
      in mongo server, pull the zip packs to local, unzip and checking files' md5.
      
  read_log_to_mongo.py: 
      read each log file, and update mongoDB by log data. 'gold.type[type:xxx, sum:xxx]'
      
  cal_gold_each_person_in_mongo.py: 
      calculate gold sum and update to person record in mongoDB in every night.
