import os
import ssdeep
import numpy as np
import json

def calculate_hashes(directory):
    hashes = {}
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            data = f.read()
            hash_value = ssdeep.hash(data)
            hashes[filename] = hash_value
    return hashes


def calculate_similarity_matrix(hashes):
    files = list(hashes.keys())
    size = len(files)
    similarity_matrix = np.zeros((size, size), dtype=int)
    
    for i in range(size):
        for j in range(i + 1, size):
            similarity = ssdeep.compare(hashes[files[i]], hashes[files[j]])
            similarity_matrix[i][j] = similarity
            similarity_matrix[j][i] = similarity  # 对称矩阵

    return similarity_matrix, files


def calculate_average_similarity(group, similarity_matrix, files):
    indices = [files.index(file) for file in group]
    avg_similarities = {}
    
    for i, file in enumerate(indices):
        total_similarity = np.sum(similarity_matrix[file, indices])  # 计算与组内其他文件的相似度总和
        count = len(indices) - 1  # 不包括自己
        avg_similarities[group[i]] = total_similarity / count if count > 0 else 0

    representative = max(avg_similarities, key=avg_similarities.get)
    return representative


def group_files(hashes, threshold):
    groups = []
    representatives = {}

    similarity_matrix, files = calculate_similarity_matrix(hashes)

    for filename, hash_value in hashes.items():
        found_group = False
        for i, group in enumerate(groups):
            representative = representatives[group[0]]
            rep_index = files.index(representative)
            new_index = files.index(filename)
            similarity = similarity_matrix[rep_index][new_index]

            if similarity >= threshold:
                group.append(filename)
                found_group = True
                
                # 更新代表性文件
                representatives[group[0]] = calculate_average_similarity(group, similarity_matrix, files)
                break
        
        if not found_group:
            groups.append([filename])  # Create a new group
            representatives[filename] = filename  # 新建组时，代表文件为自身

    return groups, representatives

def save_groups_to_file(groups, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, group in enumerate(groups):
            f.write(f"Group {i + 1}: {', '.join(group)}\n")


def save_groups_to_json(groups, representatives, output_file):
    results = []
    for i, group in enumerate(groups):
        representative = representatives[group[0]]
        results.append({
            "group_number": i + 1,
            "files": group,
            "representative": representative
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def main(directory, threshold, output_file):
    for folder_program in os.listdir(directory):
        program_path = os.path.join(directory, folder_program)
        assemble_path = os.path.join(program_path, 'assemble')
        criterion_path = os.path.join(program_path, 'criterion')
        slices_path = os.path.join(program_path, 'slice')
        traces_path = os.path.join(program_path, 'first_trace')
        generalize_path = os.path.join(program_path, 'generalized')
        group_path = os.path.join(program_path, output_file)

        os.makedirs(assemble_path, exist_ok=True)
        os.makedirs(criterion_path, exist_ok=True)
        os.makedirs(slices_path, exist_ok=True)
        os.makedirs(traces_path, exist_ok=True)
        os.makedirs(generalize_path, exist_ok=True)

        hashes = calculate_hashes(generalize_path)
        groups, representatives = group_files(hashes, threshold)
        save_groups_to_json(groups, representatives, group_path)


if __name__ == "__main__":
    dir_path = '/home/fuzz/Desktop/group/generalized' 
    similarity_threshold = 60  # 相似度阈值，0-100之间
    output_file = 'group_results.json'  
    main(dir_path, similarity_threshold, output_file)

