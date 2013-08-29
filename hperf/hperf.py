#!/usr/bin/env python
# encoding: utf-8
'''
hperf -- Simple CLI to measure the performance of your web page.
@author:     cltorres@us.ibm.com
'''
import sys
import browser
import benchmarks
from argparse import ArgumentParser

__all__ = []
__version__ = 0.1
__date__ = '2013-06-05'
__updated__ = '2013-06-05'


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg

    def __str__(self):
        return self.msg

    def __unicode__(self):
        return self.msg


def setup_argument_parser(program_license):
    '''Configures the argument parser'''
    parser = ArgumentParser(description=program_license)
    parser.add_argument("urls", metavar="urls", nargs='+')
    parser.add_argument("-v", "--verbose", dest="verbose", action="count",
                        help="set verbosity level")
    parser.add_argument("-S", "--suite", dest="suite", action="store_true",
                        help="Switch to interpret urls as suite configuration")
    parser.add_argument("-b", "--browser", choices=['chrome', 'firefox'],
                        default="chrome",
                        help="Browser to use [default: %(default)s]")
    parser.add_argument("-s", "--samples", type=int, dest="num_samples",
                        help="Set number of samples [default: %(default)s]",
                        metavar="N", default=1)
    parser.add_argument("-u", "--user_agent", dest="user_agent",
                        help="Set HTTP User-Agent [default: browser's default]")
    parser.add_argument("--nocache", action='store_true',
                        help="Disables browser caching", default=False)
    parser.add_argument("-B", "--beacon", dest="beacon",
                        help="HAR beacon")

    return parser


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_license = ''' Created by cltorres@us.ibm.com'''

    try:
        parser = setup_argument_parser(program_license)
        args = parser.parse_args()
        urls = args.urls
        verbose = args.verbose

        if verbose > 0:
            print("Verbose mode on")

        driver = browser.Browser(args.browser, cache_enabled=(not args.nocache))

        for url in urls:
            bench = benchmarks.Benchmark(driver, url, args.num_samples)
            url_samples = bench.samples

    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        try:
            if driver:
                driver.close()
        except Exception, ex:
            pass

        return 0
    # except Exception, exception:
    #     try:
    #         if driver:
    #             driver.close()
    #     except Exception, ex:
    #         pass
    #     indent = len(program_name) * " "
    #     sys.stderr.write(program_name + ": " + repr(exception) + "\n")
    #     sys.stderr.write(indent + "  for help use --help\n")
    #     return 2
    else:
        driver.close()
        return 0


if __name__ == "__main__":
    sys.exit(main())
