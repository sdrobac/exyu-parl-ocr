import cyrtranslit
import numpy as np
import roman
from Levenshtein import ratio
from lxml import etree
import zipfile
from pathlib import Path
import tempfile


def parse_numbering(r, namespaces):
    anum = {}
    for n in r.findall('.//w:abstractNum', namespaces):
        nid = n.attrib[f'{{{namespaces["w"]}}}abstractNumId']
        levels = {}
        for l in n.findall('./w:lvl', namespaces):
            lid = l.attrib[f'{{{namespaces["w"]}}}ilvl']
            t = l.find('./w:start', namespaces)
            if not t is None:
                lst = int(t.attrib[f'{{{namespaces["w"]}}}val'])
            else:
                lst = 1
            lfmt = l.find('./w:numFmt', namespaces).attrib[f'{{{namespaces["w"]}}}val']
            ltxt = l.find('./w:lvlText', namespaces).attrib[f'{{{namespaces["w"]}}}val']
            levels[lid] = [lst, lfmt, ltxt]
        anum[nid] = levels
    numberings = {}
    for n in r.findall('.//w:num', namespaces):
        nid = n.attrib[f'{{{namespaces["w"]}}}numId']
        aid = n.find('./w:abstractNumId', namespaces).attrib[f'{{{namespaces["w"]}}}val']
        numberings[nid] = anum[aid]
    return numberings


def decode_numbering(nid, lid, numberings):
    n = numberings[nid][lid]
    number = n[0]
    n[0] += 1
    if n[1] == 'decimal':
        nstr = str(number)
    elif n[1] == 'bullet':
        nstr = "X"
    elif n[1] == 'upperRoman':
        nstr = roman.toRoman(number).upper()
    elif n[1] == 'lowerRoman':
        nstr = roman.toRoman(number).lower()
    elif n[1] == 'upperLetter':
        nstr = chr(number + 64)
    elif n[1] == 'lowerLetter':
        nstr = chr(number + 96)
    elif n[1] == 'russianLower':
        nstr = cyrtranslit.to_cyrillic(chr(number + 96))
    elif n[1] == 'russianUpper':
        nstr = cyrtranslit.to_cyrillic(chr(number + 64))
    else:
        print("Unknown numbering format:", n[1])
        exit(1)
    return n[2].replace('%1', nstr) + "\t"


def pretty_print_cell(cell, namespaces, numberings):
    cell_text = ""
    for element in cell.findall('./w:p', namespaces):
        p_runs = process_xml_tree(element, namespaces, numberings, [], remove_br=False)
        p_runs = sum(p_runs, [])
        cell_text = cell_text + "\n" + "".join([run[0] for run in p_runs])
    return cell_text.strip()


# Function to pretty print a table
def pretty_print_table(table, namespaces, numberings):
    columns = []
    rows = table.findall('.//w:tr', namespaces)
    for row in rows:
        i=0
        for cell in row.findall('.//w:tc', namespaces):
            while i>=len(columns):
                columns.append([])
            gs = cell.find('./w:tcPr/w:gridSpan', namespaces)
            if gs is not None:
                gs = int(gs.attrib[f'{{{namespaces["w"]}}}val'])
            else:
                gs = 1
            txt = pretty_print_cell(cell, namespaces, numberings)
            n = list(txt.split('\n'))
            columns[i] += n
            for j in range(1, gs):
                if j==len(columns):
                    columns.append([])
                columns[j] += [''] * len(n)
            i += gs

    lines = []
    for i in range(max([len(x) for x in columns])):
        line = ""
        for j in range(len(columns)):
            if i < len(columns[j]):
                line += columns[j][i] + "\t"
            else:
                line += "\t"
        lines.append(line[:-1])
    return lines


# Function to extract text and formatting from runs
def process_run(run, namespaces, remove_br=True):
    text = ""
    formatting = {}

    for t in run.findall('./', namespaces):
        if t.tag == f'{{{namespaces["w"]}}}t':
            text += t.text
        elif t.tag == f'{{{namespaces["w"]}}}tab':
            text += "\t"
        elif t.tag == f'{{{namespaces["w"]}}}br':
            if remove_br:
                if text.endswith("-"):
                    text = text[:-1]
                else:
                    text += " "
            else:
                text += "\n"
    # Extract text

    # Extract formatting
    properties = run.find('./w:rPr', namespaces)
    if properties is not None:
        if properties.find('.//w:b', namespaces) is not None:
            formatting['bold'] = True
        if properties.find('.//w:i', namespaces) is not None:
            formatting['italic'] = True
        if properties.find('.//w:u', namespaces) is not None:
            formatting['underline'] = True
        color = properties.find('.//w:color', namespaces)
        if color is not None and f'{{{namespaces["w"]}}}val' in color.attrib:
            formatting['color'] = color.attrib[f'{{{namespaces["w"]}}}val']
        size = properties.find('.//w:sz', namespaces)
        if size is not None and f'{{{namespaces["w"]}}}val' in size.attrib:
            formatting['size'] = int(size.attrib[f'{{{namespaces["w"]}}}val'])
    return text, formatting


def process_para(paragraph, namespaces, numberings):

    numbering_props = paragraph.find('./w:pPr/w:numPr', namespaces)
    if numbering_props is not None:
        numbering_id = numbering_props.find('./w:numId', namespaces)
        level = numbering_props.find('./w:ilvl', namespaces)
        if numbering_id is not None and level is not None:
            numbering_id = numbering_id.attrib[f'{{{namespaces["w"]}}}val']
            level = level.attrib[f'{{{namespaces["w"]}}}val']
            decoded_numbering = decode_numbering(numbering_id, level, numberings)
            return decoded_numbering, {}

    return None


