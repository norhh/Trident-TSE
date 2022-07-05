import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import json



with open('/home/Trident/eval/data/codeflaws_path.json') as json_file:
    data = json.load(json_file)

classes = ["SISA", "DRWV", "DMAA", "ORRN", "OILN", "OAIS"]
# FIXME: I do not know what this variable means:
side_effect_classes = []

fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(8.5, 3))
np.random.seed(19680801)

data_keys = []
data_values = []
for clas in classes:
    data_values += [data["TP"][clas], data["AKN"][clas], data["AKP"][clas]]
    if clas in side_effect_classes:
        clas = clas[:-1]
    data_keys += [clas + "\nTP", clas + "\nAKN", clas + "\nAKP"]

# plot violin plot
parts = axs.violinplot(data_values,
                        showmeans=False,
                        showmedians=True)
i = 0
color = ['red', 'green', 'blue']
for partname in ('cbars','cmins','cmaxes','cmedians'):
    vp = parts[partname]
    vp.set_edgecolor('black')
    vp.set_linewidth(1)
for pc in parts['bodies']:
    pc.set_color(color[i%3])
    pc.set_edgecolor(color[i%3])
    pc.set_linewidth(1)
    i+=1
#axs.set_title('Violin plot')
axs.yaxis.grid(True)
axs.set_xticks([y + 1 for y in range(len(data_values))])
axs.set_xlabel('')
axs.set_ylabel('Path count')
for item in ([axs.title, axs.xaxis.label, axs.yaxis.label] +
                axs.get_xticklabels() + axs.get_yticklabels()):
    item.set_fontsize(7)

# add x-tick labels
plt.setp(axs, xticks=[y + 1 for y in range(len(data_values))],
            xticklabels=data_keys)
plt.savefig('codeflaws_paths.png')

