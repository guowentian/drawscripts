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

    ## draw the bars with breakdown
    for j in range(stacks_num):
        bars[j] = ax.bar(np.array(range(clusters_num)) + width*j*1.1, y_values[j], width=width,
               hatch=patterns[j], color=color_map[j], edgecolor="black")

    ## set format for axis
    ax.set_xticks(np.array(range(clusters_num)) + width * (stacks_num/2))
    ax.set_xticklabels(x_label)


if __name__ == "__main__":
    data_folder = "data"
    data_filenames = ["reuse_ratio.txt"]
    color_map = get_reorder_list(7, COLOR_MAP)
    patterns = get_reorder_list(4, PATTERNS)

    ## read in data
    data = []
    for data_filename in data_filenames:
        ret = read_file_universal(data_folder + "/" + data_filename)
        assert len(ret[0]) == 4
        datasets_ratios = np.array(ret).transpose()
        data.append(datasets_ratios)

    figs, axes = plt.subplots()

    x_labels = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8"]
    legend_labels = ["YT","WK", "AS","OR"]
    draw_subfigure(axes, None, data[0], legend_labels, x_labels, None, color_map=color_map, patterns=patterns)

    # set common y label for subfigures in one row
    axes.set_ylabel('Reuse ratio (%)')

    # add the common legend
    add_legend(legend_labels, color_map=color_map, patterns=patterns, fontsize=14)

    # adjust layout for multiple subfigures
    figs.tight_layout(rect=[0, 0.18, 1, 1])
    figs.set_figheight(2.4 * 1.1)
    figs.set_figwidth(1 * 7.5)

    plt.savefig('plots/reuse_ratio.pdf')


