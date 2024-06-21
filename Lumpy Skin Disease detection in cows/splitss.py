import splitfolders
data_path='./dataset'

splitfolders.ratio(data_path, output="split_data",
    seed=1337, ratio=(.9, 0.1), group_prefix=None, move=False)
