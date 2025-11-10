import json
import csv
import sys
import os
import re

def expand(filename, language_id, abbr={}, metalanguage_id="stan1293", kuerzel="a"):
    text_id = filename.split(".")[0]
    print(text_id)
    otc_id = language_id + kuerzel

    with open(filename) as csv_in:
        rows = csv.DictReader(csv_in)
        fieldnames = rows.fieldnames + ["OTC_ID", "LGR_Conformance", "Abbreviations"]
        result = []
        for i, row in enumerate(rows):
            sentence_number = i + 1
            old_id = row["ID"]
            id_ = f"{otc_id}-{text_id}-{old_id}"
            row["ID"] = id_
            row["OTC_ID"] = otc_id
            row["Text_ID"] = text_id
            row["Sentence_Number"] = sentence_number
            row["LGR_Conformance"] = "WORD_ALIGNED"
            row["Language_ID"] = language_id
            found_glosses = re.findall("[A-Z][A-Z_]+", row["Gloss"])
            row["Abbreviations"] = {}
            for k in found_glosses:
                try:
                    expansion = abbr[k]
                    row["Abbreviations"][k] = expansion
                except KeyError:
                    print(f"no expansion found for abbreviation {k}")
            result.append(row)
    return result, fieldnames


if __name__ == "__main__":
    language_id = os.getcwd().split("/")[-1]
    filenames = sys.argv[1:]
    abbr = json.loads(open("abbr.json").read())
    global_rows = []
    found_fieldnames = ['Language_ID', 'Text_ID', 'Sentence_Number']
    banned = ["LGR", "LGRConformance"]
    for filename in filenames:
        print(filename)
        rows, fieldnames = expand(filename, language_id, abbr)
        found_fieldnames += [x for x in fieldnames if x not in found_fieldnames and x not in banned]
        global_rows += rows
    with open("sentences.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=found_fieldnames)
        writer.writeheader()
        for row in global_rows:
            try:
                del row['LGR']
            except KeyError:
                pass
            try:
                del row['LGRConformance']
            except KeyError:
                pass
            writer.writerow(row)
