from pathlib import Path

import pandas as pd


def strip_in_data(df: pd.DataFrame):
    """
    Strip whitespace in column names and values.
    Args:
        df:

    Returns:

    """
    # Common data cleaning
    df.columns = df.columns.str.strip()
    df = df.map(
        lambda x: x if not isinstance(
            x, str) else x.strip())
    return df


def read_and_filter(csv_path: Path) -> pd.DataFrame:
    """
    Read and filter csv file.
    Args:
        csv_path:

    Returns:

    """
    tar_cols = [
        'Transaction_Time',
        'Transaction_Partner',
        'Primary_Category',
        'Secondary_Category',
        'Product',
        'Amount',
        'Order_id'
    ]

    if csv_path.name.startswith("wechat"):
        csv_df = pd.read_csv(csv_path, header=16, encoding='utf-8')
        csv_df = strip_in_data(csv_df)
        order_id_key = '交易单号'
        Transaction_Time_key = '交易时间'
        product_key = '商品'
        amount_key = '金额(元)'  # 有英文括号
        condition = (
                            csv_df['收/支'] == '支出') & (csv_df['当前状态'].isin(['支付成功', '已转账', '对方已收钱']))
    else:
        csv_df = pd.read_csv(csv_path, encoding='gbk', skiprows=4).iloc[:-7]
        csv_df = strip_in_data(csv_df)
        order_id_key = '交易号'
        Transaction_Time_key = '付款时间'
        product_key = '商品名称'
        amount_key = '金额（元）'  # 有中文括号
        condition = ~csv_df['交易状态'].isin(['交易失败', '交易关闭', '退款成功'])
    mappings = {
        '交易对方': 'Transaction_Partner',
        product_key: 'Product',
        order_id_key: 'Order_id',
    }

    # Filter
    csv_df = csv_df[condition]

    # Type conversion
    csv_df['Transaction_Time'] = csv_df[Transaction_Time_key].astype(
        'datetime64[ns]')

    if csv_df[amount_key].dtype == 'object':
        csv_df['Amount'] = csv_df[amount_key
        ].str.replace('¥', '').astype('float64')
    else:
        csv_df['Amount'] = csv_df[amount_key]

    csv_df['Primary_Category'] = ''
    csv_df['Secondary_Category'] = ''

    csv_df = csv_df.rename(columns=mappings)
    return csv_df[tar_cols]
