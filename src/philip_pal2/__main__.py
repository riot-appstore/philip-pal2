# Copyright (c) 2019 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""packet init for PHiLIP PAL
This exposes a main function to run the packet from CLI
"""
import argparse
import logging

from philip_pal2 import Phil
from philip_pal2.philip_cli import show_pinout


def main():
    """Main function to allow direct exec of philip_pal package from CLI."""
    parser = argparse.ArgumentParser(prog="python3 -m philip_pal")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable more output"
    )
    parser.add_argument(
        "--dut-reset", action="store_true", help="Reset device-under-test (DUT)"
    )
    parser.add_argument(
        "--show-pinout", default=None, help="Shows the pinout 1=bluepill, 0=nucleo"
    )
    parser.add_argument("--reset", action="store_true", help="Reset PHiLIP MCU")
    parser.add_argument(
        "--fw", "-f", action="store_true", help="Gets the firmware version"
    )
    parser.add_argument(
        "port", action="store", type=str, nargs="?", help="PHiLIP serial port"
    )
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    logging.info("Connect to PHiLIP")
    if args.port:
        logging.info(". on port: %s", args.port)
        philip = Phil(args.port)
    else:
        philip = Phil()

    if args.fw:
        rev = philip.read_reg("sys.fw_rev")
        print('{"version": "%r.%r.%r"}' % (rev[3], rev[2], rev[1]))
    if args.reset:
        logging.info(". reset")
        philip.soft_reset()
    if args.dut_reset:
        logging.info(". dut reset")
        philip.dut_reset()
    if args.show_pinout is not None:
        show_pinout(args.show_pinout)


main()
