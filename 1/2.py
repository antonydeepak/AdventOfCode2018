import sys

if __name__ == '__main__':
    input_path = "1.in"
    with open(input_path, 'r') as f:
        freq_shift = 0
        all_frequencies = set([freq_shift])

        while True:
            f.seek(0)
            for line in f:
                freq_shift += int(line)
                if freq_shift in all_frequencies:
                    print(freq_shift)
                    sys.exit(0)
                    break
                all_frequencies.add(freq_shift)