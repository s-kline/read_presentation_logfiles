# author: s-kline
# gets videoratings from post-scan presentation task.
# sorts them in the order that videos were presented for each subject
# saves them in matlab struct variables to be able to use them in SPM fMRI parametric modulation analysis


import os

# functions for getting and saving rating data:

# gets rating data from files and aggregates in dict
def get_ratings(directory, suffix):
    ''' 
    :param directory: a string. full path to were all the rating files are saved
    :param suffix: a string. suffix used to identify rating files: e.g. '.txt' if u don't want the .log files
    :return: agg_dict: a list containing the rating dicts of all subjects
    :return: itemlist: a list containing the item names i.e. the keys of each subject dict
    '''
    import os

    rating_files = []
    agg_dict = []

    all_files = os.listdir(directory)
    for item in all_files:
        if item.endswith(suffix):
            rating_files.append(item)
    rating_files.sort()

    # input is list of textfiles
    for txtfile in rating_files:
        vp_data = {}
        vp_data['vp_code'] = txtfile[8:11]
        rating_txtfile = open(base_dir + txtfile, 'r')
        ratingdata = rating_txtfile.readlines()

        for line in ratingdata:
            columns = line.split('\t')
            if len(columns) > 3:
                if columns[0].startswith('bsp') or columns[0].startswith('sex') or columns[0].startswith('neu'): #or 'Valenz' or 'Sex_Erregung' in columns[1]:
                    video = columns[0]
                    scale = columns[1]
                    rating = columns[2]
                    vp_data[video + '_' + scale] = rating
                # elif
        agg_dict.append(vp_data)

    itemlist = sorted(list(set(vp_data.keys())))
    itemlist = [item for item in itemlist if 'neu' or 'sex' or 'bsp' in item]
    return agg_dict, itemlist

# takes rating data from get_ratings() and writes a txt file for use in excel or spss
def save_ratings(data, vars, destination):
    '''
    :param data: list of aggregated data dicts
    :param vars: list of variables (keys in data_dicts)
    :param destination: a string. txtfile with full path where the data should be saved
    :return: nothing. saves a txtfile with the data in the specified destination
    '''
    resultsfile = (open(destination, 'a+'))
    resultsfile.write('VP_Code\t' + '\t'.join(vars))
    for dataset in data:
        # print(dataset)
        resultsfile.write('\n' + dataset['vp_code'])
        for key in vars:
            if key in dataset:
                resultsfile.write('\t' + dataset[key])
            else:
                resultsfile.write('\t' + '99')
    return

# gets order of presentation from presentation logfiles
def present_order(path):
    '''
    :param path: a string. full path to were all the MRI presentation logfiles are saved
    :return: dict of video presentation order lists with VPs as keys.
    '''
    logs = [i for i in os.listdir(path) if i.endswith('trialdata.txt')]
    order_dict = {} # will contain presentation order

    # which video was presented when?
    for log in logs:
        p_vids = []
        vp = log[7:10]
        logfile = open(path + log)
        lines = logfile.readlines()
        for line in lines:
            cols = line.split('\t')
            if cols[1] == '5': # 5 is code for VSS-delivery trial
                p_vids.append(cols[8]) # video numbers are in this column
        order_dict[vp] = p_vids
    return order_dict

# takes presentation order and ratings from agg_data to make pmod lists sorted in dict by VPs as key
def make_pmod_dict(agg_dict, order_dict, scale):
    '''
    :param agg_dict: rating dict created by get_ratings()
    :param order_dict: order dict created by present_order()
    :param scale: string representing the variable suffix: _Valenz or _Sex_Erregung
    :return: pmod dict
    '''
    pmod_dict = {} # will contain valence ratings sorted by presentation order
    for subject in order_dict:
        pmod_list = []
        order = order_dict[subject]
        rats = [item for item in agg_dict if item["vp_code"] == subject]
        if rats: ratsdict = rats[0]
        for vidnum in order:
            if vidnum != '0': # only actually delivered videos, skip losses
                varname = 'sex_' + (vidnum).zfill(3) + scale
                try:
                    pmod_list.append(ratsdict[varname])
                except:
                    print(Exception)
                    print(subject)


        pmod_dict[subject] = pmod_list
    return pmod_dict

# saves the pmod lists as structs in mat files to merge with cond files
def pmod_savestruct(path, vp, params, name):
    '''
    :param path: a string. full path to save directory pmod structs
    :param vp: a string. vp code for filename to save
    :param params: a list. containing the pmods in correct order
    :param name: a string. name of the pmod in the struct files
    :return: nothing. saves the pmods as structs in mat files.
    '''

    import numpy as np
    from numpy.core.records import fromarrays
    from scipy import io as sio  # relevant to save variables as .mat-files

    savename = path + '0202rs-' + vp + 'py_pmod_struct.mat'

    p_val_params = [float(item) for item in params] # results in matlab datatype "double", needed for spm

    cell_p_val_params = np.empty(1, dtype=np.object) # first create empty 1x1 np array
    cell_p_val_params[0] = p_val_params # fill only array spot with python list

    name = [[],[],[], [name]]
    param = [[], [], [], cell_p_val_params]
    poly = [[], [], [], [float(1)]] # also needs to be "double" for spm to take it

    # list of np.arrays with dtype=object becomes cell array in matlab
    name = [np.array(item, dtype=object) for item in name]
    # param = [np.array(item, dtype=object) for item in param]
    poly = [np.array(item, dtype=object) for item in poly]


    pmod_rec = fromarrays([name, param, poly], names=['name', 'param', 'poly'])
    sio.savemat(savename, {'pmod': pmod_rec})
    return



