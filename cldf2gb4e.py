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
with open(f"{filename}.tex","w") as tex_file:
    tex_file.write(preamble)
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            tex_file.write('\\ea\\label{ex:%s}\n' % row["ID"])
            vernacular = row["Analyzed_Word"].strip().replace(" ", "\\_")
            tex_file.write(f'\\gll {vernacular}\\\\\n')
            gloss = row["Gloss"]
            allcapsglosses = re.findall("([A-Z][A-Z]+)",gloss)
            for match in  sorted(allcapsglosses):
                gloss=gloss.replace(match, "\\textsc{%s}"%match.lower())
            gloss=gloss.replace(" ", "\\_")
            tex_file.write(f'     {gloss}\\\\\n')
            tex_file.write(f"""\\glt `{row["Translated_Text"]}'\n""")
            tex_file.write("\\z\n\n")
    tex_file.write(end_document)
