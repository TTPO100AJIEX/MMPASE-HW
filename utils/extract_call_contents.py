import typing

import tqdm

def extract_call_contents(event_log_list: typing.List[dict], call_name_substring: str) -> typing.List[dict]:
    open_starts = 0
    call_number = 0
    log_list_filt = [ ]
    for event in tqdm.tqdm(event_log_list):
        event_name = event['concept:name']

        if call_name_substring in event_name:
            if event_name.startswith("Start:"):
                open_starts += 1
            else:
                assert event_name.startswith("End:")
                open_starts -= 1
                if open_starts == 0:
                    call_number += 1

        if open_starts != 0:
            log_list_filt.append({ **event, 'case:concept:name': str(call_number) })

    assert open_starts == 0
    return log_list_filt
