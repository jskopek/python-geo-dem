import zipfile
import urllib2
import sys
import getopt

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

def get_args(argv, source=None, dem_files=None):
    """
    Parases any custom arguments from the command line, reverting to the the default if none passed
    Returns a (source, dem_files) pair of arguments.
    """

    try:
        options, args = getopt.getopt(argv, 's:d:', ['source_url=','dem_files='])
    except getopt.GetoptError:
        print 'download_data.py -s <source_url> -d <dem_files>'
        print '  -s, --source_url: The root URI folder that contains the dem files'
        print '  -d, --dem_files:  A comman separated list of DEM files that we wish to download (e.g. a10g,f10h)'
        sys.exit(2)

    for opt, val in options:
        if opt in ['-s', '--source_url']:
            source = val
        elif opt in ['-d', '--dem_files']:
            dem_files = val

    return (source, dem_files)
        
def download_and_extract(source, dem_files):
    """
    Download each dem file from the source and extract it
    """

    for dem_file in dem_files.split(','):
        url = '%s%s.zip' % (source, dem_file)
        file_name = url.split('/')[-1]
        download_file(url, file_name)

        try:
            zf = zipfile.ZipFile(file_name, 'r')
        except zipfile.BadZipfile:
            print 'Invalid zip file provided at: %s' % url
            sys.exit(2)

        zf.extractall()



if __name__ == '__main__':
    source, dem_files = get_args(sys.argv[1:],
        source='http://www.ngdc.noaa.gov/mgg/topo/DATATILES/elev/',
        dem_files='a10g'
    )
    download_and_extract(source, dem_files)
