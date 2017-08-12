BASE_PATH = D:/wuzhijing/resp/QA_demo

# source_path = BASE_PATH/data/squad/dev-v1.1.json
source_path = D:/wuzhijing/resp/QA_demo/data/squad/dev-v1.1.json
target_path = single.json
inter_dir = "inter_single"
root_dir = "save"

if:debug
	parg = -d
	marg = --debug
	
# proprocess data
python3 -m squad.prepro --mode single --single_path $source_path $parg --target_dir $inter_dir --glove_dir .

python -m squad.prepro --mode single --single_path D:/wuzhijing/resp/QA_demo/data/squad/dev-v1.1.json --target_dir inter_single --glove_dir .


num=37
load_path="save/37/save"
shared_path="save/37/shared.json"
eval_path="inter_single/eval.json"
python3 -m basic.cli --data_dir $inter_dir --eval_path $eval_path --nodump_answer --load_path $load_path --shared_path $shared_path $marg --eval_num_batches 0 --mode forward --batch_size 1 --len_opt --cluster --cpu_opt --load_ema

python -m basic.cli --data_dir inter_single --eval_path inter_single/eval.json --nodump_answer --load_path save/37/save --shared_path save/37/shared.json --eval_num_batches 0 --mode forward --batch_size 1 --len_opt --cluster --cpu_opt --load_ema


# Ensemble (for single run, just one input)
python3 -m basic.ensemble --data_path $inter_dir/data_single.json --shared_path $inter_dir/shared_single.json -o $target_path $eval_path

python -m basic.ensemble --data_path inter_single/data_single.json --shared_path inter_single/shared_single.json -o single.json inter_single/eval.json


python squad/evaluate-v1.1.py D:/wuzhijing/resp/QA_demo/data/squad/dev-v1.1.json D:/wuzhijing/resp/QA_demo/out/basic/00/answer/test-000002.json

python squad/evaluate-v1.1.py D:/wuzhijing/resp/QA_demo/data/squad/dev-v1.1.json D:/wuzhijing/resp/QA_demo/single.json