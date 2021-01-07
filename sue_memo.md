

cd ~/catkin_ws/src/ai_race/scripts
bash prepare.sh -l 1t

cd ~/catkin_ws/src/ai_race/scripts
./stop.sh

cd ~/catkin_ws/src/ai_race/ai_race/utility/scripts
python keyboard_con_pygame2.py
l 進む,a 左にまがる,d 右にまがる

roslaunch sim_environment rosbag.launch

cd ~/catkin_ws/src/ai_race/ai_race/utility/scripts
python rosbag_to_images_and_commands.py ~/_2020-12-30-13-23-45.bag

#train
cd ~/catkin_ws/src/ai_race/ai_race/learning/scripts
python3 train.py --data_csv $HOME/Images_from_rosbag/data-20210105/data-20210105.csv --model simplenet --model_name 0107 --n_epoch 11

python3 trt_conversion.py --pretrained_model $HOME/work/experiments/models/checkpoints/sim_race_0107_epoch=11.pth --trt_model $HOME/work/experiments/models/checkpoints/sim_race_0107_epoch=11_trt.pth --model simplenet

cd ~/catkin_ws/src/ai_race/ai_race/learning/scripts
python inference_from_image.py --trt_module --trt_model $HOME/work/experiments/models/checkpoints/sim_race_0107_epoch=11_trt.pth


resnet18
Computational complexity:       2.83 GMac
Number of parameters:           11.18 M 

simplenet
Computational complexity:       0.09 GMac
Number of parameters:           624.64 k

simplenet + in 120x160
Computational complexity:       0.02 GMac
Number of parameters:           153.6 k 

simplenet + in 120x160 + del fc1 + add global_ave_pool
Computational complexity:       0.02 GMac
Number of parameters:           9.78 k 
epoch:  11, train acc: 0.866211, train loss: 0.017605, test acc: 0.843137, test loss: 0.021321
LAP:31(+0.4),CourseOut:1,Recovery:0

simplenet + in 60x160 + del fc1 + add global_ave_pool + del conv5
Computational complexity:       0.01 GMac
Number of parameters:           7.46 k
epoch:  11, train acc: 0.866211, train loss: 0.019126, test acc: 0.886275, test loss: 0.02091
CourseOut:IPPAIATTA

