"""Small XLSX reader for the fixed historical Meta export used in this project.

The public pipeline only needs to read cell values from one .xlsx worksheet.  An
XLSX file is a ZIP package containing XML documents, so the standard library is
sufficient for this narrow task.  This avoids introducing a spreadsheet-library
dependency solely to extract a small, fixed table.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import zipfile
import xml.etree.ElementTree as ET

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"

CELL_REF_RE = re.compile(r"([A-Z]+)(\d+)")


@dataclass(frozen=True)
class WorksheetData:
    """Cell values from one worksheet, preserving Excel row positions."""

    rows: list[list[object | None]]


def column_index(cell_reference: str) -> int:
    """Convert an Excel cell reference such as 'C12' to a zero-based column."""
    match = CELL_REF_RE.fullmatch(cell_reference)
    if not match:
        raise ValueError(f"Invalid Excel cell reference: {cell_reference!r}")
    letters = match.group(1)
    value = 0
    for letter in letters:
        value = value * 26 + (ord(letter) - ord("A") + 1)
    return value - 1


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    """Read the workbook shared-string table, if present."""
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []

    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    strings: list[str] = []
    for string_item in root.findall(f"{{{MAIN_NS}}}si"):
        # A shared string can contain several rich-text runs.  Concatenate all
        # <t> nodes in document order so the visible Excel value is preserved.
        text = "".join(
            node.text or "" for node in string_item.iter(f"{{{MAIN_NS}}}t")
        )
        strings.append(text)
    return strings


def _worksheet_target(archive: zipfile.ZipFile, sheet_name: str) -> str:
    """Resolve an Excel worksheet name to its XML part within the ZIP package."""
    workbook_root = ET.fromstring(archive.read("xl/workbook.xml"))
    relationships_root = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))

    relationship_targets = {
        relation.attrib["Id"]: relation.attrib["Target"]
        for relation in relationships_root.findall(f"{{{PKG_REL_NS}}}Relationship")
    }

    sheets_node = workbook_root.find(f"{{{MAIN_NS}}}sheets")
    if sheets_node is None:
        raise ValueError("Workbook contains no sheets collection")

    for sheet in sheets_node:
        if sheet.attrib.get("name") != sheet_name:
            continue
        relationship_id = sheet.attrib[f"{{{DOC_REL_NS}}}id"]
        target = relationship_targets[relationship_id].lstrip("/")
        if not target.startswith("xl/"):
            target = f"xl/{target}"
        return target

    raise KeyError(f"Worksheet {sheet_name!r} was not found")


def _parse_number(raw: str) -> int | float:
    """Parse an XML numeric cell without unnecessarily converting integers."""
    number = float(raw)
    return int(number) if number.is_integer() else number


def read_worksheet(path: str | Path, sheet_name: str) -> WorksheetData:
    """Read visible cell values from one worksheet in an XLSX workbook."""
    workbook_path = Path(path)
    with zipfile.ZipFile(workbook_path) as archive:
        shared = _shared_strings(archive)
        target = _worksheet_target(archive, sheet_name)
        root = ET.fromstring(archive.read(target))

    parsed_rows: dict[int, dict[int, object | None]] = {}
    max_column = -1
    max_row = 0

    sheet_data = root.find(f"{{{MAIN_NS}}}sheetData")
    if sheet_data is None:
        return WorksheetData(rows=[])

    for row_node in sheet_data.findall(f"{{{MAIN_NS}}}row"):
        excel_row = int(row_node.attrib.get("r", "0"))
        if excel_row <= 0:
            continue
        max_row = max(max_row, excel_row)
        cells: dict[int, object | None] = {}
        for cell in row_node.findall(f"{{{MAIN_NS}}}c"):
            reference = cell.attrib.get("r")
            if not reference:
                continue
            index = column_index(reference)
            max_column = max(max_column, index)
            cell_type = cell.attrib.get("t")
            value_node = cell.find(f"{{{MAIN_NS}}}v")

            if cell_type == "inlineStr":
                inline = cell.find(f"{{{MAIN_NS}}}is")
                value = "" if inline is None else "".join(
                    node.text or "" for node in inline.iter(f"{{{MAIN_NS}}}t")
                )
            elif value_node is None:
                value = None
            else:
                raw = value_node.text or ""
                if cell_type == "s":
                    value = shared[int(raw)]
                elif cell_type == "b":
                    value = raw == "1"
                elif cell_type in {"str", "e"}:
                    value = raw
                else:
                    value = _parse_number(raw)
            cells[index] = value
        parsed_rows[excel_row] = cells

    width = max_column + 1
    rows = [
        [parsed_rows.get(excel_row, {}).get(index) for index in range(width)]
        for excel_row in range(1, max_row + 1)
    ]
    return WorksheetData(rows=rows)
