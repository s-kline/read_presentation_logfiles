# author: s-kline
# imports video ratings and extracted fMRI beta weights from excel. 
# Makes scatterplots for paper 

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data_file = 'Y:\\0202RS\\work\\Daten\\ausgelesen\\videoratings\\ICBA_videoratings.xlsx'
rat_data = pd.read_excel(data_file, index_col=0)


rat_data = rat_data[rat_data < 99] # filter out missings represented by 99 in the xlsx
rat_data.dropna(how='any')

rat_transp = rat_data.transpose()

vars = rat_data.columns.values
descrip = rat_data.describe()

sexvids = rat_data.loc[:, vars[46:-1]] # label-based indexing
neuvids = rat_data.loc[:, vars[4:46]]

sex_transp = rat_transp.iloc[47:-1,:]
neu_transp = rat_transp.iloc[4:46,:]

sex_valenz = sexvids.loc[:, [label for label in sexvids.columns.values if 'Valenz' in label]] # index-based indexing
sex_arousal = sexvids.loc[:, [label for label in sexvids.columns.values if 'Erregung' in label]]

sex_transp_valenz = sex_transp.loc[[label for label in sex_transp.index.values if 'Valenz' in label], :]
sex_transp_arousal = sex_transp.loc[[label for label in sex_transp.index.values if 'Erregung' in label], :]


# correlations heatmap
subset = sex_valenz
corr = subset.corr()
sns.set(font_scale=0.75)
ax = sns.heatmap(
    corr,
    vmin=-1, vmax=1, center=0, # correlation scale goes from -1 to 1
    cmap ='spring', # colormap
    square=True,
    xticklabels= subset.columns.values,
    yticklabels= subset.columns.values
)
# plt.show()
plt.close()

betas_file = 'Y:\\0202RS\\work\\auswertung\\x_results\\pmod_sexual_arousal\\extractvals\\Delivery_pornoXsexarousal_rat_placebos.xls'
betas_data = pd.read_excel(betas_file, index_col=0, sheet_name=3)


axlabels = ['beta of Delivery' + r'$_\mathrm{VSS}$' + ' modulation by sexual arousal (-8/12/-4)',
            'beta of Delivery' + r'$_\mathrm{VSS}$' + ' modulation by sexual arousal (-12/-6/18)',
            'beta of Delivery' + r'$_\mathrm{VSS}$' + ' modulation by sexual arousal (14/-8/20)'
            ]
# make scatterplot for each ROI with IAt score

sns.set(style="ticks",
        color_codes=True
        )
sns.set_context('paper', font_scale=1.7)
sns.set_palette('Blues_d')

i = 0
for col in betas_data.columns.values:
    if col == 's-IATsex': break
    roi_betas = betas_data.loc[:, col]
    iat_score = betas_data.loc[:, 's-IATsex']

    sns.jointplot(x= roi_betas,
                y= iat_score,
                kind='reg',
                marker= '.',
                scatter_kws={'s': 50},
                data=betas_data,
                space=0,
                height=7,
                ratio=4,
                truncate=False
                    )
    sns.despine()
    plt.margins(x=-0.05, y=-0.05)

    plt.xlabel(axlabels[i], fontsize=16)
    plt.ylabel('s-IATsex', fontsize=16)

    fig1 = plt.gcf()
    fig1.suptitle(col, y=1, fontsize=24)
    fig1.tight_layout(pad=0)
    plt.show()
    plt.draw()
    path = 'Y:\\0202RS\work\\auswertung\\x_results\\pmod_sexual_arousal\\extractvals\\'
    fig1.savefig(path + 'Scatterplot_' + col + '_IAT_sum_pmod_sexual_arousal.png', dpi=100)



    i += 1

