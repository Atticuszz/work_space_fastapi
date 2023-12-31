import shutil
import zipfile
from pathlib import Path

from fastapi import HTTPException


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
    assert original_dir.is_dir(), f"原文件夹{original_dir}不存在"

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


def unzip_file(zip_file: Path, password: str = None) -> Path:
    """
    解压zip_file到当前目录,并创建bill_csv文件夹，将解压后的文件移动到bill_csv文件夹下
    """
    bill_dir: Path = Path(__file__).cwd()
    target_file: Path | None = None
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
            target_file = bill_dir / "bill_csv" / "alipay_bill.csv"
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
            target_file = bill_dir / "bill_csv" / "wechat_bill.csv"
    except RuntimeError as e:
        print(e)
        raise HTTPException(status_code=400, detail="Wrong password")

    finally:

        # 删除源文件，使用pathlib库
        Path.unlink(zip_file)
    return target_file
