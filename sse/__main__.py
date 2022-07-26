from .stock import overview,profile
from .bond import kzhgszq
import argparse

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('product', help='产品，stock, bond', nargs='?', default='stock')
    parser.add_argument('cmd', help='Command', nargs='?', default='overview')
    parser.add_argument('--overview', nargs='?', help='成交概况 20220329')
    parser.add_argument('--profile', nargs='?', help='证券基础资料')
    parser.add_argument('--product_code', nargs='?', default='01,02,03,11,17', help='产品代码 01 A股, 02 B股, 03 科创, 11 股票回购, 17 汇总股票')
    args=parser.parse_args()

    if args.product == 'stock':
        if args.profile:
            profile(args.profile)
        elif args.overview:
            overview(args.overview, args.product_code)
