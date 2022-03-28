import argparse
import os


def exiftool(filename):
    """
    Run exiftool against the file
    :param filename: the path to the file
    :return: string output
    """
    result = os.system(".\\tools\\exiftool.exe " + "\"" + filename + "\"")
    return result
    # todo


def jhead(filename):
    """
    Run jhead against the file. Requires the file be a JPEG
    :param filename: the path to the file
    :return: string output
    """
    return 'jhead'
    # todo


def pdfinfo(filename):
    """
    Run pdfinfo against the file. Requires the file be a PDF
    :param filename: the path to the file
    :return: string output
    """
    return 'pdfinfo'
    # todo


def origami(filename):
    """
    Run origami against the file. Requires the file be a PDF
    :param filename: the path to the file
    :return: string output
    """
    return 'origami'
    # todo


def main():
    """
    Parse the commandline arguments and run the appropriate tools
    :return: None
    """
    parser = argparse.ArgumentParser(description='idk run tools against a file')  # todo better description
    parser.add_argument('files', metavar='file', nargs='+', help='paths to files to analyze')
    parser.add_argument('-e', '--exiftool', action='store_true', help='run exiftool against the files')
    parser.add_argument('-j', '--jhead', action='store_true', help='run jhead against the files')
    parser.add_argument('-p', '--pdfinfo', action='store_true', help='run pdfinfo against the files')
    parser.add_argument('-o', '--origami', action='store_true', help='run origami against the files')
    parser.add_argument('-a', '--all', action='store_true', help='run all applicable tools against the files (default)')
    parser.add_argument('--out', help='A file to save the output to')
    args = parser.parse_args()
    out_str = 'Results from coalescence toolkit:\n'

    if not args.exiftool and not args.jhead and not args.pdfinfo and not args.origami and not args.all:
        args.all = True  # if no tools are chosen, run all of them

    first = True
    for filename in args.files:
        # Add a separator if needed
        if len(args.files) > 1 and not first:
            print('*' * 100)
            out_str += '*' * 100 + '\n'
        first = False

        print(f'\nAnalysis of {filename}:\n')
        out_str += f'\nAnalysis of {filename}:\n\n'

        # check if the file exists
        if not os.path.exists(filename):
            print(f'Could not find the file "{filename}"\n{"-"*100}')
            out_str += f'Could not find the file "{filename}"\n{"-"*100}\n'
            continue

        # todo check for filetype
        """
        We could add a function that uses os.path.splitext() to get the file extension
        but also could mix in mimetypes.guess_extension() and check to see if they
        match, and maybe output that the file extension has been attempted to be hidden. 
        Once this is determined the program will change what tools are ran against the 
        file. Just an idea though.
        """

        # exiftool
        if args.exiftool or args.all:
            print('Running exiftool...')
            out_str += 'Results from exiftool:\n'
            try:
                res = exiftool(filename)
                print(res)
                out_str += res + '\n'
            except Exception as e:
                print(f'exiftool ran into error: {e}')
                out_str += f'exiftool ran into error: {e}\n'
            finally:
                print('-' * 100)
                out_str += '-' * 100 + '\n'

        # jhead
        if args.jhead or args.all:
            print('Running jhead...')
            out_str += 'Results from jhead:\n'
            try:
                res = jhead(filename)
                print(res)
                out_str += res + '\n'
            except Exception as e:
                print(f'jhead ran into error: {e}')
                out_str += f'jhead ran into error: {e}\n'
            finally:
                print('-' * 100)
                out_str += '-' * 100 + '\n'

        # pdfinfo
        if args.pdfinfo or args.all:
            print('Running pdfinfo...')
            out_str += 'Results from pdfinfo:\n'
            try:
                res = pdfinfo(filename)
                print(res)
                out_str += res + '\n'
            except Exception as e:
                print(f'pdfinfo ran into error: {e}')
                out_str += f'pdfinfo ran into error: {e}\n'
            finally:
                print('-' * 100)
                out_str += '-' * 100 + '\n'

        # origami
        if args.origami or args.all:
            print('Running origami...')
            out_str += 'Results from origami:\n'
            try:
                res = origami(filename)
                print(res)
                out_str += res + '\n'
            except Exception as e:
                print(f'origami ran into error: {e}')
                out_str += f'origami ran into error: {e}\n'
            finally:
                print('-' * 100)
                out_str += '-' * 100 + '\n'

    # save the output
    if args.out:
        print(f'Saving to {args.out}...')
        try:
            with open(args.out, 'w') as f:
                f.write(out_str)
            print('Saved')
        except Exception as e:
            print(f'An error occurred while saving the file: {e}')


if __name__ == '__main__':
    main()
