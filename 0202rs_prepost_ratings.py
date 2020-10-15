# author s-kline
# reads out pre-post experiment ratings from presentation logfiles


def get_all(directory, namestr):
    '''
    :param directory: a string. full path to were all the rating files are saved
    :param namestr: a string. used to identify files
    :return: agg_dict: a list containing the rating dicts of all subjects
    :return: itemlist: a list containing the item names i.e. the keys of each subject dict
    '''
    import os

    rating_files = []
    agg_dict = []

    all_files = os.listdir(directory)
    for item in all_files:
        if namestr in item:
            rating_files.append(item)
    rating_files.sort()
    # print(rating_files)

    # input is list of textfiles

    for txtfile in rating_files:
        vp_data = {} # individual vp data dictionary
        vp_data['vp_code'] = txtfile[7:10]
        rating_txtfile = open(directory + txtfile, 'r')
        ratingdata = rating_txtfile.readlines()
        pre_data = ratingdata[1].split('\t')
        post_data = ratingdata[2].split('\t')
        # print(pre_data, post_data)
        vp_data['pre_Sex_Erregung'] = pre_data[2]
        vp_data['post_Sex_Erregung'] = post_data[2]

        agg_dict.append(vp_data)
    itemlist = ['pre_Sex_Erregung', 'post_Sex_Erregung']

    # itemlist = sorted(list(set(vp_data.keys())))
    # itemlist = [item for item in itemlist if 'neu' or 'sex' or 'bsp' in item]

    return agg_dict, itemlist

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


path = 'W:\\Stark\\0202RS\\Daten\\Auswertung_unsortiert\\Logfiles\\EPI_1\\'
name = 'prepost_rating'
agg_data, headerlist = get_all(path, name)


savepath = 'W:\\Stark\\0202RS\\Daten\\Auswertung_unsortiert\\ausgelesen\\prepost_ratings.txt'
save_ratings(agg_data, headerlist, savepath)