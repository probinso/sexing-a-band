import csv 
from collections import defaultdict

def word_decade_dict_builder():
    output_dict = defaultdict()

    with open("./data/only_tfidf_output.csv") as fd:
        for line in csv.reader(fd):
            decade = int(line[2])
            document = map(lambda s: map(float, str.split(s, ':')), line[3:])

            for item in document:
                if item[0] in output_dict:
                    if output_dict[item[0]] > decade:
                        output_dict[item[0]] = decade
                    else:
                        continue 
                else:
                    output_dict[int(item[0])] = decade

        print(output_dict)
        return output_dict


if __name__ == '__main__':
    word_decade_dict_builder()

