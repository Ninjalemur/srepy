import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#gives stacked plots with pattern change on stack

# make up some fake data
pos_mut_pcts = np.array([20, 10, 5, 7.5, 30, 50])
pos_cna_pcts = np.array([10, 0, 0, 7.5, 10, 0])
pos_both_pcts = np.array([10, 0, 0, 0, 0, 0])
neg_mut_pcts = np.array([10, 30, 5, 0, 10, 25])
neg_cna_pcts = np.array([5, 0, 7.5, 0, 0, 10])
neg_both_pcts = np.array([0, 0, 0, 0, 0, 10])
genes = ['PIK3CA', 'PTEN', 'CDKN2A', 'FBXW7', 'KRAS', 'TP53']

with sns.axes_style("white"):
    sns.set_style("ticks")
    sns.set_context("talk")
    
    # plot details
    bar_width = 0.35
    epsilon = .015
    line_width = 1
    opacity = 0.7
    pos_bar_positions = np.arange(len(pos_mut_pcts))
    neg_bar_positions = pos_bar_positions + bar_width

    # make bar plots
    hpv_pos_mut_bar = plt.bar(pos_bar_positions, pos_mut_pcts, bar_width,
			      color='#ED0020',
			      label='HPV+ Mutations')
    hpv_pos_cna_bar = plt.bar(pos_bar_positions, pos_cna_pcts, bar_width-epsilon,
			      bottom=pos_mut_pcts,
			      alpha=opacity,
			      color='white',
			      edgecolor='#ED0020',
			      linewidth=line_width,
			      hatch='//',
			      label='HPV+ CNA')
    hpv_pos_both_bar = plt.bar(pos_bar_positions, pos_both_pcts, bar_width-epsilon,
			       bottom=pos_cna_pcts+pos_mut_pcts,
			       alpha=opacity,
			       color='white',
			       edgecolor='#ED0020',
			       linewidth=line_width,
			       hatch='0',
			       label='HPV+ Both')
    hpv_neg_mut_bar = plt.bar(neg_bar_positions, neg_mut_pcts, bar_width,
			      color='#0000DD',
			      label='HPV- Mutations')
    hpv_neg_cna_bar = plt.bar(neg_bar_positions, neg_cna_pcts, bar_width-epsilon,
			      bottom=neg_mut_pcts,
			      color="white",
			      hatch='//',
			      edgecolor='#0000DD',
			      ecolor="#0000DD",
			      linewidth=line_width,
			      label='HPV- CNA')
    hpv_neg_both_bar = plt.bar(neg_bar_positions, neg_both_pcts, bar_width-epsilon,
			       bottom=neg_cna_pcts+neg_mut_pcts,
			       color="white",
			       hatch='0',
			       edgecolor='#0000DD',
			       ecolor="#0000DD",
			       linewidth=line_width,
			       label='HPV- Both')
    plt.xticks(neg_bar_positions, genes, rotation=45)
    plt.ylabel('Percentage of Samples')
    #plt.legend(loc='best')
    #sns.despine()
    plt.legend(bbox_to_anchor=(1.1, 1.05))  
    sns.despine()  
    plt.show()


