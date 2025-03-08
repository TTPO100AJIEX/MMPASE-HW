import typing

import tqdm

def extract_call_contents(event_log_list: typing.List[dict], call_name_substring: str) -> typing.List[dict]:
    open_starts = 0
    call_number = 0
    log_list_filt = [ ]
    for event in tqdm.tqdm(event_log_list):
        event_name = event['concept:name']

        if event_name.endswith(call_name_substring):
            if event_name == f"Start:{call_name_substring}":
                open_starts += 1
            else:
                assert event_name == f"End:{call_name_substring}"
                open_starts -= 1
                if open_starts == 0:
                    log_list_filt.append({ **event, 'case:concept:name': str(call_number) })
                    call_number += 1

        if open_starts != 0:
            log_list_filt.append({ **event, 'case:concept:name': str(call_number) })

    assert open_starts == 0
    return log_list_filt
