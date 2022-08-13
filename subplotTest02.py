# Multiple figures in a single window
# https://stackoverflow.com/questions/11159436/multiple-figures-in-a-single-window

import numpy as np

def save_image(data, ws=0.1, hs=0.1, sn='save_name'):
    import matplotlib.pyplot as plt
    m = n = int(np.sqrt(data.shape[0])) # (36, 1, 32, 32)

    fig, ax = plt.subplots(m,n, figsize=(m*6,n*6))
    ax = ax.ravel()
    for i in range(data.shape[0]):
        ax[i].matshow(data[i,0,:,:])
        ax[i].set_xticks([])
        ax[i].set_yticks([])

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9,
                        top=0.9, wspace=ws, hspace=hs)
    plt.tight_layout()
    plt.savefig('{}.png'.format(sn))


np.save("img_test.npy", np.array([[1, 2], [3, 4]]))  # new
data = np.load('img_test.npy')


save_image(data, ws=0.1, hs=0.1, sn='multiple_plot')
