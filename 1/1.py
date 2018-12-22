if __name__ == '__main__':
    input_path = "1.in"
    freq_shift = 0
    with open(input_path, 'r') as f:
        for line in f:
            freq_shift += int(line)
    print(freq_shift)