from common import *
import matplotlib.patches as mpatches


def draw_subfigure(ax, x_values, y_values, legend_labels, x_label, y_label=None,
               color_map=COLOR_MAP, patterns=PATTERNS):
    assert (len(legend_labels) >= len(y_values))

    # a cluster has stacks_num of bars, the length of each bar is width
    width = 0.2
    stacks_num = len(y_values)
    clusters_num = len(x_label)
    bars = [None] * stacks_num

    ## draw the bar
    for j in range(stacks_num):
        bars[j] = ax.bar(np.array(range(clusters_num)) + width*j*1.1, y_values[j], width=width,
               hatch=patterns[j], color=color_map[j], edgecolor="black")

    ## set format for axis
    ax.set_xticks(np.array(range(clusters_num)) + width * (stacks_num/2))
    ax.set_xticklabels(x_label)
    ax.set_yscale("log")
    #ax.set_yticklabels(y_label)

    # label times
    #for j in range(stacks_num):
    #    label_times(ax, bars[j], np.min(y_values, axis=0), y_values[j,:])


if __name__ == "__main__":
    data_folder = "data/comparison_baselines_data"
    data_filenames = ["com_youtube.txt", "wiki_talk.txt",
                      "wiki_topcats.txt", "soc_twitter.txt",
                      "soc_dogster.txt", "com_orkut.txt"]
    nrows = 3
    ncols = 2

    ## read in data
    data = []
    for data_filename in data_filenames:
        ret = read_file_universal(data_folder + "/" + data_filename)
        assert len(ret[0]) == 4
        methods_perf = np.array(ret).transpose()
        data.append(methods_perf)

    figs, axes = plt.subplots(nrows=nrows, ncols=ncols)

    # draw each subfigure
    x_labels = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8"]
    legend_labels = ["RPS", "GPSM", "REUSE_KV", "NEMO"]
    for i in range(nrows):
        for j in range(ncols):
            draw_subfigure(axes[i][j], None, data[i*ncols+j], legend_labels, x_labels, None)

    time_limit = 3600*3
    for i in range(nrows):
        for j in range(ncols):
            dataset_id = i*ncols + j
            reach_limit = False
            for methods_perf in data[dataset_id]:
                for perf in methods_perf:
                    if perf >= time_limit:
                        reach_limit = True
            if reach_limit:
                axes[i][j].set_ylim(ymax=time_limit)


    titles = ["YT", "WK", "TP", "TW", "DG", "OR"]
    for i in range(nrows):
        for j in range(ncols):
            axes[i][j].set_title(titles[i*ncols+j])

    # set common y label for subfigures in one row
    for i in range(nrows):
        axes[i][0].set_ylabel('Elapsed time (s)')

    # add the common legend
    add_legend(legend_labels)

    # adjust layout for multiple subfigures
    figs.tight_layout(rect=[-0.07, 0.03, 1, 1], h_pad=-0.5, w_pad=-1.3)
    figs.set_figheight(2.4 * 3)
    figs.set_figwidth(8 * 2)

    plt.savefig('plots/comparison_baselines.pdf')