def process_xml_tree(node, namespaces, numberings, current_paragraphs, remove_br=True):

    nodes = node.findall('./', namespaces)
    if any(x.find('./mc:AlternateContent', namespaces) is not None and x.find('../w:pPr/w:numPr', namespaces) is not None for x in nodes):
        nodes = [x for x in nodes if x.find('./w:t', namespaces) is not None] + [x for x in nodes if x.find('./w:t', namespaces) is None]

    for n in nodes:
        add_newparagraph = False
        if n.tag == f'{{{namespaces["w"]}}}p':
            if len(current_paragraphs) == 0 or len(current_paragraphs[-1]) > 0:
                current_paragraphs.append([])
            p_head = process_para(n, namespaces, numberings)
            if p_head:
                current_paragraphs[-1].append(p_head)
        elif n.tag == f'{{{namespaces["v"]}}}textbox':
            if len(current_paragraphs) == 0 or len(current_paragraphs[-1]) > 0:
                current_paragraphs.append([])
            add_newparagraph = True
        elif n.tag == f'{{{namespaces["w"]}}}r':
            run = process_run(n, namespaces, remove_br=remove_br)
            if len(current_paragraphs) == 0:
                current_paragraphs.append([])
            current_paragraphs[-1].append(run)
        para = process_xml_tree(n, namespaces, numberings, current_paragraphs, remove_br)
        if add_newparagraph and len(current_paragraphs[-1]) > 0:
            current_paragraphs.append([])
    return current_paragraphs


def parse_word(file):

    # Open the Word document (as a .zip file)
    with zipfile.ZipFile(file, 'r') as zip_ref:
        # Extract the document.xml file from the .zip
        zip_ref.extract('word/document.xml', tempfile.gettempdir())
        zip_ref.extract('word/numbering.xml', tempfile.gettempdir())

    # Load the XML file
    xml_path = tempfile.gettempdir() + '/word/document.xml'
    xml_tree = etree.parse(xml_path)
    root = xml_tree.getroot()

    # Define the XML namespaces
    namespaces = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
        'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'v': 'urn:schemas-microsoft-com:vml',
        'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    }

    etree.strip_elements(root, f'{{{namespaces["w"]}}}drawing', with_tail=False)

    xml_npath = tempfile.gettempdir() + '/word/numbering.xml'
    xml_ntree = etree.parse(xml_npath)
    nroot = xml_ntree.getroot()

    numberings = parse_numbering(nroot, namespaces)

    # Process tables and convert to paragraphs
    for table in root.findall('.//w:tbl', namespaces):
        lines = pretty_print_table(table, namespaces, numberings)
        for t in table.findall('./', namespaces):
            table.remove(t)
        for l in lines:
            new_paragraph = etree.Element(f'{{{namespaces["w"]}}}p')
            new_run = etree.SubElement(new_paragraph, f'{{{namespaces["w"]}}}r')
            new_text = etree.SubElement(new_run, f'{{{namespaces["w"]}}}t')
            new_text.text = l
            # etree.SubElement(new_run, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}br')
            # Insert the new paragraph before the table
            table.addprevious(new_paragraph)

    # Process paragraphs and text frames
    return process_xml_tree(root, namespaces, numberings, [])


def order_lines(source_lines, paragraphs):
    target_lines = [''.join([x[0] for x in p]) + '\n' for p in paragraphs]
    ix = np.zeros(len(target_lines)) - 1
    pos = np.linspace(0, len(source_lines), len(target_lines), dtype=int)
    for (i, l) in enumerate(target_lines):
        six = max(0, pos[i] - 50)
        eix = min(len(source_lines), pos[i] + 50)
        ldist = np.array([ratio(l, x) for x in source_lines[six:eix]])
        ixmax = np.argmax(ldist)
        if ldist[ixmax] > 0.9 and np.count_nonzero(ldist == ldist[ixmax]) == 1:
            ix[i] = ixmax + six

    if ix[0] == -1:
        ix[0] = 0
    for i in range(1, len(ix)):
        if ix[i] == -1:
            ix[i] = ix[i - 1] + 0.0001

    paragraphs = [x for _, x in sorted(zip(ix, paragraphs))]
    return paragraphs


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('file_or_dir', metavar='file_or_dir', type=str, help='word file or directory with word files')
    args = parser.parse_args()

    root = Path(args.file_or_dir)

    if root.is_file():
        files = [root]
    else:
        files = [x for x in root.glob('**/*.docx')]

    for file in files:

        # get paragraphs with formatting from .docx
        paragraphs = parse_word(str(file))

        # This reorders lines in accordance to the .txt file, however it is VERY SLOW
        if file.with_suffix('.txt').exists():
            with file.with_suffix('.txt').open('r', encoding='utf-8') as f:
                source_doc = f.readlines()
            paragraphs = order_lines(source_doc, paragraphs)

        # write just text to file .docx.txt
        txt = ""
        for p in paragraphs:
            txt += ''.join([x[0] for x in p]) + '\n'
        with open(f'{str(file)}.txt', 'w', encoding='utf-8') as f:
            f.write(txt)

    return


if __name__ == '__main__':
    main()  # noqa pylint: disable=no-value-for-parameter
