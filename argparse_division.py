import argparse

parser = argparse.ArgumentParser(description='Argparse tutorial')

argument_display_name = 'nums'
help_info_display = 'Pass two numbers for division'

parser.add_argument(argument_display_name,
                    help=help_info_display, type=int, nargs=2)
                    
# nargs takes '+' for 1 or more arguments, or specified number of arguments needed (int)

args = parser.parse_args()

if args.nums:
    # args.nums is a list, so we can acess numbers by indexes
    print(args.nums[0] // args.nums[1])
