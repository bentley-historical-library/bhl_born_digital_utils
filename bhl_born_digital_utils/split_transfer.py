import os
import shutil


def split_transfer(transfer_dir, transfer_name, split_size):
    item_to_count = {}
    for dirname in os.listdir(transfer_dir):
        item_dir = os.path.join(transfer_dir, dirname)
        if os.path.isdir(item_dir):
            item_count = 0
            for _, _, filenames in os.walk(item_dir):
                item_count += len(filenames)
            item_to_count[dirname] = item_count
    total_count = sum([count for item, count in item_to_count.items()])
    if total_count > split_size:
        chunks = []
        sorted_items = sorted(item_to_count, key=item_to_count.get)
        current_chunk_size = 0
        current_chunk = []
        for sorted_item in sorted_items:
            item_count = item_to_count[sorted_item]
            if (current_chunk_size + item_count) > split_size:
                chunks.append(current_chunk)
                current_chunk_size = 0
                current_chunk = []
            current_chunk_size += item_count
            current_chunk.append(sorted_item)
        chunks.append(current_chunk)
        for i, chunk in enumerate(chunks):
            chunk_dirname = "{}-{:03d}".format(transfer_name, i+1)
            chunk_dirpath = os.path.join(transfer_dir, chunk_dirname)
            os.makedirs(chunk_dirpath)
            for item in chunk:
                item_dir = os.path.join(transfer_dir, item)
                shutil.move(item_dir, chunk_dirpath)
            print("Moved {} into {}".format(", ".join(chunk), chunk_dirpath))
    else:
        print("Transfer size is fewer than {} files".format(split_size))
