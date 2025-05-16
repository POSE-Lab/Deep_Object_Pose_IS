## Steps to run Experiments

### Preprocessing the data
Run the following command locally (not inside Docker):
```bash
DATASET_PATH=/path/to/IndustryShapes
python3 utils/prepare_dataset.py \
  --data_folder $DATASET_PATH/train/ \
  --output_folder data/preprocessed \
  --models_path $DATASET_PATH/models_eval \
  --obj_map  obj_names.json\
  --scenes "000001 000002 000003 000004 000005 000006 000007 000008 000009 000010 000011 000012 000013"
```

### Build the docker image
From the directory containing the Dockerfile.noetic (`docker/`), run:

**For training:**

```bash
cd docker
docker build -t nvidia-dope:train -f train/Dockerfile.noetic ..
```

**For inference:**

```bash
cd docker
docker build -t nvidia-dope:test -f train/Dockerfile.noetic ..
```

### Training the model

Apply some minor modifications to `Deep_Object_Pose` repo:

```bash
cd Deep_Object_Pose
git apply ../diff.patch
```

Activate docker container

```bash
./run_dope_docker.sh dope-training nvidia-dope:train
```



From the project root (outside the Docker directory), run:

```bash
python3 -m torch.distributed.launch --nproc_per_node=1 train.py --network dope --epochs 100 --batchsize 1 --outf tmp/ --data /path/to/data/preprocessed
```

### Running inference

Activate docker container

```bash
./run_dope_docker.sh dope-testing nvidia-dope:test
```



**Example for running inference on one test scene:**

```bash
python3 inference.py --config /path/to/config/test_scenes/config_pose_000001.yaml --camera /path/to/config/test_scenes/camera_info_000001.yaml --data /path/to/data/000001/rgb/
```

**Example running on all test scenes**

```bash
for i in $(seq -w 1 8); do
  python3 inference.py --config /path/to/config/test_scenes/config_pose_00000$i.yaml \
                       --camera /path/to/config/test_scenes/camera_info_00000$i.yaml \
                       --data /path/to/test-dataset/00000$i/rgb/ \
                       --outf /path/to/output_experiments/00000$i
done

```

### Evaluation using bop toolkit

Create `bop_predictions.csv` file using the following script


```bash
python utils/results_to_bop.py \
  --root_folder /path/to/output_experiments/ \
  --outf /path/to/evaluation_results/ \
  --modelpath /path/to/IndustryShapes/models_eval
```

(Optional) If you want to visualize the results, add `--visualize` flag to the command above.
