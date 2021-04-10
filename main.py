import re
import csv
import operator
import itertools


def get_adapted_contents(contents):
    adapted_contents = []
    headers_commas = contents[0].count(',')
    for i, line in enumerate(contents):
        if line.count(',') > headers_commas:
            last_comma_index = line.rfind(",")
            new_line = line[:last_comma_index] + "" + line[last_comma_index + 1:]
            adapted_contents.append(new_line)
        else:
            adapted_contents.append(line)
    return adapted_contents


def get_unified_grouped_list(headers, grouped_data_dict):
    new_data = [headers.strip().split(',')]
    for (c1, c2), g in grouped_data_dict:
        c3, c4, c5, c6, c7 = '', '', '', '', ''
        for d in g:
            c3 = d['surname'] if not c3 == d['surname'] else c3
            c4 += d['organization']
            c5 += d['position']
            c6 += d['phone']
            c7 += d['email']
        new_data.append([c1, c2, c3, c4, c5, c6, c7])
    return new_data


def main():
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        contacts_list = f.readlines()

    line_pattern = re.compile("(?P<fio>.*)[,](?P<organization>[^,]*)?[,]"
                              "(?P<position>[^,]*)?[,](?P<phone>[^,]*)?[,](?P<email>[^,\n]*)?$")
    fio_pattern = re.compile("(?P<lastname>[А-Я][а-я]+)[, ](?P<firstname>[А-Я][а-я]+)[, ](?P<surname>[А-Я][а-я]+|)")
    number_pattern = re.compile("^(8|\\+7)\\D*(\\d{3})\\D*(\\d{3})\\D*(\\d{2})\\D*(\\d{2})")
    extra_number_pattern = re.compile(".*(доб\\.)\\D(\\d{4}|)?")

    adapted_contents = get_adapted_contents(contacts_list)
    headers = adapted_contents[0]
    data = adapted_contents[1:]
    records_list = []

    for index, line in enumerate(data):
        if re.match(line_pattern, line):
            fio_line, organization, position, phone, email = re.match(line_pattern, line).groups()
            if re.match(fio_pattern, fio_line):
                lastname, firstname, surname = re.match(fio_pattern, fio_line).groups()
                if re.match(number_pattern, phone):
                    a, b, c, d, e = re.match(number_pattern, phone).groups()
                    if re.match(extra_number_pattern, phone):
                        f, g = re.match(extra_number_pattern, phone).groups()
                        fg = ' ' + f + g
                    else:
                        fg = ''
                    formatted_number = f"{a}({b}){c}-{d}-{e}{fg}"
                else:
                    formatted_number = phone
                d = {'lastname': lastname,
                     'firstname': firstname,
                     'surname': surname,
                     'organization': organization,
                     'position': position,
                     'phone': formatted_number,
                     'email': email}
                records_list.append(d)

    keys = operator.itemgetter('lastname', 'firstname')
    operator.itemgetter('surname', 'organization', 'position', 'phone', 'email')
    records_list.sort(key=keys)
    grouped_records_list = itertools.groupby(records_list, keys)
    unified_records_list = get_unified_grouped_list(headers, grouped_records_list)

    with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(unified_records_list)


if __name__ == '__main__':
    main()
