# author: s-kline
# extracts and saves reaction time data from presentation logfiles


def get_times(directory, namestr):
    '''
    :param directory: a string. full path to were all the rating files are saved
    :param namestr: a string. used to identify files
    :return: agg_dict: a list containing the rating dicts of all subjects
    :return: itemlist: a list containing the item names i.e. the keys of each subject dict
    '''
    import os

    trial_files = []
    agg_dict = []

    all_files = os.listdir(directory)

    trial_files = [item for item in all_files if namestr in item]
    trial_files.sort()

    #
    # for item in all_files:
    #     if namestr in item:
    #         trial_files.append(item)
    # trial_files.sort()

    print(trial_files)

    # input is list of textfiles

    conds = {'5': 'p_win', '6': 'p_loss', '7': 'n_win', '8': 'n_loss', '9': 'zero'}

    for txtfile in trial_files:
        vp_data = {} # individual vp data dictionary
        vp_data['vp_code'] = txtfile[7:10]
        trial_txtfile = open(directory + txtfile, 'r')
        trialdata = trial_txtfile.readlines()

        p_count = 1
        n_count = 1
        z_count = 1

        for line in trialdata:
            if trialdata.index(line) >= 1:
                cols = line.split('\t')
                if conds[cols[1]] == 'p_win' or 'p_loss':
                    vp_data['p_trial_' + str(p_count)] = int(cols[6]) - int(cols[5])
                    p_count += 1
                if conds[cols[1]] == 'n_win' or 'n_loss':
                    vp_data['n_trial_' + str(n_count)] = int(cols[6]) - int(cols[5])
                    n_count += 1
                if conds[cols[1]] == 'zero':
                    vp_data['zero_trial_' + str(z_count)] = int(cols[6]) - int(cols[5])
                    z_count += 1

        agg_dict.append(vp_data)
    itemlist = sorted(list(set(vp_data.keys())))
    # print(itemlist)
    # itemlist = [item for item in itemlist if 'neu' or 'sex' or 'bsp' in item]

    return agg_dict, itemlist

def get_times_from_log(directory, suffix):
    '''
    :param directory: a string. full path to were all the rating files are saved
    :param suffix: a string. used to identify files
    :return: agg_dict: a list containing the rating dicts of all subjects
    :return: itemlist: a list containing the item names i.e. the keys of each subject dict
    '''
    import os

    agg_dict = []
    all_files = os.listdir(directory)
    log_files = [item for item in all_files if item.endswith(suffix)]
    log_files.sort()

    for log in log_files:
        vp_data = {} # individual vp data dictionary
        vp_data['vp_code'] = log[0:3]
        logfile = open(directory + log, 'r')
        trialdata = logfile.readlines()

        onset_labels = []
        target_onsets = []
        response_onsets = []
        react_times = []
        conds = []

        p_counter = 1
        n_counter = 1
        z_counter = 1

        for line in trialdata:
            cols = line.split('\t')
            if len(cols) >= 4:
                if 'target' in cols[3]: # target stimulus was presented
                    if len(onset_labels) > 0 and onset_labels[-1] != 'Response': # if last entry is not a response, one is missing
                        onset_labels.append('missing response')
                        response_onsets.append(99)

                    event = cols[3] # get full event label: target_+ condition
                    onset_labels.append(event)  # append label
                    target_onsets.append(cols[4]) # onset of target stimulus
                    if 'p' in event:
                        conds.append(event[7:9] + str(p_counter).zfill(2))  # only 'p_' with running condition-specific number
                        p_counter += 1
                    elif 'n' in event:
                        conds.append(event[7:9] + str(n_counter).zfill(2))  # only 'n_' with running condition-specific number
                        n_counter += 1
                    elif '0' in event:
                        conds.append(event[7:9] + str(z_counter).zfill(2))  # only '0_' with running condition-specific number
                        z_counter += 1

                if cols[2] == 'Response' and len(onset_labels) > 0 : # response was recorded
                    if onset_labels[-1].startswith('target'):      # only include responses, that come right after a target
                        onset_labels.append(cols[2])
                        response_onsets.append(cols[4])

        # calculate reaction times
        for i in range(len(response_onsets)):
            if response_onsets[i] == 99:
                time = 99
            else:
                time = (int(response_onsets[i]) - int(target_onsets[i]))/ 10
            react_times.append(time) # reaction times in milliseconds

        # check stuff: #

        # print('VP:', vp_data['vp_code'])
        # for thing in onset_labels:
        #    print(thing)
        # print(len(conds), '\n', len(target_onsets), '\n', len(response_onsets))
        # print(target_onsets, '\n', response_onsets, '\n', conds, '\n', react_times, '\n')


        # fill vp_data dicts with stimuli onsets and calculated reaction times
        for j in range(len(target_onsets)):
            cond = conds[j]
            vp_data['target_onset_' + cond] = target_onsets[j]
            vp_data['response_onset_' + cond] = response_onsets[j]
            vp_data['react_time_' + cond] = react_times[j]

        agg_dict.append(vp_data)

    itemlist = sorted(list(set(vp_data.keys())))
    return agg_dict, itemlist


def save_times(data, vars, destination):
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
                # print(key, dataset[key])
                resultsfile.write('\t' + str(dataset[key]))
            else:
                resultsfile.write('\t' + '99')
    return

path = 'W:\\Stark\\0202RS\\Daten\\Auswertung_unsortiert\\Logfiles\\EPI_1\\'
name = '_trialdata'
# agg_data, headerlist = get_times(path, name)

suf = '.log'
agg_data, headerlist = get_times_from_log(path, suf)
print(agg_data)
print(headerlist)



savepath = 'W:\\Stark\\0202RS\\Daten\\Auswertung_unsortiert\\ausgelesen\\reacttimes_from_logs.txt'
save_times(agg_data, headerlist, savepath)