#!/usr/bin/env python
# coding: utf-8
from config import debug, selected_neuron, disable_gpu_for_tensorflow, stored_models, selected_model, background_images_path, residuals_path, covariates_file

import pandas as pd
import pickle, os, h5py
import numpy as np
from pandas import DataFrame

import tensorflow as tf
import logging
from keras.models import load_model

from sklearn.model_selection import train_test_split
from keras.utils import to_categorical

import innvestigate
import innvestigate.utils as iutils
from matplotlib import pyplot as plt

import scipy
import nibabel as nib

if debug:
    print("stored_models = ")
    print(stored_models)
    print("selected_model = ")
    print(selected_model)


# In[1]:

# Import covariate data from file
df = pd.read_pickle(covariates_file)
#print(df)
sid = df['RID']
grp = df['Group at scan date (1=CN, 2=EMCI, 3=LMCI, 4=AD, 5=SMC)']
age = df['Age at scan']
sex = df['Sex (1=female)']
tiv = df['TIV']
field = df['MRI_Field_Strength']
grpbin = (grp > 1) # 1=CN, ...


# In[3]:

# Load matched covariate information
with open('matched_cov_idx.pkl', 'rb') as cov_idx_file:
    # read the data as binary data stream
    cov_idx = pickle.load(cov_idx_file)

labels = pd.DataFrame({'Group':grpbin}).iloc[cov_idx, :]
grps = pd.DataFrame({'Group':grp, 'RID':sid}).iloc[cov_idx, :]


# In[4]:

# Load residualized data from disk
hf = h5py.File(residuals_path, 'r')
hf.keys # read keys
model_input_images = np.array(hf.get('images')) # note: was of data frame type before
hf.close()
if debug:
    print("model_input_images.shape=")
    print(model_input_images.shape)


# In[5]:

# specify version of tensorflow
#%tensorflow_version 1.x
#%tensorflow_version 2.x
logging.getLogger('tensorflow').disabled=True #disable tensorflow deprecation warnings
if debug:
    print("Tensorflow version:")
    print(tf.__version__)
#from keras.backend.tensorflow_backend import set_session
#config = tf.ConfigProto(
#    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1)
    # device_count = {'GPU': 1}
#)
#config.gpu_options.allow_growth = True
#session = tf.Session(config=config)
#set_session(session)

if disable_gpu_for_tensorflow:
    if debug: print ("Disabling GPU computation for Tensorflow...")
    os.environ["CUDA_VISIBLE_DEVICES"]="-1" #disable GPU computation for tensorflow (https://stackoverflow.com/questions/37660312/how-to-run-tensorflow-on-cpu)


# In[5]:

# Split data into training/validation and holdout test data
labels = to_categorical(np.asarray(labels))
# circumvent duplicate data
idx = np.asarray(range(len(cov_idx)))
#train_idX,test_idX,train_Y,test_Y = train_test_split(idx, labels, test_size=0.1, stratify = labels, random_state=1)
test_idX = idx # select all
testgrps = grps #.iloc[test_idX, :]
print(testgrps) # prints diagnosis and RID
print('Distribution of diagnoses in data: [1=CN, 3=LMCI, 4=AD]')
print(testgrps.Group.value_counts())


# In[6]:

test_images = model_input_images[test_idX, :]
del model_input_images


# In[7]:

testgrps["Group"] = testgrps["Group"].map({1:"CN", 3:"MCI", 4:"AD"})
Option_grps = np.array(testgrps)
Option_grps = Option_grps.astype('str')
Opt_grp = []

for i in range(len(Option_grps)):
    Opt_grp.append(' - ID '.join(Option_grps[i]))

#https://stackoverflow.com/questions/48279640/sort-a-python-list-while-maintaining-its-elements-indices
Opt_grp = [(x, i) for (i, x) in enumerate(Opt_grp)]
Opt_grp  = sorted(Opt_grp)

def unzip(ls):
    if isinstance(ls, list):
        if not ls:
            return [], []
        else:
            Opt_grp, ys = zip(*ls)

        return list(Opt_grp), list(ys)
    else:
        raise TypeError
sorted_xs, index_lst = unzip(Opt_grp)


# In[9]:

# Load original images (background) from disk
hf = h5py.File(background_images_path, 'r')
hf.keys # read keys
images_bg = np.array(hf.get('images'))
hf.close()
testdat_bg = images_bg[test_idX, :]
del images_bg

if debug:
    print('testdat_bg.shape=')
    print(testdat_bg.shape)


# In[11]:

# see https://github.com/albermax/innvestigate/blob/master/examples/notebooks/imagenet_compare_methods.ipynb for a list of alternative methods
methods = [ # tuple with method,     params,                  label
#            ("deconvnet",            {},                      "Deconvnet"),
#            ("guided_backprop",      {},                      "Guided Backprop"),
#            ("deep_taylor.bounded",  {"low": -1, "high": 1},  "DeepTaylor"),
#            ("input_t_gradient",     {},                      "Input * Gradient"),
#            ("lrp.z",                {},                      "LRP-Z"),
#            ("lrp.epsilon",          {"epsilon": 1},          "LRP-epsilon"),
            ("lrp.alpha_1_beta_0",   {"neuron_selection_mode":"index"},  "LRP-alpha1beta0"),
]

