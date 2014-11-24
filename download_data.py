from zipfile import ZipFile
import urllib2

SOURCE = 'http://www.ngdc.noaa.gov/mgg/topo/DATATILES/elev/'
DEM_FILES = 'a10g'

def download_file(url, file_name):
    # Source: http://stackoverflow.com/a/22776
    u = urllib2.urlopen(url)
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

if __name__ == '__main__':
    for dem_file in DEM_FILES.split(','):
        url = '%s%s.zip' % (SOURCE, DEM_FILES)
        file_name = url.split('/')[-1]
        download_file(url, file_name)

        with ZipFile(file_name, 'r') as zf:
            zf.extractall()



