import zipfile
import urllib2
import sys
import getopt
import os

def download_file(url, file_name):
    """
    Helper method that downloads a file from url into file_name and displays
    a progress bar during download
    Source: http://stackoverflow.com/a/22776
    """
    try:
        u = urllib2.urlopen(url)
    except urllib2.HTTPError:
        print 'File not found at: %s' % url
        sys.exit(2)

    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    f = open(file_name, 'wb')
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()

def get_args(argv, source_url=None, header_url=None, dem_files=None, target=None):
    """
    Parases any custom arguments from the command line, reverting to the the default if none passed
    Returns a (source_url, header_url, dem_files, target) pair of arguments.
    """

    try:
        options, args = getopt.getopt(argv, 's:h:d:t:', ['source-url=','header-url=','dem-files=','target='])
    except getopt.GetoptError:
        print 'download_data.py -s <sourceurl> -h <headerurl> -d <demfiles> -t <target>'
        print '  -s, --source-url:   The root URI folder that contains the dem files'
        print '  -h, --header-url:   The root URI folder that contains the dem files'
        print '  -d, --dem-files:    A comman separated list of DEM files that we wish to download (e.g. a10g,f10h)'
        print '  -t, --target:       The target folder to download source and header files into'
        sys.exit(2)

    for opt, val in options:
        if opt in ['-s', '--source-url']:
            source_url = val
        if opt in ['-h', '--header-url']:
            header_url = val
        elif opt in ['-d', '--dem-files']:
            dem_files = val
        elif opt in ['-t', '--target']:
            target = val
            if not os.path.isdir(target):
                print '--target path does not exist or is not a valid folder: %s' % target
                sys.exit(2)

    return (source_url, header_url, dem_files, target)
        
def download_and_extract(source_url, header_url, dem_files, target):
    """
    Download each dem file from the source and extract it
    """

    for dem_file in dem_files.split(','):
        # download source file
        full_source_url = '%s%s.zip' % (source_url, dem_file)
        source_file_name = full_source_url.split('/')[-1]
        source_file_path = os.path.join(target, source_file_name)
        download_file(full_source_url, source_file_path)

        # download header file
        full_header_url = '%s%s.hdr' % (header_url, dem_file)
        header_file_name = full_header_url.split('/')[-1]
        header_file_path = os.path.join(target, header_file_name)
        download_file(full_header_url, header_file_path)

        # extract the source file
        try:
            zf = zipfile.ZipFile(source_file_path, 'r')
        except zipfile.BadZipfile:
            print 'Invalid zip file provided at: %s' % url
            sys.exit(2)
        else:
            zf.extractall(target)
            zf.close()

        # remove the source file
        os.remove(source_file_path)



if __name__ == '__main__':
    args = get_args(sys.argv[1:],
        source_url='http://www.ngdc.noaa.gov/mgg/topo/DATATILES/elev/',
        header_url='http://www.ngdc.noaa.gov/mgg/topo/elev/esri/hdr/',
        dem_files='a10g',
        target=''
    )
    download_and_extract(*args)
