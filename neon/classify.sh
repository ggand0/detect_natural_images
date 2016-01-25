#!/bin/bash -e

data_dir=~/Projects/illust_detection/detect_natural_images #$1
num_epochs=40 #40
imwidth=128 #384


#echo Writing macrobatches: `date`
#python batch_writer.py --set_type directory --image_dir=$data_dir/illust-cosplay/train --data_dir=$data_dir/neon/trainbatches --target_size $imwidth --val_pct 0
#python batch_writer.py --set_type directory --image_dir=$data_dir/illust-cosplay/val --data_dir=$data_dir/neon/valbatches --target_size $imwidth --val_pct 1
#python batch_writer.py --set_type directory --image_dir=$data_dir/illust-cosplay/test --data_dir=$data_dir/neon/testbatches --target_size $imwidth --val_pct 1

for i in {1..10}
do
  echo Classifying: `date`
  #python classifier.py -z32 -e 50 --eval_freq 1 --output_file callbackdata.h5 -w $data_dir/neon/trainbatches -vw $data_dir/neon/valbatches -tw $data_dir/neon/testbatches -r0 -s model3.pkl -bgpu -iw $imwidth --serialize 1 ${@:2}
  python classifier.py -z32 -e 50 --no_progress_bar --eval_freq 1 --output_file callbackdata.h5 -w $data_dir/neon/trainbatches -vw $data_dir/neon/valbatches -tw $data_dir/neon/testbatches -r0 -s model3.pkl -bgpu -iw $imwidth --serialize 1 >> train-output #${@:2}
done

echo Done: `date`
