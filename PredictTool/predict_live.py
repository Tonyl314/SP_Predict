from CompileGamestates import CompileGamestatesToDataframe
import pickle
import pandas as pd
import numpy as np
from time import time
import sklearn
def get_prediction(gamestate):
    with open('sp_predict.pkl', 'rb') as pickler:
        sp_predict = pickle.load(pickler)
    with open('predict_scaler.pkl', 'rb') as pickler:
        scaler = pickle.load(pickler)
    gamestate_data = gamestate[["bug_avail", "da_avail", "swap_avail", "inspect_avail", "seduce_avail", "purloin_avail", "fp_avail",
                                            "micro_avail", "guest_count", "reqmissions",
                                            "elapsed", "spytime", "lowlight", "neutral", "highlight", "flirt", "flirt_cd", "lowlights",
                                            "highlights", "print_count", "difficult_attempts", "difficults_succeeded", "inspects",
                                            "case_prints", "statue_prints", "drink_prints", "book_prints",
                                            "bugs_attempted", "bb_count", "micro_progress", "green_purloin", "delegate_purloin", "green_swap",
                                            "purloin_pend", "delegate_avail", "swap_pend",
                                            "missions_bug", "missions_da", "missions_swap", "missions_inspect", "missions_seduce", "missions_purloin",
                                            "missions_fp", "missions_micro", "conversation", "statue", "elsewhere",
                                            "has_book", "has_drink", "sips_count", "has_case", "timeadd_count", "countdown", "countdown_elapsed",
                                            "Aquarium", "Ballroom", "Courtyard", "Gallery", 
                                            "High-Rise", "Library", "Moderne", "Pub", "Redwoods", "Teien", "Terrace", "Veranda",
                                            'since_bug', 'since_da', 'since_swap', 'since_inspect', 'since_seduce', 'since_purloin', 'since_fp',
                                            'since_micro', 'since_bb', 'since_light', 'since_statue', 'since_MFanim', 'since_delegate', 'since_print',
                                            'since_bugattempt', 'since_timeadd', 'green_timeadds', 'red_timeadds', 'green_bbs', 'coughs']]
    gamestate_data_reshaped = gamestate_data.values.reshape(1, -1)
    gamestate_data = scaler.transform(gamestate_data_reshaped)

    return str(sp_predict.predict_proba(gamestate_data)), gamestate['elapsed'], gamestate['uuid']
def encode_missing_variables(gamestates):
    encode_list = ['lowlight', 'highlight', 'neutral', "Aquarium", "Ballroom", "Courtyard", "Gallery", 
                "High-Rise", "Library", "Moderne", "Pub", "Redwoods", "Teien", "Terrace", "Veranda","conversation", "statue", "elsewhere"]
    for x in encode_list:
        gamestates[x] = 0
        gamestates.loc[gamestates['venue'] == x, x] = 1
        gamestates.loc[gamestates['light'] == x, x] = 1
        gamestates.loc[gamestates['spy_loc'] == x, x] = 1
    return gamestates
    


def PredictLive(file):
    gamestates = CompileGamestatesToDataframe(file)
    gamestates = encode_missing_variables(gamestates)

    index_count = len(gamestates.index)
    x = 0
    probability_dict = {}
    while x < index_count:
        prediction, elapsed, uuid = get_prediction(gamestates.iloc[x])
        prediction = prediction[2:-2]
        probability_dict[elapsed] = prediction
        x += 1
    for x in probability_dict:
        length = (len(probability_dict[x]))
        halflen = int((length + 1) / 2)
        spywin = float(probability_dict[x][halflen : -1])
        spywin = spywin * 100
        spywin = "{:.2f}".format(spywin)
        probability_dict[x] = spywin


    input("Start game")
    start_time = time()
    z = 0
    while z == 0:
        if 1 < time() - start_time:
            print("3")
            z =1
    z = 0
    while z == 0:
        if 2 < time() - start_time:
            print("2")
            z =1
    z = 0
    while z == 0:
        if 3 < time() - start_time:
            print("1")
            z =1
    z = 0
    while z == 0:
        if 4 < time() - start_time:
            print("Playing it")
            z =1
    start_time = time()
    for x in probability_dict:
        y = 0
        while y == 0:
            gametime = time() - start_time
            if x < gametime:
                print("Spy win chance: " + probability_dict[x] + "%.")
                y = 1

