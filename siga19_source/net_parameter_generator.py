import numpy as np
import math

origin_param_dim = 7+3+1
epsilon = 1e-3
param_bounds={}
param_bounds["n"] = (epsilon,1.0-epsilon)
param_bounds["theta"] = (0.0,math.pi)
param_bounds["a"] = (0.006,0.503)
param_bounds["pd"] = (0.0,1.0)
param_bounds["ps"] = (0.0,10.0)
param_bounds["box"] = (-50.0,50.0)
param_bounds["angle"] = (0.0,2.0*math.pi)

class Net_Parameter_Generator:
    def __init__(self,train_configs,name):
        self.record_size = origin_param_dim*4
        self.batch_size = train_configs["batch_size"]
        self.buffer_size = train_configs["pre_load_buffer_size"]

        self.name = name
        if self.name == "train":
            self.pf_train = open(train_configs["data_root"]+"cooked_params_train.bin","rb")
        elif self.name == "val":
            self.pf_train = open(train_configs["data_root"]+"cooked_params_val.bin","rb")
            self.buffer_size = 100000

        self.pf_train.seek(0,2)
        self.train_data_size = self.pf_train.tell()//4//origin_param_dim

        assert self.train_data_size > 0

        print("[MINE]"+self.name+" train data size:",self.train_data_size)

        self.available_train_idx = list(range(self.train_data_size))

        self.train_ptr = 0

        self.__refresh_train()
        self.__preload()

    def __preload(self):
        print(self.name+" preloading...")
        tmp_params_idxes = self.available_train_idx[self.train_ptr:self.train_ptr+self.buffer_size]
        if len(tmp_params_idxes) == 0:
            self.__refresh_train()
            tmp_params_idxes = self.available_train_idx[self.train_ptr:self.train_ptr+self.buffer_size]
        self.train_ptr+=len(tmp_params_idxes)

        tmp_map = {tmp_params_idxes[i]:i for i in range(len(tmp_params_idxes))}

        tmp_params_idxes.sort()

        self.buffer_params = np.zeros([len(tmp_params_idxes),origin_param_dim],np.float32)
        for idx in range(len(tmp_params_idxes)):
            self.pf_train.seek(tmp_params_idxes[idx]*self.record_size,0)
            self.buffer_params[tmp_map[tmp_params_idxes[idx]]] = np.fromfile(self.pf_train,np.float32,origin_param_dim)
        
        self.current_ptr = 0

        print(self.name+" done.")

    def __refresh_train(self):
        print(self.name+" refreshing train...")
        np.random.shuffle(self.available_train_idx)
        self.train_ptr = 0
        print(self.name+" done.")

    def __rejection_sampling_axay(self):
        origin = np.exp(np.random.uniform(np.log(param_bounds["a"][0]),np.log(param_bounds["a"][1]),[self.batch_size,2]))
        # origin = np.where(origin[:,[0]]>origin[:,[1]],origin,origin[:,::-1])
        while True:
            still_need = np.logical_and(origin[:,0]>0.35,origin[:,1] >0.35)
            where = np.nonzero(still_need)
            num = where[0].shape[0]
            if num == 0:
                break
            new_data= np.exp(np.random.uniform(np.log(param_bounds["a"][0]),np.log(param_bounds["a"][1]),[num,2]))
            # new_data = np.where(new_data[:,[0]]>new_data[:,[1]],new_data,new_data[:,::-1])
            origin[where] = new_data
        return origin

    def generate_training_data(self):
        tmp_params = self.buffer_params[self.current_ptr:self.current_ptr+self.batch_size]
        if tmp_params.shape[0] < self.batch_size:
            self.__preload()
            tmp_params = self.buffer_params[self.current_ptr:self.current_ptr+self.batch_size]
        self.current_ptr+=self.batch_size

        tmp_params[:,6:8] = self.__rejection_sampling_axay()

        return (tmp_params[:,3:-1],tmp_params[:,:3],tmp_params[:,[-1]])

    def generate_validating_data(self):
        return self.generate_training_data()
