import argparse
from simulate import Simulator
from parse import Parser
import json

parser = argparse.ArgumentParser(description='LTSpice Simulation Wrapper')
parser.add_argument('filename', metavar='F', type=str,
                    help='the filename to run the simulation on')
parser.add_argument('--executable',
                    action='store',
                    dest='executable',
                    default='/Applications/LTspice.app/Contents/MacOS/LTspice',
                    help='the LTSpice executable')
parser.add_argument('--output',
                    action='store',
                    dest='output',
                    default='output.json',
                    help='the JSON output file')
parser.add_argument('--params',
                    action='store',
                    dest='params',
                    default=None,
                    help='the JSON parameters dictionary')
parser.add_argument('--wine',
                    action='store',
                    dest='wine',
                    default=False,
                    help='the JSON parameters dictionary')

args = parser.parse_args()
simulator = Simulator(args.executable, is_wine=args.wine)

parsed_params = None
if args.params is not None:
    with open(args.params) as data_file:
        parsed_params = json.load(data_file)

raw_output = simulator.simulate(args.filename, params=parsed_params)

parser = Parser()
parser.parse('sample.raw')

with open('sample.json', "w") as output:
    output.write(parser.serialize())
