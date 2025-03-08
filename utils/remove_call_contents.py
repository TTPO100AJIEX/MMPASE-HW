import typing

import tqdm

def remove_call_contents(
    event_log_list: typing.List[dict],
    call_name_substring: str,
    keep_call: bool = True
) -> typing.List[dict]:
    open_starts = 0
    log_list_filt = [ ]
    for event in tqdm.tqdm(event_log_list):
        event_name = event['concept:name']
        if call_name_substring in event_name:
            if event_name.startswith("Start:"):
                open_starts += 1
            else:
                assert event_name.startswith("End:")
                open_starts -= 1
                if (keep_call) and (open_starts == 0):
                    log_list_filt.append({ **event, 'concept:name': f"Call:{event_name[len('End:'):]}" })
        else:
            if open_starts == 0:
                log_list_filt.append(event)

    assert open_starts == 0
    return log_list_filt
