from os import path, getenv, remove, devnull
from subprocess import check_output

FNULL = open(devnull, 'w')

OBT_PATH = getenv("OBT_PATH", "")
if OBT_PATH == "":
    raise EnvironmentError("Path to Oslo-Bergen-Tagger installation dir 'OBT_PATH' not set.")

TAGS = {
    'adj': {
        'kjønn': ['m/f', 'nøyt', 'fem'],
        'tall': ['ent', 'fl'],
        'type': ['<adv>', '<ordenstall>', '<perf-part>', '<pres-part>', 'fork'],
        'best': ['ub', 'be'],
        'grad': ['pos', 'kom', 'sup']
    },
    'adv': {
        'type': ['fork']
    },
    'det': {
        'kjønn': ['fem', 'nøyt', 'mask'],
        'tall': ['ent', 'fl'],
        'type': ['dem', 'dem <adj>', '<adj> forst',
                 '<adj> kvant', 'kvant', 'poss', 'poss res', 'poss høflig', 'sp', 'forst'],
        'best': ['ub', 'be'],
    },
    'konj': {
        'type': ['<adv>', 'clb'],
    },
    'prep': {
        'type': ['fork']
    },
    'pron': {
        'kjønn': ['fem', 'mask', 'mask fem', 'nøyt'],
        'tall': ['ent', 'fl'],
        'type': ['hum res', 'hum sp', 'pers', 'pers hum', 'pers høflig', 'poss hum sp', 'refl', 'sp', 'res'],
        'person': ["1", "2", "3"],
        'kasus': ['nom', 'akk'],
    },
    'sbu': {
        'type': ['<spørreartikkel>'],
    },
    'subst': {
        'kjønn': ['nøyt', 'fem', 'mask'],
        'tall': ['ent', 'fl'],
        'type': ['appell fork', 'appell', 'prop', 'fork'],
        'best': ['ub', 'be'],
        'kasus': ['gen'],
    },
    'verb': {
        'tid': ['pres inf pass', 'pres', 'inf', 'pret', 'perf-part', 'imp'],
    }
}


def write_file(data, filepath):
    with open(filepath, "w+") as f:
        f.write(data)


def assign_tags(word_tags):
    pos_tag = word_tags[0]
    tags = word_tags[1:]
    tag = {'ordklasse': pos_tag, 'raw_tags': ' '.join(word_tags)}

    num_tags = len(tags)
    num_tags_assigned = 0

    while len(tags) > 0 and num_tags_assigned < num_tags:
        proposed_tag = ' '.join(tags)

        found = False
        if pos_tag in TAGS:
            for t in TAGS[pos_tag]:
                if proposed_tag in TAGS[pos_tag][t]:
                    tag[t] = proposed_tag
                    found = True
                    break

        length = len(tags)

        if found:
            num_tags_assigned += length
            tags = word_tags[1+num_tags_assigned:]
        elif length == 1:
            if "tilleggstagger" not in tag:
                tag["tilleggstagger"] = []
            tag["tilleggstagger"].append(proposed_tag)
            num_tags_assigned += 1
            tags = word_tags[1+num_tags_assigned:]
        else:
            tags = tags[:-1]

    return tag


def check_input(text, file):
    if text is None and file is None:
        raise ValueError("No argument passed. Either pass a string or a filename using the file= kwarg")
    if text is not None and file is not None:
        raise ValueError("Both a string and file were passed as argument. Please only use one.")
    if file is not None and not path.isfile(file):
        raise FileNotFoundError("Could not find file called \"" + str(file) + "\"")


def save_json(tags, filename):
    from json import dumps
    write_file(dumps(tags, indent=2), filename)


def tag_bm(text=None, file=None, encoding="UTF-8"):
    check_input(text, file)

    if text is not None:
        temp_file = "/tmp/obtfile.txt"
        write_file(text, temp_file)
        result = check_output([path.join(OBT_PATH, "tag-bm.sh"), temp_file], stderr=FNULL).decode(encoding)
        remove(temp_file)
    else:
        result = check_output([path.join(OBT_PATH, "tag-bm.sh"), file], stderr=FNULL).decode(encoding)

    tags = []

    lines = result.split("\n")

    tag_starts = [line for line in lines if line.startswith("<word>")]
    num_tags = len(tag_starts)
    tag_start_indexes = [lines.index(tag_start) for tag_start in tag_starts]

    for i in range(num_tags):
        index = tag_start_indexes[i]
        word = lines[index].strip()[6:-7]
        word_tag = lines[index + 1].strip()[1:-1]

        word_tags_split = lines[index + 2].strip().split()
        base = word_tags_split[0][1:-1]
        word_tags = word_tags_split[1:]

        tag = assign_tags(word_tags)
        tag["word"] = word
        tag["word_tag"] = word_tag
        tag["base"] = base
        tags.append(tag)

    return tags
