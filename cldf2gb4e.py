import csv
import sys
import re

examples = True

output_type = "examples"
try:
    output_type = sys.argv[3]
except IndexError:
    pass

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
\newcommand{\verntrans}[2]{\parbox[t]{.45\textwidth}{#1}\qquad\parbox[t]{.45\textwidth}{#2}\medskip\par}
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
            vernaculars = []
            translations = []
            for row in csv_reader:
                vernacular = row["Analyzed_Word"].strip()
                vernacular_words = vernacular.split("\t")
                recomposed_string = "\t".join(["{%s}"%w if " " in w else w for w in vernacular_words])
                recomposed_string = recomposed_string.replace("&","\\&").replace("#","\\#").replace("\t\t","\t{\\relax}\t")
                gloss = row["Gloss"]
                allcapsglosses = re.findall("([A-Z.]*[A-Z]+)",gloss)
                for match in  sorted(allcapsglosses):
                    gloss=gloss.replace(match, "\\textsc{%s}"%match.lower())
                gloss=gloss.replace("_", "\\_").replace(" ", "\\_").replace("&","\\&").replace("#","\#").replace("\t\t","\t{\\relax}\t")
                if gloss.startswith("\t"):
                    gloss = "{\\relax}"+gloss
                processed_translation = row["Translated_Text"].replace("&","\\&").replace("#","\\#")
                if output_type == "examples":
                    tex_file.write('\\ea\\label{ex:%s}\n' % row["ID"])
                    tex_file.write(f'\\gll {recomposed_string}\\\\\n')
                    tex_file.write(f'     {gloss}\\\\\n')
                    tex_file.write(f"""\\glt `{processed_translation}'\n""")
                    tex_file.write("\\z\n\n")
                if output_type == "lines":
                    tex_file.write("\\verntrans{%s}{%s}\n" % (recomposed_string,processed_translation))
                if output_type == "pages":
                    vernaculars.append(recomposed_string)
                    translations.append(processed_translation)
        if output_type == "columns":
            print(len(vernaculars))
            print(len(translations))
            max_chars_page=1700
            accumulated_chars_vernacular=0
            accumulated_chars_translation=0
            print(accumulated_chars_vernacular)
            print(accumulated_chars_translation)
            tex_file.write("\\begin{tabular}{p{.45\\textwidth}@{\qquad\qquad}p{.45\\textwidth}}\n")
            vernacular_cell = []
            translation_cell = []
            for i,_ in enumerate(vernaculars):
                vernacular = vernaculars[i]
                translation = translations[i]
                accumulated_chars_vernacular += len(vernacular)
                accumulated_chars_translation += len(translation)
                if accumulated_chars_vernacular > max_chars_page or accumulated_chars_translation > max_chars_page:
                    tex_file.write("\n".join(vernacular_cell))
                    tex_file.write("\n&\n")
                    tex_file.write("\n".join(translation_cell))
                    tex_file.write("\n\\end{tabular}\medskip\n\n")
                    tex_file.write("\\begin{tabular}{p{.45\\textwidth}@{\qquad\qquad}p{.45\\textwidth}}\n")
                    accumulated_chars_vernacular=len(vernacular)
                    accumulated_chars_translation=len(translation)
                    vernacular_cell = [vernacular]
                    translation_cell = [translation]
                vernacular_cell.append(vernacular)
                translation_cell.append(translation)
            tex_file.write("\n".join(vernacular_cell))
            tex_file.write("\n&\n")
            tex_file.write("\n".join(translation_cell))
            tex_file.write("\\end{tabular}\medskip\n\n")
        if output_type == "pages":
            print(len(vernaculars))
            print(len(translations))
            max_chars_page=3500
            accumulated_chars_vernacular=0
            accumulated_chars_translation=0
            print(accumulated_chars_vernacular)
            print(accumulated_chars_translation)
            vernacular_cell = []
            translation_cell = []
            for i,_ in enumerate(vernaculars):
                vernacular = vernaculars[i]
                translation = translations[i]
                accumulated_chars_vernacular += len(vernacular)
                accumulated_chars_translation += len(translation)
                if accumulated_chars_vernacular > max_chars_page or accumulated_chars_translation > max_chars_page:
                    tex_file.write("\n".join(vernacular_cell))
                    tex_file.write("\\newpage\n")
                    tex_file.write("\n".join(translation_cell))
                    tex_file.write("\\newpage\n")
                    accumulated_chars_vernacular=len(vernacular)
                    accumulated_chars_translation=len(translation)
                    vernacular_cell = [vernacular]
                    translation_cell = [translation]
                vernacular_cell.append(vernacular)
                translation_cell.append(translation)
            tex_file.write("\n".join(vernacular_cell))
            tex_file.write("\\newpage\n")
            tex_file.write("\n".join(translation_cell))
        tex_file.write(end_document)

