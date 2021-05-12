# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
import csv

def average_of_list(num_list):
    avg = sum(num_list) / len(num_list)
    return avg

def ease_csv_exporter():
    card_ids_factors = {
        x[0]: {'ease_factor': x[1]/10, 'note_id': x[2]}
        for x in mw.col.db.all("select id, factor, nid from cards")}

    notes_ids_tags = {
        x[0]: {'tags':
               list(filter(None, x[1].split(' ')))}
        for x in mw.col.db.all("select id, tags from notes")}

    for card_id, card_vals in card_ids_factors.items():
        card_note_id = card_vals['note_id']
        note_id = card_ids_factors[card_id]['note_id']
        card_ids_factors[card_id]['tags'] = notes_ids_tags[note_id]['tags']

    tag_analysis_dict = {}

    for card_id, card_vals in card_ids_factors.items():
        tag_list = card_vals['tags']
        ease_factor = card_vals['ease_factor']
        for tag in tag_list:
            try:
                tag_analysis_dict[tag]['ease_factors'].append(ease_factor)
            except(KeyError):
                tag_analysis_dict[tag] = {'ease_factors': [ease_factor]}

    final_dict_analysis = {
        tag: {
            'count': len(tag_vals['ease_factors']),
            'ease_factor_average': average_of_list(tag_vals['ease_factors'])}
                                 for tag, tag_vals in tag_analysis_dict.items()}

    return(final_dict_analysis)


def button_function():
    final_dict_analysis = ease_csv_exporter()
    path, _ = QFileDialog.getSaveFileName(
        mw,
        "Export Tag Ease CSV","tag_ease_analysis.csv","CSV Files (*.csv)")
    parts = path.split('.')
    data = []
    if parts[-1] not in ['csv', 'CSV']:
        path += '.csv'
    labels = ['Tags', 'Card Counts', 'Average Ease Factor']

    with open(path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(labels)
        for key, vals in final_dict_analysis.items():
            writer.writerow([key, vals['count'], vals['ease_factor_average']])


action = QAction("Export Tags Ease CSV", mw)
qconnect(action.triggered, button_function)
mw.form.menuCol.addAction(action)
