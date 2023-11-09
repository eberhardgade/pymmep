#!/usr/bin/env python3
"""
Utilities relating to eaf transcription files.
"""
from lxml import etree
from pathlib import Path
import base58, uuid



def eaf_iterator(tx_dir="mmep-corpus/transcribed-audio", start=None, end=None):
    """
    Returns an iterator of transcription file paths.

    kwargs:
    - `tx_dir`: root directory of trannscriptions
    - `start`: from yyyymm
    - `end`: to (incl) yyyymm
    """
    txs = Path(tx_dir)
    for tx in sorted(txs.glob("**/*.eaf")):
        assert (start==None) == (end==None), "Provide both start and end year or neither"
        if start is not None and end is not None:
            txyyyymm = str(tx).split('_')[-3][:6]
            if start <= int(txyyyymm) <= end:
                yield str(tx.relative_to("."))
        else:
            yield str(tx.relative_to("."))




def get_tiers(eaf, tx_only=False, language=None):
    """
    Return Tier elems from eaf tree.

    kwargs:
    - `tx_only`: return only transcription tiers
    - `language`: return tier of language (not implemented)
    """
    if tx_only:
        return eaf.findall("TIER[@LINGUISTIC_TYPE_REF='default-lt']")
    else:
        return eaf.findall("TIER")




def parse_eaf(eaf_path):
    """
    Returns eaf etree object from the eaf_path.
    """
    parser = etree.XMLParser(remove_blank_text=True)
    return  etree.parse(eaf_path, parser).getroot()




def write_eaf(eaf, eaf_path):
    """
    Writes eaf tree (`eaf`) to file (`eaf_path`).
    """
    b = etree.tostring(
        eaf, pretty_print=True, encoding="utf-8", xml_declaration=True
    )
    f = open(eaf_path, "wb")
    f.write(b)




def get_time_slots(eaf):
    """
    Return time_slot elems from eaf tree.
    
    Input: lxml.etree._Element from get.root(); as delivered by parse_eaf() in this module
    Output: [lxml.etree._Element], Elements with tag TIME_SLOT
    """
    return eaf.findall('TIME_ORDER/TIME_SLOT')




def make_time_slot_dictionary(time_slot_list):
    """
    Takes a list of time slots and returns a dictionary containing their IDs as keys and time values in milliseconds as values.
    
    Input: [lxml.etree._Element] with tag TIME_SLOT and attributes 'TIME_SLOT_ID' and 'TIME_VALUE'; as delivered by get_time_slots() in this module
    Output: {'ID': Value}
    - Keys are strings
    - Values are ints
    """
    
    time_slot_dictionary = {}

    for time_slot in time_slot_list:
        time_slot_dictionary[time_slot.attrib['TIME_SLOT_ID']] = int(time_slot.attrib['TIME_VALUE'])
        
    return time_slot_dictionary  




def xml_formatted_uuid():
    """
    Generate a UUID and return it prepended with "i-" and formatted as a string
    so it can be used as an annotation ID (valid xml)
    """
    return f"i-{str(base58.b58encode(uuid.uuid4().bytes), 'UTF8')}"
