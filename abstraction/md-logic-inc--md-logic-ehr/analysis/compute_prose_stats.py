#!/usr/bin/env python3
"""Compute accurate prose word count excluding inline JSON schemas."""

prose_paragraphs = [
    "MD Logic export will be in the following format.",
    "Upon requesting details on a patient you will be sent an email that contains a direct link to download the requested data.",
    "Upon clicking on this link you will be directed to a page where you can download a zip file. This zip file will contain all the documents in the requested patient's record.",
    'Included in this export file there will be a file with the name "manifest.json"',
    "This file will be a standard JSON File that follows the following schema",
    "If you need a full export of all, please contact mdlogic support. As this can be an extremely large amount of data, special arrangements will need to be made to deliver the data.",
    "You will recive a collection of ZipFiles, each of these is structurally identical to the individual patient export.",
    "Allong with the zip files you will provided with a manifest file. This manifest file includes demographic information about each patient along with information as to which zip file belongs to each patient. It will follow the schema below.",
]

total = sum(len(p.split()) for p in prose_paragraphs)
print(f"Prose paragraphs (excluding schema blocks): {len(prose_paragraphs)}")
print(f"Prose word count: {total}")

# Note spelling errors in original
errors = {
    "recive": "receive",
    "Allong": "Along",
    "Descripton": "Description (in schema field name)",
}
print("\nSpelling errors in documentation:")
for wrong, right in errors.items():
    print(f"  '{wrong}' → should be '{right}'")

