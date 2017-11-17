#source check_hadoop_tasks.sh
RUNPY="sh -x py27/py27.sh"
#RUNPY="./pypy/opt/pypy-bin/bin/pypy"
HADOOP_HOME="/home/map/platform/hadoop-gz/hadoop-client2/hadoop/"
HADOOP_HOME="/home/map/platform/hadoop-guoke/hadoop/"
HADOOP_HOME="/home/map/platform/hadoop_lbs-traj/"
#UGI="hadoop.job.ugi=lbs-guiji,geomining0718"
#UGI="hadoop.job.ugi=map-client,map-client"
UGI="hadoop.job.ugi=lbs-guoke,lbs-guoke"
#UGI="hadoop.job.ugi=ns-webgis,,mMlxRqi3SDezGoZV"
#QUEUE="mapred.job.queue.name=lbs_gzns"
#QUEUE="mapred.job.queue.name=map-client"
QUEUE="mapred.job.queue.name=lbs-guoke"
QUEUE="mapred.job.queue.name=ns-webgis"
JOBUGI="-jobconf $UGI -jobconf $QUEUE"

JOBUGI=""
#PYTAR="/app/lbs/traj/tools/py2.tar.gz#py27"
PYTAR="/app/lbs/traj/tools/pypy.tar.gz#py27"
#PYTAR="/user/lbs-guiji/traj/zhuozhengxing//pypy.tar.gz#py27"
#PYTAR="/user/lbs-guiji/traj/zhuozhengxing//py27.tar.gz#py27"
#PYTOOLS="/user/lbs-guiji/traj/zhuozhengxing//pytools.tar#pytools"

PYTOOLS="/app/lbs/traj/zhuozhengxing/tools/pytools.tar#pytools"
PYTAR="/app/lbs/traj/zhuozhengxing/tools/py27.tar.gz#py27"
#PYTAR="/app/lbs/traj/zhuozhengxing/pypy_bin.tar.gz#pypy"
#RUNPY="./pypy/opt/pypy-bin/bin/pypy"

#JOB_PRIORITY=NORMAL
JOB_PRIORITY=VERY_HIGH

date=20171106
if [ -z $date ];then exit 1;fi
#train
#INPUT=/app/lbs/traj/zhanghuaizhi/conn_mark/20170601.apxy_joined/part-00000.gz
input_cw=/app/lbs/traj/caoyanbin/ssid/poi_ap_cw.txt
input_hw=/app/lbs/traj/caoyanbin/ssid/poi_ap_hw.txt
input_cw2=/app/lbs/traj/caoyanbin/ssid/poi_ap_cw2.txt
input_ssid=/app/lbs/traj/ssid/20171111/*
#INPUT=/app/lbs/traj/zhanghuaizhi/conn_mark/20170606.apxy_joined/part-00000.gz
OUTPUT=/app/lbs/traj/caoyanbin/ssid/poi_ssid_xy.txt

$HADOOP_HOME/bin/hadoop dfs -D $UGI -rmr $OUTPUT
$HADOOP_HOME/bin/hadoop streaming\
	-input $input_hw \
	-input $input_cw\
	-input $input_ssid\
	-output $OUTPUT \
	-mapper "$RUNPY mapper_ssid.py"\
	-reducer "$RUNPY reducer.py" \
	$JOBUGI \
	-jobconf abaci.is.dag.job=true\
	-jobconf abaci.dag.vertex.num=5 \
	-jobconf abaci.dag.next.vertex.list.0=4 \
	-jobconf abaci.dag.next.vertex.list.1=4 \
	-jobconf abaci.dag.next.vertex.list.2=4 \
	-jobconf abaci.dag.next.vertex.list.3=4 \
	-jobconf stream.map.streamprocessor.0="$RUNPY mapper_ssid.py" \
	-jobconf stream.map.streamprocessor.1="$RUNPY mapper_hw.py" \
	-jobconf stream.map.streamprocessor.2="$RUNPY mapper_cw.py" \
	-jobconf stream.map.streamprocessor.3="cat" \
    -jobconf stream.reduce.streamprocessor.4="$RUNPY reducer.py"\
    -jobconf mapred.job.name="traj_join-${date}_ssid_caoyanbin" \
	-jobconf mapred.input.dir.0=$input_ssid \
	-jobconf mapred.input.dir.1=$input_hw \
	-jobconf mapred.input.dir.2=$input_cw \
	-jobconf mapred.input.dir.3=$input_cw \
	-jobconf mapred.map.tasks=100\
	-jobconf mapred.reduce.tasks=500\
	-jobconf mapred.job.map.capacity=200\
	-jobconf mapred.job.reduce.capacity=200\
	-jobconf abaci.job.map.memory.mb=50 \
    -jobconf abaci.job.reduce.memory.mb=100\
	-jobconf stream.memory.limit=800\
	-jobconf mapred.job.priority=$JOB_PRIORITY \
	-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner -jobconf stream.num.map.output.key.fields=2 -jobconf num.key.fields.for.partition=1  \
	-file reducer.py\
	-file mapper_ssid.py\
	-file util.so\
    -file mapper_cw.py\
    -file mapper_hw.py\
	-cacheArchive $PYTAR  -cacheArchive $PYTOOLS
if [ $? -ne 0 ];then exit 1;fi

#-mapper "$RUNPY learn_cluster.py|$RUNPY train_byrf.py train"\
#-jobconf mapred.output.compress=true\
#-reducer "$RUNPY eva_error.py" \
#-jobconf stream.reduce.streamprocessor.2="$RUNPY eva_error_puc2.py" \
#-jobconf stream.reduce.streamprocessor.1="$RUNPY train_v2.py -mode x" \
