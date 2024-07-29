import re
dictionary =  {}

with open("gloss.sty", "r", encoding="UTF-8") as read_file:
    for line in read_file:
        if "\entry" in line:
            res = re.findall(r"\\entry\{([^\}]*)\}\}?\{/[^/]*/\}\{([^\}]*)\}\}?\{([^\}]*)", line)
            # print(re.sub(r"\\hl\{([^\}]*)\}", r"$1", res[0][1]))
            dictionary[re.sub(r"\\hl\{([^\}]*)", r"\1", res[0][1])] = "{" + re.sub(r"\\hl\{([^\}]*)", r"\1", res[0][0]) +"}{" + re.sub(r"\\hl\{([^\}]*)", r"\1", res[0][2]) + "}"

sorted_dict = dict(sorted(dictionary.items(), key=lambda s: s.lower()))

with open("english_glossary.tex", "w", encoding="UTF-8") as writefile:
    writefile.write("\\begin{multicols}{2}[\\chapter{English-Hewramî Glossary}]\n\n\\begin{sloppypar}\n")
    heading = ""
    for key, item in sorted_dict.items():
        if key[0] != heading:
            heading = key[0]
            writefile.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n%%%%%%%        " + heading + "          %%%%%%%%%%%%%\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n%\n\\\\{\\noindent\\Huge\\textbf{" + heading + "}}\\\\\n%\n")
        writefile.write("\\engentry{" + key + "}" + item + "\n%\n")
    writefile.write("\n\\end{sloppypar}\n\n\end{multicols}")
