# coding=utf-8
# coding=utf-8
# 导入所需的库
import shutil
import zipfile
from pathlib import Path

__all__ = ["del_blank", "entries_sort_key"]

from fastapi import HTTPException


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


def move_and_rename_files(
        original_dir: Path,
        target_dir: Path,
        new_name: str,
        if_delete: bool = False
):
    """
    将文件夹中的所有csv文件移动到目标文件夹，并重命名。
    Args:
        target_dir:
        original_dir:
        new_name:
        if_delete: if delete the original folder (folder_path)
    Returns:

    """
    assert original_dir.is_dir(), "原文件夹不存在"

    for item in original_dir.glob('*.csv'):
        # 构建新文件名和目标路径
        if not new_name.endswith('.csv'):
            new_name += '.csv'
        item = item.rename(new_name)
        target_path: Path = target_dir

        target_path.mkdir(exist_ok=True)
        # 如果目标路径下已经存在同名文件，则删除
        old_file = target_path.joinpath(new_name)
        if old_file.exists():
            old_file.unlink()
        # 移动和重命名文件
        shutil.move(item, target_path)
    if if_delete:
        # 删除原文件夹
        original_dir.rmdir()


def move_files_from_folder_to_directory(
        folder_path: Path,
        target_directory: Path):
    """
    将文件夹中的所有文件和子文件夹移动到目标目录，并删除原文件夹。
    """
    # 遍历文件夹中的所有文件和子文件夹
    for item in folder_path.iterdir():
        # 构建目标路径
        target_path = target_directory / item.name

        # 移动文件或文件夹
        shutil.move(str(item), str(target_path))

    # 删除原文件夹
    folder_path.rmdir()


def unzip_file(zip_file: Path, password: str = None):
    """
    解压zip_file到当前目录
    """
    bill_dir: Path = Path(__file__).cwd()
    assert zip_file.exists(), "zip_file not exists"
    try:
        if not password:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(bill_dir)
            move_and_rename_files(
                original_dir=bill_dir,
                target_dir=bill_dir / "bill_csv",
                new_name="alipay_bill",
            )
            print(f"Successfully extracted {zip_file.name} to {bill_dir}")
        else:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.setpassword(bytes(password, 'utf-8'))
                zip_ref.extractall(bill_dir)
            # 移动文件

            move_and_rename_files(
                original_dir=bill_dir / zip_file.stem,
                target_dir=bill_dir / "bill_csv",
                new_name="wechat_bill",
                if_delete=True
            )
            print(
                f"Successfully extracted {zip_file.name} to {bill_dir} with password")
    except RuntimeError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Wrong password")

    finally:

        # 删除源文件，使用pathlib库
        Path.unlink(zip_file)
