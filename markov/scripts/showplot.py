#!/usr/bin/env python3

"""Show a matplotlib plot that has been pickled."""

import argparse # For command line parsing.
import pickle # For reading the pickle format.
import matplotlib.pyplot as plt

if __name__ == "__main__":

    description="""Show a matplotlib plot that has been pickled."""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("matplot", metavar="MATPLOT.pickle",
                        help="The pickle file for the matplot figure")

    args = parser.parse_args()

    with open(args.matplot, 'rb') as fig_file:
        fig_handle = pickle.load(fig_file)

    fig_handle.show()
