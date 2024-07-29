# -*- coding: utf-8 -*-

import os # package for accesing file structures
import string # package for manipulating strings
import re # package for regular expressions

# Define function that strips sentences and translations
def gloss_strip(type, text):
    # initializing substrings
    sub1 = type
    sub2 = "</item>"
    s=str(re.escape(sub1))
    e=str(re.escape(sub2))
    res=re.findall(s+"(.*)"+e,text)[0]
    return res

# Define function that strips morphemes and glosses
def gloss_strip_hyph(type, text, bool):
    res = gloss_strip(type, text)
    if res.startswith("=") or res.startswith("-"):
        out = res
    elif res.endswith("=") or res.endswith("-"):
        bool = True
        out = " " + res
    elif bool:
        out = res
        bool = False
    else:
        out = " " + res
    return out, bool
        
# Set XML tags for words, parsed words, glosses, and translations
sType = "<item type=\"txt\" lang=\"hac-baseline\">"
pType = "<item type=\"txt\" lang=\"hac-morpheme\">"
gType = "<item type=\"gls\" lang=\"en-lexGloss\">"
tType = "<item type=\"gls\" lang=\"en-free\">"

# Begin Gloss Numbering
glossnumb = 1

# Set boolean variable that controlls  morpheme spacing
spacebool = False

# List all glosses to be converted to SC
sc_list = ["=3pl", ".3pl", "-3pl", ".3sg", "=3sg", "-3sg", ".2sg", "=2sg", "2sg", ".2pl", "-2pl", "=2pl", ".1sg", "=1sg", "-1sg", ".1pl", "-1pl", "=1pl", #
".gen", "=ez", "attr", "-dir", ".dir", "-obl", ".obl", ".ez.gen", #
".f", "-f", "-pl", ".m", ".pl", "-pl", "-dim", #
".def", "-def", "-indf", ".indf", ".cmpd", "sbjv-", "ind-", "-pstc", "imp-", "-imp", ".imp", "neg-", #
".prs", ".pst", ".ptcp", "pvb-", "=povb", "povb", "=compl",".pstc", ".adv", #
"=add", "=dem", "=post", "=cop", "-nmlz", "clf", #
"dem.prox", "dem.dist", "pn", "reflx", "intj", "post", "ptcl", "hort", "fill", "voc", "neg.exist", "neg.", #
]

# Select file name
file = "DPhtmlTXT"

# Initialize line variables
opening = ""
label = ""
sentence = ""
parsing = ""
gloss = ""
translation = ""
close = ""

# Open file
txtfile = open(file + '_gloss.txt', 'w', encoding="utf-8")
readfile = open(file + '.txt', encoding='utf-8')

# Extract glosses from XML-format TXT file and write to TXT file
for line in readfile:
    if sType in line:
        sentence += " " + gloss_strip(sType, line)
    elif pType in line:
        res, spacebool = gloss_strip_hyph(pType, line, spacebool)
        parsing += res
    elif gType in line:
        res, spacebool = gloss_strip_hyph(gType, line, spacebool)
        gloss += res
    elif tType in line:
        translation = gloss_strip(tType, line)

        # Format the glosses in lansci-gb4e style
        label = "\\ea \\label{" + file + "." + str(glossnumb) + "}\n"
        sentence = "\\textit{" + sentence + "} \\\\ \n"
        sentence = sentence.replace("\\textit{ ", "\\textit{")
        parsing = "\\gll " + parsing + " \\\\ \n"
        parsing = parsing.replace("\\gll  ", "\\gll ")
        gloss = gloss + " \\\\ \n"
        gloss = re.sub('==', '=', gloss)
        for w in sc_list:
            if w in gloss:
                gloss = gloss.replace(w, "\\textsc{" + w + "}")
        translation = "\\glt `" + translation + "\'\n"
        close = "\\z \n \n"

        # Write the glosses
        txtfile.write(label)
        txtfile.write(sentence)
        txtfile.write(parsing)
        txtfile.write(gloss)
        txtfile.write(translation)
        txtfile.write(close)

        # Add to the gloss counter
        glossnumb += 1

        # Clear line variables
        opening = ""
        label = ""
        sentence = ""
        parsing = ""
        gloss = ""
        translation = ""
        close = ""