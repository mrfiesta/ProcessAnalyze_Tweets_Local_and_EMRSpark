
### COnfigure roles in Amazon AMI

pip3 install awscli

### Configure AWS CLI

aws configure
AWS Access Key ID [None]: XXXXXXXXXXXXXXXXXXXXX
AWS Secret Access Key [None]: XXXXXXXXXXXXXXXXXXXX
Default region name [None]: us-west-2
Default output format [None]: json

# AWS cli environment

export AWS_DEFAULT_PROFILE=XXXXXXXX
export AWS_CONFIG_FILE=$HOME/.aws/config

# Create EMR cluster ITC profile

aws emr create-cluster --name TestSparkCluster1 --release-label emr-5.20.0 --applications Name=Spark --enable-debugging --log-uri s3://FOLDER_FOR_LOGS/Logs --instance-type m4.4xlarge --instance-count 10 --use-default-roles --configurations https://s3-us-west-2.amazonaws.com/FOLDER_WITH_FILE_TO_CONFIG_SPARK/myConfig.json

aws emr add-steps --cluster-id j-GENERATED_KEY --steps Type=spark,Name=SparkWordCountApp,Args=[--deploy-mode,cluster,--master,yarn,--conf,spark.yarn.submit.waitAppCompletion=false,--num-executors,7,--executor-cores,2,--executor-memory,8g,s3://FOLDER_FOR_FILES/TestCloudSparkEMR_firefox_geocode.py,s3://FOLDER_FOR_FILES/NL_geonames_triGram_townprovinces.csv,s3://FOLDER_WITH_ALLJSON_FILES/*.json,s3://FOLDER_FOR_OUTPUT/_wordcount,--packages,com.databricks:spark-csv_2.10:1.2.0],ActionOnFailure=CONTINUE

#Terminate cluster

aws emr terminate-clusters --cluster-ids j-GENERATED_KEY

### Copy from s3 to local
aws s3 cp s3://FOLDER_FOR_OUTPUT/ /LOCAL_FOLTER_COPY_S3_FILES/ --recursive
