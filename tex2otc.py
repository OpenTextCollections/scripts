import glob
import re
import csv
import json

def uppercase_textsc(s):
    result = s
    textscs = re.findall(r"\\textsc{(.*?)}",s)
    for textsc in textscs:
        result = result.replace(r"\textsc{%s}"%textsc, textsc.upper())
    return result.replace(r'\TEXTSC','').replace(r'\textsc','')


def tex2unicode(s):
    result = s
    result = result.replace("\\textsuperscript{A}","ᴬ")
    result = result.replace("\\textsuperscript{K}","ᴷ")
    result = result.replace("\\stackunder[-10pt]{\\^{i}}{\\'{}}","î́")
    result = result.replace("\\'e","é")
    result = result.replace("\\'u","ú")
    result = result.replace("\\'o","ó")
    result = result.replace("\\'i","í")
    result = result.replace("\\'a","á")
    result = result.replace("{-\\O}","-Ø")
    result = result.replace("{\\O}","Ø")
    return result

def get_imt_blocks(lines, number, textname, glottocode):
    print(textname)
    blocks = []
    gll_line = None
    examplenumber = 1
    for i,line in enumerate(lines):
        if 'gll' in line:
            assert('glt' in lines[i+2])
            orthographic = tex2unicode(lines[i-1].replace('\\textit','').replace('\\\\','').strip()[1:-1])
            morphemic = tex2unicode(lines[i].replace('\\gll','').strip()[:-2])
            gloss = uppercase_textsc(lines[i+1].strip()[:-2].replace('\\_','_'))
            translation = tex2unicode(lines[i+2].replace('\\glt','').strip()[1:-1])
            found_glosses = re.findall("[A-Z][A-Z_]+", gloss)
            abbreviations = {}
            for k in found_glosses:
                try:
                    expansion = abbr[k]
                    abbreviations[k] = expansion
                except KeyError:
                    print(f"no expansion found for abbreviation {k}")

            blocks.append({
               "ID": f'{glottocode}a-{textname}-{examplenumber}',
               "Primary_Text":orthographic,
               "Analyzed_Word":morphemic.replace(' ', '\t'),
               "Gloss":gloss.replace(' ', '\t'),
               "Translated_Text":translation,
               "Text_ID": textname,
               "Sentence_Number": examplenumber,
               "Language_ID": glottocode,
               "OTC_ID": f'{glottocode}a',
               "LGR_Conformance": 'WORD_ALIGNED',
               "Abbreviations": abbreviations
            })
            examplenumber += 1
    return blocks


found_fieldnames = "ID","Primary_Text","Analyzed_Word","Gloss","Translated_Text","Text_ID","Sentence_Number","Language_ID","OTC_ID","LGR_Conformance","Abbreviations"

files = sorted(glob.glob("*tex"))
global_rows = []
glottocode = 'hawr1243'
abbr = json.loads(open("abbr.json").read())
for j, f in enumerate(files):
    textname = f.split('/')[-1].replace('.tex','').replace('-glossed','')
    with open(f) as infile:
        lines = infile.readlines()
    global_rows += get_imt_blocks(lines, j+1, textname, glottocode)

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

