import argparse
import os
import subprocess


def exiftool(filename):
    """
    Run exiftool against the file
    :param filename: the path to the file
    :return: string output
    """
    result = subprocess.run(("exiftool", "--ExifToolVersion", "--Directory", "--FileType", "--MimeType", filename), capture_output=True, text=True).stdout
    return result


def filetype(filename):
    """
    Run exiftool against the file to get the filetype only
    :param filename: the path to the file
    :return: string output
    """
    exifType = subprocess.run(("exiftool", "-b", "-FileTypeExtension", filename), capture_output=True, text=True).stdout
    osType = ((os.path.splitext(filename))[1])[1:]
    if exifType.lower() == osType.lower():
        print("Filetype not mismatched")
    else:
        print("!!! Filetype mismatched, the document is labeled " + osType + " but is actually " + exifType + " !!!")
    print()
    return exifType


def jhead(filename):
    """
    Run jhead against the file. Requires the file be a JPEG
    :param filename: the path to the file
    :return: string output
    """
    result = subprocess.run(("jhead", filename), capture_output=True, text=True).stdout
    return result


def pdfinfo(filename):
    """
    Run pdfinfo against the file. Requires the file be a PDF
    :param filename: the path to the file
    :return: string output
    """
    result = subprocess.run(("pdfinfo", filename), capture_output=True, text=True).stdout
    yn = input("Do you wish to see the file's metadata?")
    if(yn=="y" or yn=="yes" or yn=="Yes" or yn=="YES"):
        result += subprocess.run(("pdfinfo", "-meta", filename), capture_output=True, text=True).stdout
        return result
    else:
        return result

def origami(filename):
    """
    Run origami against the file. Requires the file be a PDF
    :param filename: the path to the file
    :return: string output
    """
    result = subprocess.run(('pdfcop', filename), capture_output=True, text=True).stdout
    return result


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

        file_type = filetype(filename)

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
        if args.jhead or (args.all and file_type == 'JPG'):
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
        if args.pdfinfo or (args.all and file_type == 'PDF'):
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
        if args.origami or (args.all and file_type == 'PDF'):
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