# Preload CNN models from disk
print("Preloading all " + str(len(stored_models)) + " models. This may take a while...")
model_dict = dict()
for model_path in stored_models:
    print("Loading " + model_path + "...")
    model_dict[model_path] = dict()
    model_dict[model_path]["mymodel"] = load_model(model_path)
    model_dict[model_path]["mymodel"].layers[-1].activation=tf.keras.activations.linear
    model_dict[model_path]["mymodel"].save('tmp_wo_softmax.hdf5')
    model_wo_softmax = load_model('tmp_wo_softmax.hdf5')
    os.remove('tmp_wo_softmax.hdf5')
    print("model_wo_softmax loaded.")
    print('Creating analyzer...')
    # create analyzer -> only one selected here!
    for method in methods:
        model_dict[model_path]["analyzer"] = innvestigate.create_analyzer(method[0], model_wo_softmax, **method[1])
    print('Analyzer created.')
# load atlas nifti data:
img = nib.load('aal/aal.nii')
img_drawn = nib.load('aal/canny_regions_by_border.nii.gz')
aal_drawn = img_drawn.get_fdata()
#aal = np.array(img.dataobj)
x_range_from = 10; x_range_to = 110 #sagittal
y_range_from = 10; y_range_to = 130 #coronal
z_range_from = 5; z_range_to = 105 #axial
aal = img.get_fdata()[x_range_from:x_range_to, y_range_from:y_range_to, z_range_from:z_range_to]
aal = np.transpose(aal, (2, 0, 1)) # reorder dimensions to match coronal view z*x*y in MRIcron etc.
aal = np.flip(aal, (1,2)) # flip coronal and sagittal dimension


# aal is now [axial,sagittal,coronal]
if debug:
    print("aal.shape = ")
    print(aal.shape)

# load region names to array
# region name with id 'i' is stored at index 'i'
aal_region_names = np.genfromtxt('aal/aal.csv', delimiter=';', usecols=(2), dtype = str, skip_header=1)


def get_region_ID(axi, sag, cor):
    return(aal[axi, sag, cor])

def get_region_name(axi, sag, cor):
    return(aal_region_names[int(aal[axi, sag, cor])])


class Model():
    
    def set_model(self, new_model_name):
        if debug: print("Called set_model().")
        
        global methods
        self.selected_model = new_model_name
        self.mymodel = model_dict[self.selected_model]["mymodel"]
        #model_wo_softmax = model_dict[selected_model]["model_wo_softmax"]
        self.analyzer = model_dict[self.selected_model]["analyzer"]
        print('Model loaded.')
    
        # callback for a new subject being selected
    def set_subject(self, subj_id):
        if (debug): print("Called set_subject().")

        #global subj_bg, subj_img, pred, relevance_map # define global variables to store subject data
        self.subj_img = test_images[subj_id]
        self.subj_img = np.reshape(self.subj_img, (1,)+ self.subj_img.shape) # add first subj index again to mimic original array structure
        self.subj_bg = testdat_bg[subj_id, :,:,:, 0]
        # evaluate/predict diag for selected subject
        self.pred = (self.mymodel.predict(self.subj_img)[0,1]*100) # scale probability score to percent
        # derive relevance map from CNN model
        self.relevance_map = self.analyzer.analyze(self.subj_img, neuron_selection=selected_neuron)
        self.relevance_map = np.reshape(self.relevance_map, self.subj_img.shape[1:4]) # drop first index again
        self.relevance_map = scipy.ndimage.filters.gaussian_filter(self.relevance_map, sigma=0.8) # smooth activity image
        # perform intensity normalization
        scale = np.quantile(np.absolute(self.relevance_map), 0.99)
        if scale!=0: # fallback if quantile returns zero: directly use abs max instead
            #scale = max(-np.amin(a), np.amax(a))
            self.relevance_map = (self.relevance_map/scale) # rescale range
        clipping_threshold = 3 # max value to be plotted, larger values will be set to this value;
                                # corresponding to vmax in plt.imshow; vmin=-vmax used here
                                # value derived empirically here from the histogram of relevance maps
        self.relevance_map[self.relevance_map > clipping_threshold] = clipping_threshold # clipping of positive values
        self.relevance_map[self.relevance_map < -clipping_threshold] = -clipping_threshold # clipping of negative values
        self.relevance_map = self.relevance_map/clipping_threshold # final range: -1 to 1 float
        #print(np.max(relevance_map), np.min(relevance_map))
        # returns values by modifying global variables: self.subj_bg, self.subj_img, self.pred, self.relevance_map
        return
        
    def __init__(self):
        if debug: print("Initializing new datamodel object...")
        #load selected model data from dictionary:
        self.mymodel = model_dict[selected_model]["mymodel"]
        #model_wo_softmax = model_dict[selected_model]["model_wo_softmax"]
        self.analyzer = model_dict[selected_model]["analyzer"]

        # Call once to initialize first image and variables
        self.set_subject(index_lst[0]) # invoke with first subject
