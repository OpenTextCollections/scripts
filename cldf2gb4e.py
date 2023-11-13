import csv
import sys
import re

title = ""
maketitle = ""
try:
    title = "\\title{%s}\date{}" %sys.argv[2]
    maketitle = "\maketitle"
except IndexError:
    pass

preamble=r"""\documentclass{scrartcl}
\usepackage{libertine}
\usepackage{langsci-gb4e}
\examplesitalics
%s
\begin{document}
%s
""" % (title,maketitle)

end_document="\\end{document}"


filename = sys.argv[1]
if not filename.endswith("csv"):
    print("please provide a file of type csv")
else:
    tex_filemame = filename[0:-4]+".tex"
    print(tex_filemame)
    with open(tex_filemame,"w") as tex_file:
        tex_file.write(preamble)
        with open(filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                tex_file.write('\\ea\\label{ex:%s}\n' % row["ID"])
                vernacular = row["Analyzed_Word"].strip()
                vernacular_words = vernacular.split("\t")
                recomposed_string = "\t".join(["{%s}"%w if " " in w else w for w in vernacular_words]).replace("&","\\&").replace("#","\\#")
                tex_file.write(f'\\gll {recomposed_string}\\\\\n')
                gloss = row["Gloss"]
                allcapsglosses = re.findall("([A-Z][A-Z]+)",gloss)
                for match in  sorted(allcapsglosses):
                    gloss=gloss.replace(match, "\\textsc{%s}"%match.lower())
                gloss=gloss.replace(" ", "\\_").replace("&","\\&")
                tex_file.write(f'     {gloss}\\\\\n')
                processed_translation = row["Translated_Text"].replace("&","\\&").replace("#","\\#")
                tex_file.write(f"""\\glt `{processed_translation}'\n""")
                tex_file.write("\\z\n\n")
        tex_file.write(end_document)
