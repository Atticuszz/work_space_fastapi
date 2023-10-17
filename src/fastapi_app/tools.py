# coding=utf-8

__all__ = ["del_blank", "entries_sort_key"]


def del_blank(old_str: str) -> str:
    """
    del blank in string
    """
    return old_str.replace(" ", '')


def entries_sort_key(
        entry: dict
) -> tuple[int, ...]:
    """
    entry[‘date'] = "2023-10-1"
    entry['slot'] = "19:00-20:00"
    big date,slot forward
    """
    # print(entry)
    stat_time: list[int] = [0, 0]
    end_time: list[int] = [0, 0]
    clean_date: str = del_blank(entry["date"])
    clean_slot: str = del_blank(entry["slot"])
    date: list[int] = [
        int(digit) for digit in clean_date.split('-')]
    slot: list[str] = clean_slot.replace(
        '：', ':').split('-')
    if len(slot) and slot[0]:
        stat_time = [int(digit) for digit in slot[0].split(':') if digit != '']
    elif len(slot) > 1:
        end_time = [int(digit) for digit in slot[1].split(':')]
    # print(date)
    # print(slot)
    # print(stat_time, end_time)
    cmp_key: tuple[int, ...] = (*date, *stat_time, *end_time)
    return cmp_key
