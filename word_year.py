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

       
       # -----------------------------------------------------
        # year_breakdown = defaultdict(int)

        # for item in output_dict.items():
        #     year_breakdown[item[1]] += 1

        # print(year_breakdown)
        # -----------------------------------------------------
        # The results below show the counts of when words were first seen in our corpus by decade
        # {decade: count_of_words}
        # result ----> defaultdict(<type 'int'>, {2: 804, 3: 374, 4: 445, 
        #                           5: 1724, 6: 1192, 7: 447, 8: 14})

        return output_dict


if __name__ == '__main__':
    word_decade_dict_builder()

