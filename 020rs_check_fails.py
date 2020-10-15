# author: s-kline
# checks if pre-specified experiemnt algorithm worked as it should
# gets data from presentation logfiles
# checks reinforcement rate and how long target was presented in each trial

### data on planned trials and what actually happens is saved in _trialdata.txt files
# 5 = PornoGewinn,
# 6 = PornoVerlust,
# 7 = NeutralGewinn,
# 8 = NeutralVerlust,
# 9 = NichtsTrial

# gucken, ob insgesamt die Gewinne in Pornotrials (5 oder 6 im logfile) die geplante Anzahl ergeben
# gucken, ob insgesamt die Gewinne in Neutraltrials (7 oder 8 im logfile) die geplante Anzhal ergeben

#read file, take header as dict keys and colums as lists for the keys
import os
trialdata_files = []
subjects_total = 0
few_p_reinforce = 0
few_n_reinforce = 0
many_p_reinforce = 0
many_n_reinforce = 0

resultsfile = open('Y:\\0202RS\\work\\Daten\\ausgelesen\\fail_results.txt', 'a+')

base_dir = 'Y:\\0202RS\\work\\Daten\\Logfiles\\EPI_1\\'
#base_dir = 'Y:\\0202RS\\work\\Daten\\pmod_sample_trialdata\\'
all_files = os.listdir(base_dir)
for txtfile in all_files:
    if 'trialdata' in txtfile:
        trialdata_files.append(txtfile)
trialdata_files.sort()

all_target_durs = []

for txtfile in trialdata_files:
    target_durs = []
    filename = txtfile
    p_trials_outcome = []
    n_trials_outcome = []

    trialdata_file = open (base_dir+filename, 'r')
    trialdata = trialdata_file.readlines()

    headerstring = trialdata[0]
    headers = headerstring.split('\t')

    for line in trialdata:
        content = line.split('\t')
        if content[2] == '5' or content[2] == '6':
            p_trials_outcome.append(int(content[3]))
        if content[2] == '7' or content[2] == '8':
            n_trials_outcome.append(int(content[3]))
    target_durs.append(int(content[4]))
    all_target_durs.append(int(content[4]))
    trialdata_file.close()

    p_reinforcement = sum(p_trials_outcome)
    n_reinforcement = sum(n_trials_outcome)
    if p_reinforcement != 15 or n_reinforcement != 15:
        if p_reinforcement < 15:
            few_p_reinforce += 1
        if p_reinforcement > 15:
            many_p_reinforce +=1

        if n_reinforcement < 15:
            few_n_reinforce += 1
        if n_reinforcement > 15:
            many_n_reinforce += 1
        print ('\n', txtfile)
        print ('number of reinforced porntrials: ' + str(p_reinforcement))
        print ('number of reinforced neutraltrials: ' + str(n_reinforcement))
    resultsfile.write('\n'+ txtfile + '\t' + str(p_reinforcement) + '\t' + str(n_reinforcement))

    subjects_total += 1

print ('\n', subjects_total, 'subjects in total')
print (str(few_p_reinforce) + ' won less sexual videos than planned')
print (str(many_p_reinforce) + ' won more sexual videos than planned')
print (str(few_n_reinforce) + ' won less neutral videos than planned')
print (str(many_n_reinforce) + ' won more neutral videos than planned')


print(sorted(all_target_durs))
print(min(all_target_durs), max(all_target_durs))
print(sum(all_target_durs)/len(all_target_durs))
resultsfile.close()