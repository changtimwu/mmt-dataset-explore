#!/bin/sh
OVTDIR="$HOME/openvino/training_extensions"
MMTDIR="$HOME/openvino/mmt2cvat"
origdir=${PWD}

setup_env() {
  cd $OVTDIR/models/object_detection
  ./init_venv.sh
  . venv/bin/activate
}

select_model() {
    export modelnm=$1
    export MODEL_TEMPLATE=`realpath ./model_templates/person-detection/$modelnm/template.yaml`
    export WORK_DIR=/tmp/my-$(basename $(dirname $MODEL_TEMPLATE))
    export SNAPSHOT=snapshot.pth
    python ../../tools/instantiate_template.py ${MODEL_TEMPLATE} ${WORK_DIR}
}

perf_eval() {
    tds=$1
    TEST_ANN_FILE="$MMTDIR/${tds}.json"
    TEST_IMG_ROOT="$MMTDIR/$tds/$tds"
    metricsnm="metrics_${modelnm}_${tds}.yaml"
    python eval.py  --load-weights ${SNAPSHOT} --test-ann-files ${TEST_ANN_FILE} --test-data-roots ${TEST_IMG_ROOT} --save-metrics-to $metricsnm
    cp $metricsnm $origdir
}


setup_env
#select_model "person-detection-0203"
#cd $WORK_DIR
#perf_eval "airport"
#perf_eval "MMTPerson200329_Ch004"
#perf_eval "MMTPerson200329_Ch007"

select_model "person-detection-0201"
cd $WORK_DIR
perf_eval "airport"
perf_eval "MMTPerson200329_Ch004"
perf_eval "MMTPerson200329_Ch007"