### read out ratings
base_dir = 'W:\\Stark\\0202RS\\Daten\\Auswertung_unsortiert\\Videoratings\\'
agg_data, headerlist = get_ratings(base_dir, '.txt')

### get ratings in order of presentation
# log_path = 'W:\\Stark\\0202RS\\Daten\\Auswertung_unsortiert\\Logfiles\\EPI_1\\'
# pres_order_dict = present_order(log_path)

# pmods = make_pmod_dict(agg_data, pres_order_dict, '_Sex_Erregung')


### save structs for all vps
# save_dir = 'Y:\\0202RS\\work\\auswertung\\flevel_SID\\SID_logs_converted_sex_arousalPmod_model03\\'
# for vp_id in pmods:
#      pmod_savestruct(save_dir, vp_id, pmods[vp_id], 'p_sexarousal')


### make rating results file for behavioral analysis

# results = 'W:\\Stark\\0202RS\\Daten\\Auswertung_unsortiert\\ausgelesen\\rating_results.txt'
# save_ratings(agg_data, headerlist, results)


### convert_to_dataframe for easy plotting

import pandas as pd
import re
import seaborn as sns
from matplotlib import pyplot as plt


rating_df = pd.DataFrame(agg_data)
# rating_df = rating_df.set_index('vp_code')

rating_df = rating_df.drop([0,1]) # drop the first two rows
variables = [col for col in rating_df.columns] # get list of columns/variables
rating_df = rating_df.drop(columns=[v for v in variables if v.startswith('bsp')]) # drop example videos

# group filtering

pmod_paper_N = [2,
                3,
                8,
                10,
                11,
                12,
                15,
                16,
                17,
                18,
                24,
                26,
                27,
                28,
                31,
                33,
                37,
                38,
                39,
                41,
                43,
                45,
                46,
                47,
                48,
                52,
                53,
                54,
                57,
                59,
                60,
                61,
                62,
                64,
                65,
                67,
                70,
                71,
                73,
                74,
                75,
                77,
                81,
                82,
                88,
                91,
                92,
                # 96,
                99,
                100,
                101,
                102,
                104,
                105,
                106,
                107,
                111,
                115,
                119,
                122,
                123,
                124,
                125,
                129,
                133,
                135,
                138,
                141,
                143,
                144,
                158,
                162,
                164,]

# this drops all subject that are not in pmod_paper_N from further processing & plotting!
rating_df = rating_df.drop([sub for sub in rating_df.index if sub not in pmod_paper_N])

variables = [col for col in rating_df.columns]  # updated list of vars
stubs = list(set([re.sub('_Sex_Erregung|_Valenz', '', v) for v in variables if v != 'vp_code']))


tmp = pd.wide_to_long(rating_df,
                      stubnames=stubs,
                      i='vp_code',
                      j='rating_scale',
                      sep='_',
                      suffix='\\w+')

tmp.reset_index(inplace= True)
tmp['id'] = tmp.index
tmp.index = tmp['vp_code']

long_rdf = pd.wide_to_long(tmp,
                      stubnames=['sex', 'neu'],
                      i='id',
                      j='video_number',
                      sep='_')

long_rdf.reset_index(inplace=True)

long_rdf = long_rdf.dropna()
long_rdf['sexual'] = long_rdf['sex'].astype(int)
long_rdf['neutral'] = long_rdf['neu'].astype(int)

long_rdf['video_number'] = long_rdf['video_number'].astype(int)

### finally make the plots

sns.set(style='ticks')
sns.set_palette(sns.color_palette("hls", 2))

a4_dims = (12, 4)
fig, ax = plt.subplots(figsize=a4_dims)

plt.subplot(1, 2, 1)
plt.ylim(0, 9)
sexplot = sns.barplot(x='video_number',
             y='sexual',
             hue='rating_scale',
             errwidth=0.5,
             capsize=0.1,
             palette=sns.color_palette("hls", 2),
             data=long_rdf)
sl = sexplot.legend()
sl.set_title('rating scale')

new_labels = ['sexual arousal', 'valence']
for t, l in zip(sl.texts, new_labels): t.set_text(l)

sns.despine()

plt.subplot(1, 2, 2)
plt.ylim(0,9)
neuplot =sns.barplot(x='video_number',
             y='neutral',
             hue='rating_scale',
             errwidth=0.5,
             capsize=0.1,
             palette=sns.color_palette("hls", 2),
             data=long_rdf)
nl = neuplot.legend()
nl.set_title('rating scale')

new_labels = ['sexual arousal', 'valence']
for t, l in zip(nl.texts, new_labels): t.set_text(l)

sns.despine()

fig1 = plt.gcf()

plt.show()
plt.draw()
path = 'O:\\Klein\\0202rs\\Publikation\\'
# fig1.savefig(path + '0202rs_placebos_pmod_videoratings.png', dpi=100)

# optional sex-only plot

# longer_rdf = long_rdf.drop(['sex', 'neu'], axis='columns')
# longer_rdf = pd.melt(longer_rdf,
#                      id_vars=['id', 'video_number', 'vp_code', 'rating_scale'],
#                      var_name='video category',
#                      value_name='rating')
#
# sns.catplot(x='video_number',
#             y='rating',
#             hue='video category',
#             data=longer_rdf,
#             kind='bar',
#             errwidth=0.5,
#             capsize=0.1,
#             #style='rating_scale',
#             )
# plt.show()