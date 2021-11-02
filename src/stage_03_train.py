from src.utils.all_utils import read_yaml,create_directory,save_local_df
import argparse
import pandas as pd 
import os,joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet


def train(config_path,params_path):
    config = read_yaml(config_path)
    params = read_yaml(params_path)


    artifacts_dir = config["artifacts"]["artifacts_dir"]
    raw_local_dir = config["artifacts"]["raw_local_dir"]
    raw_local_file = config["artifacts"]["raw_local_file"]


    raw_local_dir_path = os.path.join(artifacts_dir,raw_local_dir,raw_local_file)
    df = pd.read_csv(raw_local_dir_path)
    split_size = params["base"]["test_size"]
    random_state = params["base"]["random_state"]


    split_data_dir = config["artifacts"]["split_data_dir"]

    train_data_filename = config["artifacts"]["train"]
    test_data_filename = config["artifacts"]["test"]

    train_data_path = os.path.join(artifacts_dir,split_data_dir,train_data_filename)
    test_data_path = os.path.join(artifacts_dir,split_data_dir,test_data_filename)

    train_data = pd.read_csv(train_data_path)

    train_y = train_data["quality"]
    train_x = train_data.drop("quality",axis=1)
    alpha =params["model_params"]["ElasticNet"]["alpha"]
    l1_ratio =params["model_params"]["ElasticNet"]["l1_ratio"]
    random_state = params["base"]["random_state"]

    lr = ElasticNet(alpha = alpha,l1_ratio=l1_ratio ,random_state=random_state)
    lr.fit(train_x,train_y)


    model_dir = config["artifacts"]["model_dir"]
    model_file = config["artifacts"]["model_file"]
    
    model_dir = os.path.join(artifacts_dir,model_dir) 
    create_directory([model_dir])
    model_path = os.path.join(model_dir,model_file) 

    joblib.dump(lr,model_path)



if __name__ == '__main__':

    
    args = argparse.ArgumentParser()
    args.add_argument("--config","-c",default ="config/config.yaml")
    args.add_argument("--params","-p",default ="params.yaml")
    parsed_args = args.parse_args()

    train(config_path = parsed_args.config,params_path = parsed_args.params)