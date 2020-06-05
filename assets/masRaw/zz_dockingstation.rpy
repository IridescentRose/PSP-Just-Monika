










default persistent._mas_pm_taken_monika_out = False


init -900 python in mas_ics:
    import os




    islands_folder = os.path.normcase(
        renpy.config.basedir + "/game/mod_assets/location/special/"
    )




    islands_nwf = (
        "0ea361ef4c501c15a23eb36b1c47bf1a8eac1b4c2a1bc214e30db9e4f154dbdc"
    )


    islands_nwof = (
        "fff96da27e029d5bab839bde8b2a00f8d484ad81880522b0e828c8a2cd0a7c97"
    )


    islands_dwf = (
        "791f379866edf72dc6fd72ae8d7b26af43dd8278b725a0bf2aeb5c72ba04a672"
    )


    islands_dwof = (
        "83963cf273e9f1939ad2fa604d8dfa1912a8cba38ede7f762d53090783ae8ca4"
    )


    islands_rwf = (
        "5854576632f76d9a99c8c69c8b4a6c2053241c0cb7550c31aa49ab0454635e36"
    )


    islands_rwof = (
        "e78eaf99bc56f22f16579c3a22f336db838d36c84ac055f193aec343deb5c9dc"
    )


    islands_nrwf = (
        "68610912a463d267d4bd74400909204b5efe2249e71b348f2cc911b79fea3693"
    )


    islands_nrwof = (
        "37e01bb69418ebb825c2955b645391a1fb99e13c76b1adb47483d6cc02c1d8e3"
    )


    islands_owf = (
        "4917416ab2c390846bdc59fa25a995d2a5be1be0ddbc3860048aef4fe670fa70"
    )


    islands_owof = (
        "4b4dc5ccfa81de15e09ee01ea7ee7ff3a5c498a5a4d660e8579dd5556599ae1b"
    )


    islands_nowf = (
        "21e8b98faafb24778df5cce17876e0caf822f314c9f80c6d63e7d2a3d68ab54a"
    )


    islands_nowof = (
        "ac6e6d09cd18aa30a8dd2e33879b0669590f303fe98c9dba8ce1b5dd0c8212ba"
    )


    islands_swf = (
        "510a7fc62321f3105c99c74fd53d06f4e20f6e4cc20d794327e3094da7a5d168"
    )


    islands_swof = (
        "262242dd67ae539bae0c7022d615696d19acb85fc7723f545a00b65aeb13be24"
    )


    islands_nswf = (
        "c426957bda7740b361bc010a2f6ddb0a8fa2a1a983da9c40249a0648117f45a9"
    )


    islands_nswof = (
        "822ed24c0250a273f6e614790a439473f638ce782e505507e617e56e85ffc17f"
    )






    islands_map = {
        "nwf": ("night_with_frame.png", islands_nwf),
        "nwof": ("night_without_frame.png", islands_nwof),
        "dwf": ("with_frame.png", islands_dwf),
        "dwof": ("without_frame.png", islands_dwof),
        "rwf": ("rain_with_frame.png", islands_rwf),
        "rwof": ("rain_without_frame.png", islands_rwof),
        "nrwf": ("night_rain_with_frame.png", islands_nrwf),
        "nrwof": ("night_rain_without_frame.png", islands_nrwof),
        "owf": ("overcast_with_frame.png", islands_owf),
        "owof": ("overcast_without_frame.png", islands_owof),
        "nowf": ("night_overcast_with_frame.png", islands_nowf),
        "nowof": ("night_overcast_without_frame.png", islands_nowof),
        "swf": ("snow_with_frame.png", islands_swf),
        "swof": ("snow_without_frame.png", islands_swof),
        "nswf": ("night_snow_with_frame.png", islands_nswf),
        "nswof": ("night_snow_without_frame.png", islands_nswof)
    }



    o31_cg_folder = os.path.normcase(
        renpy.config.basedir + "/game/mod_assets/monika/cg/"
    )


    o31_marisa = (
        "6a05463e8200af9846e7f70f4c03e6feddb6c5a93395d7b17a91a6fd23da29af"
    )


    o31_rin = (
        "c8fb05e801e0eb1f234b4af99d910e561a9afbbd1a5df6bee6edd602c94adb81"
    )






    o31_map = {
        "o31mcg": ("o31_marisa_cg.png", o31_marisa),
        "o31rcg": ("o31_rin_cg.png", o31_rin)
    }



    game_folder = os.path.normcase(
        renpy.config.basedir + "/game/"
    )



init -45 python:
    import os 


    class MASDockingStation(object):
        """
        Docking station class designed to help with file reading / writing of
        certain files.
        """
        import hashlib  
        import base64   
        from StringIO import StringIO as slowIO
        from cStringIO import StringIO as fastIO
        
        import store.mas_utils as mas_utils 
        
        
        DEF_STATION = "/characters/"
        DEF_STATION_PATH = os.path.normcase(renpy.config.basedir + DEF_STATION)
        
        
        
        READ_SIZE = 4095
        B64_READ_SIZE = 5460
        
        
        
        
        
        ERR = "[ERROR] {0} | {1} | {2}\n"
        ERR_DEL = "Failure removing package '{0}'."
        ERR_GET = "Failure getting package '{0}'."
        ERR_OPEN = "Failure opening package '{0}'."
        ERR_READ = "Failure reading package '{0}'."
        ERR_SEND = "Failure sending package '{0}'."
        ERR_SIGN = "Failure to request signature for package '{0}'."
        ERR_SIGNP = "Package '{0}' does not match checksum."
        
        
        
        
        PKG_E = 1
        
        
        PKG_F = 2
        
        
        PKG_N = 4
        
        
        PKG_C = 8
        
        
        def __init__(self, station=None):
            """
            Constructor

            IN:
                station - the path to the folder this docking station interacts
                    with. (absolute path), will try to create the folder if it
                    doesn't exist. Exceptions will be logged.
                    NOTE: END WITH '/' please
                    (Default: DEF_STATION_PATH)
            """
            if station is None:
                station = self.DEF_STATION_PATH
            
            
            
            
            self.station = os.path.normcase(station)
            self.enabled = True
            
            if not os.path.isdir(self.station):
                try:
                    os.makedirs(self.station)
                except Exception as e:
                    mas_utils.writelog(self.ERR.format(
                       self.ERR_CREATE.format(self.station),
                       str(self),
                       repr(e)
                   ))
                    self.enabled = False
        
        
        
        def __str__(self):
            """
            toString
            """
            return "DS: [{0}]".format(self.station)
        
        
        def checkForPackage(self, package_name, check_read=True):
            """
            Checks if a package exists in the docking station

            NOTE: will log exceptions

            NOTE: no signature checking

            IN:
                package_name - the filename we are lookiung for
                check_read - If False, then only check for existence
                    (Default: True)

            RETURNS:
                True if the package exists
                    If check_read is true, then package must also be readable
                False otherwise
            """
            if not self.enabled:
                return False
            
            return self._m1_zz_dockingstation__check_access(
                self._trackPackage(package_name),
                check_read
            )
        
        
        def createPackageSlip(self, package, bs=None):
            """
            Generates a checksum for a package (which is a file descriptor)

            NOTE: may throw exceptions

            NOTE: when checking packages, we read by B64_READ_SIZE always

            IN:
                package - file descriptor of the package we want
                    NOTE: is seek(0)'d after reading
                bs - blocksize to use. IF None, the default blocksize is ued
                    (Default: None)

            RETURNS:
                sha256 checksum (hexadec) of the given package, or None
                if error occured
            """
            if not self.enabled:
                return None
            
            pkg_slip = self._unpack(package, None, False, True, bs)
            
            
            package.seek(0)
            
            return pkg_slip
        
        
        def destroyPackage(self, package_name):
            """
            Attempts to destroy the given package in the docking station.

            NOTE: exceptions are logged

            IN:
                package_name - name of the package to delete

            RETURNS:
                True if package no exist or was deleted. False otherwise
            """
            if not self.enabled:
                return False
            
            if not self.checkForPackage(package_name, False):
                return True
            
            
            try:
                os.remove(self._trackPackage(package_name))
                return True
            
            except Exception as e:
                mas_utils.writelog(self.ERR.format(
                    self.ERR_DEL.format(package_name),
                    str(self),
                    repr(e)
                ))
                return False
        
        
        def getPackageList(self, ext_filter=""):
            """
            Gets a list of the packages in the docking station.
            We also ensure that the item retrieved is not a folder.

            IN:
                ext_filter - extension filter to use when getting list.
                    the '.' is added if not already given.
                    If not given, we get all the packages
                    (Default: "")

            RETURNS: list of packages
            """
            if not self.enabled:
                return []
            
            
            if len(ext_filter) > 0 and not ext_filter.startswith("."):
                ext_filter = "." + ext_filter
            
            return [
                package
                for package in os.listdir(self.station)
                if package.endswith(ext_filter)
                and not os.path.isdir(self._trackPackage(package))
            ]
        
        
        def getPackage(self, package_name):
            """
            Gets a package from the docking station

            NOTE: will log exceptions

            IN:
                package_name - The filename we are looking for

            RETURNS:
                open file descriptor to the package (READ BYTES mode)
                    if package is readable and no errors occurred
                None otherwise
            """
            if not self.enabled:
                return None
            
            
            if not self.checkForPackage(package_name):
                return None
            
            
            package_path = self._trackPackage(package_name)
            package = None
            try:
                package = open(package_path, "rb")
            
            except Exception as e:
                mas_utils.writelog(self.ERR.format(
                    self.ERR_OPEN.format(package_name),
                    str(self),
                    repr(e)
                ))
                if package is not None:
                    package.close()
                return None
            
            
            return package
        
        
        def packPackage(self, contents, pkg_slip=False):
            """
            Packs a package so it can be sent
            (encodes a data buffer into base64)

            NOTE: may throw exceptions

            IN:
                contents - the bytes buffer we want to pack. Recommened to use
                    StringIO here, but any buffer that supports read(bytes)
                    will work fine.
                    NOTE: is CLOSED after reading
                pkg_slip - True will generate a checksum for the data buffer
                    and return that as well
                    (Default: False)

            RETURNS:
                tuple of the following format:
                [0] - base64 version of the given data, in a cStringIO buffer
                [1] - sha256 checksum if pkg_slip is True, None otherwise
            """
            box = None
            try:
                box = self.fastIO()
                
                return (box, self._pack(contents, box, True, pkg_slip))
            
            except Exception as e:
                
                if box is not None:
                    box.close()
                raise e
            
            finally:
                
                contents.close()
        
        
        def safeRandom(self, amount):
            """
            Generates a random amount of unicode-safe bytes.

            IN:
                amount - number of bytes to generate
            """
            return self.base64.b64encode(os.urandom(amount))[:amount]
        
        
        def sendPackage(self,
                package_name,
                package,
                unpacked=False,
                pkg_slip=False
            ):
            """
            Sends a package into the docking station
            (Writes a file in this stations' folder)

            NOTE: exceptions are logged

            IN:
                package_name - name of the file to write
                package - the data to write as bytes
                unpacked - True means that package is not in base64
                    False means that it is in base64
                    (Default: False)
                pkg_slip - True means we should generate a sha256 checksum for
                    the package and return that
                    (Default: False)

            RETURNS:
                sha256 checksum if pkg_slip is True
                True if package was sent successfully and pkg_slip is False
                False Otherwise
            """
            if not self.enabled:
                return False
            
            mailbox = None
            try:
                
                mailbox = open(self._trackPackage(package_name), "wb")
                
                
                _pkg_slip = self._pack(package, mailbox, unpacked, pkg_slip)
                
                
                if pkg_slip:
                    return _pkg_slip
                
                
                return True
            
            except Exception as e:
                mas_utils.writelog(self.ERR.format(
                    self.ERR_SEND.format(package_name),
                    str(self),
                    str(e)
                ))
                return False
            
            finally:
                
                if mailbox is not None:
                    mailbox.close()
            
            return False
        
        
        def signForPackage(self,
                package_name,
                pkg_slip,
                keep_contents=False,
                bs=None
            ):
            """
            Gets a package, checks if all the contents are there, and then
            deletes the packaging.
            (Check if a file exists, is readable, has the checksum of the
            passed in pkg_slip, then deletes the file on disk)

            NOTE: Exceptions are logged

            IN:
                package_name - name of the file to check
                pkg_slip - sha256 checksum the file should match
                keep_contents - if True, then we copy the data into a StringIO
                    buffer and return it.
                    (Defualt: False)
                bs - blocksize to use when reading the package
                    IF None, the default blocksize is used
                    (Default: None)

            RETURNS:
                if the package matches signature:
                    - if keep_contents is True
                        StringIO buffer containing decoded data
                    - otherwise, 1 is returned
                if package found but no sig match
                    - NOTE: if this happens, we NEVER delete teh package
                    - return -2
                if package not found
                    - return -1
                0 otherwise (like if error occured)
            """
            if not self.enabled:
                return 0
            
            package = None
            contents = None
            try:
                
                package = self.getPackage(package_name)
                if package is None:
                    return -1
                
                
                if keep_contents:
                    
                    contents = slowIO()
                
                
                
                _pkg_slip = self._unpack(
                    package,
                    contents,
                    keep_contents,
                    True,
                    bs
                )
                
                
                if _pkg_slip != pkg_slip:
                    contents.close()
                    return -2
                
                
                if keep_contents:
                    return contents
                
                
                if contents is not None:
                    contents.close()
                
                package.close()
                os.remove(self._trackPackage(package_name))
                return 1
            
            except Exception as e:
                mas_utils.writelog(self.ERR.format(
                    self.ERR_SIGNP.format(package_name),
                    str(self),
                    str(e)
                ))
                if contents is not None:
                    contents.close()
                return 0
            
            finally:
                
                if package is not None:
                    package.close()
            
            return 0
        
        
        def smartUnpack(self,
                    package_name,
                    pkg_slip,
                    contents=None,
                    lines=0,
                    b64=True,
                    bs=None
            ):
            """
            Combines parts of signForPackage and _unpack in a way that is very
            useful for us

            NOTE: all exceptions are logged

            NOTE: if contents was passed in an error occurred (PKG_E will be in
                the return bits), then the contents of contents is undefined.

            IN:
                package_name - name of the package to read in
                pkg_slip - chksum to check package with (considerd PRE b64 decode)
                contents - buffer to save contents of package.
                    If None, we save contents to a StringIO object and return
                    that
                    (Default: None)
                lines - number of lines to retrieve when reading data.
                    If less than 0, then we scan the file itself to tell us
                    how many lines to read.
                    If "all", then we read ALL LINES
                    (Default: 0)
                b64 - True means the package is encoded in base64
                    (Default: True)
                bs - blocksize to use. By default, we use B64_READ_SIZE
                    (Default: None)

            RETURNS: tuple of the following format
                [0]: PKG_* bits constants highlighting success/failure status
                [1]: buffer containing the contents of the package.
                    If contents is not None, this is the same reference as
                    contents.
            """
            NUM_DELIM = "|num|"
            
            
            package = self.getPackage(package_name)
            
            
            
            if package is None:
                return (self.PKG_N, None)
            
            
            if bs is None:
                bs = self.B64_READ_SIZE
            
            
            if contents is None:
                _contents = self.slowIO()
            else:
                _contents = contents
            
            
            ret_val = self.PKG_F
            
            
            checklist = self.hashlib.sha256()
            
            
            if lines == "all":
                
                lines = 20000000
            
            try:
                
                _box = MASDockingStation._blockiter(package, bs)
                
                
                if lines < 0:
                    first_item = next(_box, None)
                    
                    if first_item is None:
                        raise Exception("EMPTY PACKAGE")
                    
                    checklist.update(first_item)
                    first_unpacked = self.base64.b64decode(first_item)
                    
                    
                    raw_num, sep, remain = first_unpacked.partition(NUM_DELIM)
                    if len(sep) == 0:
                        raise Exception(
                            "did not find sep. size of first {0}".format(
                                len(raw_num)
                            )
                        )
                    
                    num = mas_utils.tryparseint(raw_num, -1)
                    
                    if num < 0:
                        
                        raise Exception(
                            "did not find lines. found {0}".format(raw_num)
                        )
                    
                    
                    lines = num
                    
                    if lines > 0:
                        
                        _contents.write(remain)
                        lines -= 1
                
                
                
                for packed_item in _box:
                    
                    checklist.update(packed_item)
                    
                    if lines > 0:
                        
                        _contents.write(self.base64.b64decode(packed_item))
                        lines -= 1
            
            
            except Exception as e:
                mas_utils.writelog(self.ERR.format(
                    self.ERR_READ.format(package_name),
                    str(self),
                    repr(e)
                ))
                
                if contents is None:
                    
                    _contents.close()
                
                return (ret_val | self.PKG_E, None)
            
            finally:
                
                package.close()
            
            
            if checklist.hexdigest() != pkg_slip:
                
                return (ret_val | self.PKG_C, _contents)
            
            
            return (ret_val, _contents)
        
        
        def unpackPackage(self, package, pkg_slip=None):
            """
            Unpacks a package
            (decodes a base64 file into a regular StringIO buffer)

            NOTE: may throw exceptions

            IN:
                package - file descriptor of the file to decode / unpack
                    NOTE: is CLOSED after reading
                pkg_slip - sha256 hex checksum of what the package data should
                    be. If passed in, then we check this against the package
                    NOTE: generated checksum uses data BEFORE it is decoded
                    (Default: None)

            RETURNS:
                StringIO buffer containing the package decoded
                Or None if pkg_slip checksum was passed in and the given
                    package failed the checksum
            """
            if not self.enabled:
                return None
            
            contents = None
            try:
                
                contents = self.slowIO()
                
                _pkg_slip = self._unpack(
                    package,
                    contents,
                    True,
                    pkg_slip is not None
                )
                
                if pkg_slip is not None and _pkg_slip != pkg_slip:
                    
                    contents.close()
                    return None
                
                return contents
            
            except Exception as e:
                
                
                if contents is not None:
                    contents.close()
                raise e
            
            finally:
                
                package.close()
        
        
        @staticmethod
        def _blockiter(fd, blocksize):
            """
            Creates an itererator of a file using the given blocksize

            NOTE: May throw exceptions

            IN:
                fd - file descriptor
                    NOTE: seeks this to 0 before starting
                blocksize - size to use for blocks

            YIELDS:
                blocks until a block read attempt gave us nothing

            ASSUMES:
                given file descriptor is open
            """
            fd.seek(0)
            block = fd.read(blocksize)
            while len(block) > 0:
                yield block
                block = fd.read(blocksize)
        
        
        def _trackPackage(self, package_name):
            """
            Adds this docking station's path tot he package_name so we can
            access it and stuff

            IN:
                package_name - name of the package

            RETURNS:
                package_name in a valid package_path ready for checking
            """
            return os.path.normcase(self.station + package_name)
        
        
        def _pack(self, contents, box, pack=True, pkg_slip=True, bs=None):
            """
            Runs the packing algorithm for given file descriptors
            Supports:
                1. encoding and checksumming data
                    this will encode the input, checksum it, then write to
                    output
                2. encoding data
                    this will encode the input, then write to output
                3. checksumming data
                    this will checksum the input. DOES NOT WRITE to output

            NOTE: may throw exceptions
            NOTE: if both pack and pkg_slip are False, this does absoultely
                nothing

            IN:
                contents - file descriptor to read data from
                box - file descriptor to write data to
                pack - if True, encode the input data into base64 prior to
                    writing to output data
                    (Default: True)
                pkg_slip - if True, generate a checksum of the data.
                    NOTE: if pack is True, this is done using data AFTER
                        encoding
                    (Default: True)
                bs - blocksize to use. If None, we use READ_SIZE
                    (Default: None)

            RETURNS:
                generated sha256 checksum if pkg_slip is True
                Otherwise, None
            """
            if not self.enabled:
                return None
            
            if not (pkg_slip or pack):
                return None
            
            if bs is None:
                bs = self.READ_SIZE
            
            _contents = MASDockingStation._blockiter(contents, bs)
            
            if pkg_slip and pack:
                
                
                checklist = self.hashlib.sha256()
                
                for item in _contents:
                    packed_item = self.base64.b64encode(item)
                    checklist.update(packed_item)
                    box.write(packed_item)
                
                return checklist.hexdigest()
            
            elif pack:
                
                for item in _contents:
                    box.write(self.base64.b64encode(item))
            
            else:
                
                checklist = self.hashlib.sha256()
                
                for item in _contents:
                    checklist.update(self.base64.b64encode(item))
                
                return checklist.hexdigest()
            
            return None
        
        
        def _unpack(self, box, contents, unpack=True, pkg_slip=True, bs=None):
            """
            Runs the unpacking algorithm for given file descriptors
            Supports:
                1. checksumming and decoding data
                    this will checksum input, decode it, then write to output
                2. decoding data
                    this will decode the input, then write to ouput
                3. checksumming data
                    this will checksum the input. DOES NOT WRITE to output

            NOTE: may throw exceptions
            NOTE: if both unpack and pkg_slip are False, this does absolutely
                nothing

            IN:
                box - file descriptor to read data from
                contents - file descriptor to write data to
                unpack - if True, decode input data from base64 prior to
                    writing output data
                    (Default: True)
                pkg_slip - if True, genereate a checksum of the data.
                    NOTE: if unpack is True, this is done using data BEFORE
                        decoding
                    (Default: True)
                bs - blocksize to use. If None, use B64_READ_SIZE
                    (Default: None)

            RETURNS:
                generated sha256 checksum if pkg_slip is True
                Otherwise, None
            """
            if not self.enabled:
                return None
            
            if not (pkg_slip or unpack):
                return None
            
            if bs is None:
                bs = self.B64_READ_SIZE
            
            _box = MASDockingStation._blockiter(box, bs)
            
            if pkg_slip and unpack:
                
                checklist = self.hashlib.sha256()
                
                for packed_item in _box:
                    checklist.update(packed_item)
                    contents.write(self.base64.b64decode(packed_item))
                
                return checklist.hexdigest()
            
            elif pkg_slip:
                
                checklist = self.hashlib.sha256()
                
                for packed_item in _box:
                    checklist.update(packed_item)
                
                return checklist.hexdigest()
            
            else:
                
                for packed_item in _box:
                    contents.write(self.base64.b64decode(packed_item))
            
            return None
        
        def _m1_zz_dockingstation__check_access(self, package_path, check_read):
            """
            Checks access of the file at package_path.
            Also ensures that the file is not actually is folder.

            NOTE:
                will log exceptions

            IN:
                package_path - path to the file we want to check access to
                check_read - If True, check for read access in addition to
                    file existence

            RETURNS:
                True if package exists / is readable.
                Otherwise:
                    if check_read is True, returns None
                    otherwise, returns False
            """
            if not self.enabled:
                return False
            
            try:
                file_ok = os.access(package_path, os.F_OK)
                read_ok = os.access(package_path, os.R_OK)
                not_dir = not os.path.isdir(package_path)
            
            except Exception as e:
                mas_utils.writelog(self.ERR.format(
                    self.ERR_GET.format(package_path),
                    str(self),
                    repr(e)
                ))
                
                
                return self._m1_zz_dockingstation__bad_check_read(check_read)
            
            if check_read:
                if not (file_ok and read_ok and not_dir):
                    return None
            
            return file_ok and not_dir
        
        def _m1_zz_dockingstation__bad_check_read(self, check_read):
            """
            Returns an appropriate failure value givne the check_read value

            IN:
                check_read - the value of check_read

            RETURNS:
                None if check_read is True, False otherwise
            """
            if check_read:
                return None
            
            return False

    mas_docking_station = MASDockingStation()


default persistent._mas_moni_chksum = None






default persistent._mas_dockstat_checkout_log = list()
default persistent._mas_dockstat_checkin_log = list()











default persistent._mas_dockstat_moni_log = dict()


default persistent._mas_dockstat_going_to_leave = False



default persistent._mas_dockstat_moni_size = 0

default persistent._mas_bday_sbp_reacted = False





init -500 python in mas_dockstat:

    blocksize = 4 * (1024**2)
    b64_blocksize = 5592408 




    MAS_PKG_NF = 1


    MAS_PKG_F = 2


    MAS_PKG_FO = 4


    MAS_PKG_DL = 8


    MAS_PKG_DP = 16




    MAS_SBP_NONE = 1


    MAS_SBP_CAKE = 2


    MAS_SBP_BANR = 4


    MAS_SBP_BLON = 8


init -11 python in mas_dockstat:
    import store.mas_utils as mas_utils

    def decodeImages(dockstat, image_dict, selective=[]):
        """
        Attempts to decode the iamges

        IN:
            dockstat - docking station to use
            image_dict - image map to use
            selective - list of images keys to decode
                If not passed in, we decode EVERYTHINg
                (DEfault: [])

        Returns TRUE upon success, False otherwise
        """
        if len(selective) == 0:
            selective = image_dict.keys()
        
        for b64_name in selective:
            real_name, chksum = image_dict[b64_name]
            
            
            b64_pkg = dockstat.getPackage(b64_name)
            
            if b64_pkg is None:
                
                return False
            
            
            real_pkg = None
            real_chksum = None
            real_path = dockstat._trackPackage(real_name)
            
            
            try:
                real_pkg = open(real_path, "wb")
                
                
                dockstat._unpack(
                    b64_pkg,
                    real_pkg,
                    True,
                    False,
                    bs=b64_blocksize
                )
                
                
                real_pkg.close()
                real_pkg = open(real_path, "rb")
                
                
                real_chksum = dockstat.createPackageSlip(
                    real_pkg,
                    bs=blocksize
                )
            
            except Exception as e:
                mas_utils.writelog(
                    "[ERROR] failed to decode '{0}' | {1}\n".format(
                        b64_name,
                        str(e)
                    )
                )
                return False
            
            finally:
                
                b64_pkg.close()
                
                if real_pkg is not None:
                    real_pkg.close()
            
            
            if real_chksum is None:
                
                mas_utils.trydel(real_path)
                return False
            
            if real_chksum != chksum:
                
                mas_utils.trydel(real_path)
                return False
        
        
        return True


    def removeImages(dockstat, image_dict, selective=[], log=False):
        """
        Removes the decoded images at the end of their lifecycle

        IN:
            dockstat - docking station
            image_dict - image map to use
            selective - list of image keys to delete
                If not passed in, we delete everything in the image dict
                (Default: [])
            log - should we log a delete failure?
                (Default: False)

        AKA quitting
        """
        if len(selective) == 0:
            selective = image_dict.keys()
        
        for b64_name in selective:
            real_name, chksum = image_dict[b64_name]
            mas_utils.trydel(dockstat._trackPackage(real_name), log=log)


init python in mas_dockstat:
    import store
    import cPickle


    previous_vars = dict()

    def setMoniSize(tdelta):
        """
        Sets the appropriate persistent size for monika

        IN:
            tdelta - timedelta to use
        """
        
        days = tdelta.days
        secs = tdelta.seconds
        hours = (days * 24) + (secs / 3600.0)
        
        
        first100 = 0.54
        post100 = 0.06
        
        
        mbs = 0
        
        if hours > 100:
            mbs = 100 * first100
            hours -= 100
            mbs += hours * post100
        
        else:
            mbs = hours * first100
        
        
        store.persistent._mas_dockstat_moni_size = int(mbs * (1024**2))



init 200 python in mas_dockstat:


    import store
    import store.mas_sprites as mas_sprites
    import store.mas_greetings as mas_greetings
    import store.mas_ics as mas_ics
    import store.evhand as evhand
    from cStringIO import StringIO as fastIO
    import codecs
    import re
    import os
    import random
    import datetime


    retmoni_status = None
    retmoni_data = None


    def _buildMetaDataList(_outbuffer):
        """
        Writes out a pipe-delimeted metadata list to the given buffer

        OUT:
            _outbuffer - buffer to write metadata to
        """
        
        END_DELIM = "|||"
        num_5 = "{:05d}"
        num_2 = "{:02d}"
        num_f = "{:6f}"
        first_sesh = ""
        affection_val = ""
        
        
        if store.persistent.sessions is not None:
            first_sesh_dt = store.persistent.sessions.get("first_session",None)
            
            if first_sesh_dt is not None:
                first_sesh = str(first_sesh_dt)
        
        
        
        
        
        
        if store.persistent._mas_affection is not None:
            _affection = store.persistent._mas_affection.get("affection", None)
            
            if _affection is not None:
                affection_val = num_f.format(_affection)
        
        
        _outbuffer.write("|".join([
            first_sesh,
            store.persistent.playername,
            store.persistent._mas_monika_nickname,
            affection_val,
            store.monika_chr.hair,
            store.monika_chr.clothes
        ]) + END_DELIM)


    def _buildMetaDataPer(_outbuffer):
        """
        Writes out the persistent's data into the given buffer

        Exceptions are logged

        OUT:
            _outbuffer - buffer to write persistent data to

        RETURNS:
            True on success, False if failed
        """
        
        END_DELIM = "|||per|"
        
        try:
            _outbuffer.write(codecs.encode(cPickle.dumps(store.persistent), "base64"))
            _outbuffer.write(END_DELIM)
            return True
        
        except Exception as e:
            mas_utils.writelog(
                "[ERROR]: failed to pickle data: {0}\n".format(repr(e))
            )
            return False


    def checkMonika(status, moni_data):
        """
        Parses if a given set of monika data is a rogue monika, our monika,
        and so on, and does checkins and more for the appropriate case.

        IN:
            status - findMonika's return status
            moni_data - findMonika's return data

        RETURNS:
            TBD
        """
        
        return


    def checkinMonika():
        """
        Adds entry to checkin log that monika has returned to the spaceroom.
        Also clears the global checksum var.
        """
        mas_utils.log_entry(
            store.persistent._mas_dockstat_checkin_log,
            store.persistent._mas_moni_chksum
        )
        store.persistent._mas_moni_chksum = None


    def checkoutMonika(chksum):
        """
        Adds entry to checkout log that monika has left the spaceroom.
        Also sets the chk to the global checksum var.
        Also removes monikas that had the same checksum

        IN:
            chksum - monika's checksum when checking her out.
        """
        
        if chksum is None or chksum == -1 or len(chksum) == 0:
            return
        
        mas_utils.log_entry(
            store.persistent._mas_dockstat_checkout_log,
            chksum
        )
        store.persistent._mas_moni_chksum = chksum
        
        if chksum in store.persistent._mas_dockstat_moni_log:
            store.persistent._mas_dockstat_moni_log.pop(chksum)


    def triageMonika(from_empty):
        """
        Jumps to an appropriate label based on retmoni_status and retmoni_data.
        If retmoni_status is None, we dont do anything.

        IN:
            from_empty - True if we should assume from empty desk, False
                otherwise.
        """
        if retmoni_status is None:
            return
        
        
        if (retmoni_status & MAS_PKG_FO) > 0:
            
            label_jump = "mas_dockstat_empty_desk"
        
        elif (retmoni_status & MAS_PKG_F) > 0:
            
            label_jump = "mas_dockstat_found_monika"
        
        else:
            
            label_jump = "mas_dockstat_empty_desk"
        
        if from_empty:
            label_jump += "_from_empty"
        
        renpy.jump(label_jump)


    def packageCheck(
            dockstat,
            pkg_name,
            pkg_slip,
            on_succ,
            on_fail,
            sign=True
        ):
        """
        Checks for existence of a package that matches the pkg name and slip.

        This acts as a wrapper around the signForPackage that can encapsulate
        return values with different values.

        Success is when signForPackage returns 1. All other values are
        considered failures.

        NOTE: if sign is False, then we use createPackageSlip + getPackage
        instead. use this if you don't want to delete the package once you
        have checked them in.

        IN:
            dockstat - docking station to check packag ein
            pkg_name - name of the package to check
            pkg_slip - checksum of this package
            on_succ - value to return on successful package check
            on_fail - value to return on failed package check
            sign - True to use signForPackage (aka delete after checking),
                False uses getPackage + createPackageSlip (aka no delete after
                checking)
                (Default: True)
        """
        if sign:
            if dockstat.signForPackage(pkg_name, pkg_slip, bs=b64_blocksize) == 1:
                return on_succ
        
        else:
            
            package = dockstat.getPackage(pkg_name)
            if package is None:
                return on_fail
            
            try:
                read_slip = dockstat.createPackageSlip(package, b64_blocksize)
                
                if read_slip == pkg_slip:
                    return on_succ
            
            except Exception as e:
                mas_utils.writelog(
                    "[WARN]: package slip fail? {0} | {1}\n".format(
                        pkg_name,
                        repr(e)
                    )
                )
            
            finally:
                if package is not None:
                    package.close()
        
        return on_fail

    def generateMonika(dockstat):
        """
        Generates / writes a monika blob file.

        NOTE: This does both generation and integretiy checking
        NOTE: exceptions are logged

        IN:
            dockstat - the docking station to generate Monika in

        RETURNS:
            checksum of monika
            -1 if checksums didnt match (and we cant verify data integrity of
                the generated moinika file)
            None otherwise

        ASSUMES:
            blocksize - this is a constant in this store
        """
        
        if "temp" in dockstat.station.lower():
            mas_utils.writelog("[ERROR] temp directory found, aborting.\n")
            return False
        
        
        
        moni_buffer = fastIO()
        moni_buffer = codecs.getwriter("utf8")(moni_buffer)
        
        
        NUM_DELIM = "|num|"
        
        
        if not _buildMetaDataPer(moni_buffer):
            
            
            _buildMetaDataList(moni_buffer)
        
        
        moni_chr = None
        try:
            moni_chr = open(os.path.normcase(
                renpy.config.basedir + "/game/mod_assets/monika/mbase"
            ), "rb")
            
            
            moni_buffer.write(moni_chr.read())
        
        except Exception as e:
            mas_utils.writelog("[ERROR] mbase copy failed | {0}".format(
                repr(e)
            ))
            moni_buffer.close()
            return False
        
        finally:
            
            if moni_chr is not None:
                moni_chr.close()
        
        
        moni_path = dockstat._trackPackage("monika")
        moni_fbuffer = None
        moni_tbuffer = None
        moni_sum = None
        try:
            
            
            
            moni_buffer_iter = store.MASDockingStation._blockiter(
                moni_buffer,
                blocksize
            )
            lines = 0
            last_line_size = 0
            for _line in moni_buffer_iter:
                lines += 1
                last_line_size = len(_line)
            
            
            line_str_size = len(str(lines) + NUM_DELIM)
            if (last_line_size + line_str_size) > blocksize:
                lines += 1
            
            
            
            moni_buffer_iter = store.MASDockingStation._blockiter(
                moni_buffer,
                blocksize
            )
            moni_tbuffer = fastIO()
            moni_tbuffer = codecs.getwriter("utf8")(moni_tbuffer)
            moni_tbuffer.write(str(lines) + NUM_DELIM)
            for _line in moni_buffer_iter:
                moni_tbuffer.write(_line)
            moni_buffer.close()
            
            
            moni_fbuffer = codecs.open(moni_path, "wb", "utf-8")
            
            
            checklist = dockstat.hashlib.sha256()
            def safe_encoder(data):
                return dockstat.base64.b64encode(dockstat.safeRandom(data))
            encoder = dockstat.base64.b64encode
            
            
            
            moni_tbuffer.seek(0)
            _line = moni_tbuffer.read(blocksize)
            total_buffer_size = 0
            while len(_line) == blocksize:
                total_buffer_size += blocksize
                data = encoder(_line)
                checklist.update(data)
                moni_fbuffer.write(data)
                _line = moni_tbuffer.read(blocksize)
            moni_tbuffer.close()
            
            
            last_buffer_size = len(_line)
            total_buffer_size += last_buffer_size
            
            
            
            moni_size_left = (
                store.persistent._mas_dockstat_moni_size
                - total_buffer_size
            )
            if moni_size_left > 0:
                
                
                
                if (moni_size_left + last_buffer_size) <= blocksize:
                    extra_padding = moni_size_left
                    moni_size_left = 0
                else:
                    extra_padding = blocksize - last_buffer_size
                    moni_size_left -= extra_padding
                
                
                data = encoder(_line + dockstat.safeRandom(extra_padding))
                checklist.update(data)
                moni_fbuffer.write(data)
                
                
                
                moni_size_limit = moni_size_left - blocksize
                curr_size = 0
                
                while curr_size < moni_size_limit:
                    data = safe_encoder(blocksize)
                    checklist.update(data)
                    moni_fbuffer.write(data)
                    curr_size += blocksize
                
                
                leftovers = moni_size_left - curr_size
                if leftovers > 0:
                    data = safe_encoder(leftovers)
                    checklist.update(data)
                    moni_fbuffer.write(data)
            
            else:
                
                
                data = encoder(_line)
                checklist.update(data)
                moni_fbuffer.write(data)
            
            
            moni_sum = checklist.hexdigest()
        
        except Exception as e:
            mas_utils.writelog("[ERROR] monibuffer write failed | {0}".format(
                repr(e)
            ))
            
            
            
            try:
                
                
                if moni_fbuffer is not None:
                    moni_fbuffer.close()
                
                moni_fbuffer = None
                os.remove(moni_path)
            except:
                pass
            
            return False
        
        finally:
            
            if moni_fbuffer is not None:
                moni_fbuffer.close()
            
            
            if moni_tbuffer is not None:
                moni_tbuffer.close()
            
            
            moni_buffer.close()
        
        
        moni_pkg = dockstat.getPackage("monika")
        if moni_pkg is None:
            
            mas_utils.writelog("[ERROR] monika not found.")
            mas_utils.trydel(moni_path)
            return False
        
        
        moni_slip = dockstat.createPackageSlip(moni_pkg, blocksize)
        if moni_slip is None:
            
            mas_utils.writelog("[ERROR] monika could not be validated.")
            mas_utils.trydel(moni_path)
            return False
        
        if moni_slip != moni_sum:
            
            mas_utils.writelog(
                "[ERROR] monisums didn't match, did we have write failure?"
            )
            mas_utils.trydel(moni_path)
            return -1
        
        
        return moni_sum


    def init_findMonika(dockstat):
        """
        findMonika variation that is meant to be run at init time.

        IN:
            dockstat - MASDockingStation to use
        """
        global retmoni_status, retmoni_data
        
        
        retmoni_status, retmoni_data = findMonika(dockstat)


    def findMonika(dockstat):
        """
        Attempts to find monika in the giving docking station

        IN:
            dockstat - MASDockingStation to use

        RETURNS: tuple of the following format:
            [0]: MAS_PKG_* constants depending on the state of monika
            [1]: either list of data or persistent object of data. Will be
                None if no data or errors occured
        """
        END_DELIM = "|||"
        PER_DELIM = "per|"
        ret_code = 0
        
        status, first_line = dockstat.smartUnpack(
            "monika",
            store.persistent._mas_moni_chksum,
            lines=-1,
            bs=b64_blocksize
        )
        
        if (status & (dockstat.PKG_E | dockstat.PKG_N)) > 0:
            
            
            
            return (MAS_PKG_NF, None)
        
        
        
        
        
        first_line.seek(0)
        
        
        
        
        real_data = first_line.read()
        first_line.close()
        
        
        
        per_data = parseMoniDataPer(real_data)
        
        if per_data is None:
            
            
            
            real_data, sep, garbage = real_data.partition(END_DELIM)
            
            
            if len(sep) == 0:
                
                return (MAS_PKG_NF, None)
            
            real_data = parseMoniData(real_data)
            ret_code = MAS_PKG_DL
        
        else:
            real_data = per_data
            ret_code = MAS_PKG_DP
        
        if real_data is None:
            
            
            return (MAS_PKG_NF, real_data)
        
        if (status & dockstat.PKG_C) > 0:
            
            mas_utils.writelog(
                "[!] I found a corrupt monika! {0}\n".format(status)
            )
            return (ret_code | MAS_PKG_FO, real_data)
        
        
        return (ret_code | MAS_PKG_F, real_data)


    def parseMoniData(data_line):
        """
        Parses monika data into its components

        NOTE: all exceptions are logged

        IN:
            data_line - PIPE delimeted data line

        RETURNS: list of the following format:
            [0]: datetime of first sessin
            [1]: playername
            [2]: monika's nickname (could be Monika)
            [3]: affection, integer value (dont really rely on this for much)
            [4]: monika's hair setting
            [5]: monika's clothes setting

            OR None if general (not item-specific) parse errors occurs)
        """
        try:
            data_list = data_line.split("|")
            
            
            data_list[0] = mas_utils.tryparsedt(data_list[0])
            data_list[3] = mas_utils.tryparseint(data_list[3], 0)
            data_list[4] = mas_sprites.tryparsehair(data_list[4])
            data_list[5] = mas_sprites.tryparseclothes(data_list[5])
            
            
            return data_list[:6]
        
        except Exception as e:
            mas_utils.writelog("[ERROR]: Moni Data parse fail: {0}\n".format(
                repr(e)
            ))
            return None


    def parseMoniDataPer(data_line):
        """
        Parses persitent data into a persitent object.

        NOTE: all exceptions are loggeed

        IN:
            data_line - the data portion that may contain a persitent

        RETURNS: a persistent object, or None if failure
        """
        try:
            
            
            splitted = data_line.split("|||per|")
            if(len(splitted)>0):
                return cPickle.loads(codecs.decode(splitted[0] + b'='*4, "base64"))
            return cPickle.loads(codecs.decode(data_line + b'='*4, "base64"))
        
        except Exception as e:
            mas_utils.writelog(
                "[ERROR]: persistent unpickle failed: {0}\n".format(repr(e))
            )
            return None


    def selectReturnHomeGreeting(gre_type=None):
        """
        Selects the correct Return Home greeting.

        If None was selected, we return the default returned home gre

        We also default type to TYPE_GENERIC_RET if no type is given

        IN:
            gre_type - greeting type to find
                If None, we use TYPE_GENERIC_RET
                (Default: None)

        RETURNS:
            Event object representing the selected greeting
        """
        if gre_type is None:
            gre_type = mas_greetings.TYPE_GENERIC_RET
        
        sel_gre_ev = mas_greetings.selectGreeting(gre_type)
        
        if sel_gre_ev is None:
            
            return store.mas_getEV("greeting_returned_home")
        
        
        return sel_gre_ev


    def getCheckTimes(chksum=None):
        """
        Gets the corresponding checkin/out times for the given chksum.

        IN:
            chksum - chksum to retrieve checkin/checkout times.
                If None, then we simply get the latest checkin/checkout,
                regardless if they match or not.
                (Default: None)

        RETURNS tuple of the following format:
            [0] - checkout time
            [1] - checkin time
        If any param is None, then we couldn't find the matching chksum or
        there were no entries
        """
        checkin_log = store.persistent._mas_dockstat_checkin_log
        checkout_log = store.persistent._mas_dockstat_checkout_log
        checkin_time = None
        checkout_time = None
        checkin_len = len(checkin_log)
        checkout_len = len(checkout_log)
        
        
        def find_time(check_log, check_sum):
            for _time, _chksum in check_log:
                if _chksum == check_sum:
                    return _time
            
            return None
        
        if checkin_len > 0:
            if chksum is None:
                checkin_time = checkin_log[checkin_len-1][0]
            
            else:
                checkin_time = find_time(checkin_log, chksum)
        
        if checkout_len > 0:
            if chksum is None:
                checkout_time = checkout_log[checkout_len-1][0]
            
            else:
                checkout_time = find_time(checkout_log, chksum)
        
        return (checkout_time, checkin_time)


    def diffCheckTimes(index=None):
        """
        Returns the difference between the latest checkout and check in times
        We do checkin - checkout.

        IN:
            index - the index of checkout/checkin to use when diffing
                If None, we use the latest one
                (Default: None)

        RETURNS: timedelta of the difference between checkin and checkout
        """
        checkin_log = store.persistent._mas_dockstat_checkin_log
        checkout_log = store.persistent._mas_dockstat_checkout_log
        checkin_len = len(checkin_log)
        checkout_len = len(checkout_log)
        
        if checkin_len == 0 or checkout_len == 0:
            return datetime.timedelta(0)
        
        if checkin_len != checkout_len:
            
            mas_utils.writelog(
                (
                    "[WARNING]: checkin is {0}, checkout is {1}. "
                    "Going to pop.\n"
                ).format(checkin_len, checkout_len)
            )
            
            
            if checkin_len > checkout_len:
                larger_log = checkin_log
                goal_size = checkout_len
            
            else:
                larger_log = checkout_log
                goal_size = checkin_len
            
            while len(larger_log) > goal_size:
                larger_log.pop()
        
        if index is None or index >= len(checkout_log):
            index = len(checkout_log)-1
        
        return checkin_log[index][0] - checkout_log[index][0]


    def timeOut(_date):
        """
        Given a date, return how long monika has been out

        We assume that checkout logs are the source of truth

        IN:
            _date - date to check
        """
        checkout_log = store.persistent._mas_dockstat_checkout_log
        
        if len(checkout_log) == 0:
            return datetime.timedelta(0)
        
        
        checkout_indexes = [
            index
            for index in range(0, len(checkout_log))
            if checkout_log[index][0].date() == _date
        ]
        
        if len(checkout_indexes) == 0:
            return datetime.timedelta(0)
        
        
        time_out = datetime.timedelta(0)
        
        for index in checkout_indexes:
            time_out += diffCheckTimes(index)
        
        return time_out


    def _ds_aff_for_tout(
            _time_out,
            max_hour_out,
            max_aff_gain,
            min_aff_gain,
            aff_mult=1
            ):
        """
        Grants an amount of affection based on time out. This is designed for
        use ONLY with the returned home greeting.

        NOTE: this also sets the monika_returned_home persistent

        IN:
            _time_out - timedelta we want to treat as monika being out
            max_hour_out - how many hours is considered max
                (anthing OVER this will be maxxed)
            max_aff_gain - amount of aff to be gained when max+
            min_aff_gain - smallest amount of aff gain
            aff_mult - multipler to hours to use as aff gain when between min
                and max
                (Default: 1)
        """
        if store.persistent._mas_monika_returned_home is None:
            hours_out = int(_time_out.total_seconds() / 3600)
            
            
            if hours_out > max_hour_out:
                aff_gain = max_aff_gain
            elif hours_out == 0:
                aff_gain = min_aff_gain
            else:
                aff_gain = hours_out * aff_mult
            
            store.mas_gainAffection(aff_gain, bypass=True)
            store.persistent._mas_monika_returned_home = (
                datetime.datetime.now()
            )


init 205 python in mas_dockstat:
    import store.mas_threading as mas_threading



    monikagen_promise = mas_threading.MASAsyncWrapper(
        generateMonika,
        [store.mas_docking_station]
    )


    monikafind_promise = mas_threading.MASAsyncWrapper(
        findMonika,
        [store.mas_docking_station]
    )



    abort_gen_promise = False



    def abortGenPromise():
        """
        Attempts to about the monikagen promise and properly delete the
        monika package.
        """
        global abort_gen_promise
        
        if not abort_gen_promise:
            return
        
        
        if not monikagen_promise.done():
            return
        
        
        monikagen_promise.end()
        store.mas_docking_station.destroyPackage("monika")
        abort_gen_promise = False








label mas_dockstat_ready_to_go(moni_chksum):


    $ can_moni_leave = moni_chksum and moni_chksum != -1

    if can_moni_leave:




        python:

            mas_useThermos()


            renpy.pause(1.0, hard=True)


        if (
            mas_isMoniAff(higher=True) and mas_isMonikaBirthday()
            and not mas_SELisUnlocked(mas_clothes_blackdress)
        ):
            if len(persistent._mas_dockstat_checkout_log) == 0:

                $ monika_chr.change_clothes(mas_clothes_blackdress)
                call mas_dockstat_first_time_goers from _call_mas_dockstat_first_time_goers
            call mas_bday_bd_outro from _call_mas_bday_bd_outro

        elif len(persistent._mas_dockstat_checkout_log) == 0:
            call mas_dockstat_first_time_goers from _call_mas_dockstat_first_time_goers_1
        else:

            m "Alright."


        $ store.mas_dockstat.checkoutMonika(moni_chksum)
    else:



        call mas_dockstat_decrement_date_counts from _call_mas_dockstat_decrement_date_counts



    return can_moni_leave


label mas_dockstat_first_time_goers:
    call mas_transition_from_emptydesk ("monika 3eua") from _call_mas_transition_from_emptydesk_10
    m 3eua "I'm now in the file 'monika' in your characters folder."
    m "After I shut down the game, you can move me wherever you like."
    m 3eub "But make sure to bring me back to the characters folder before turning the game on again, okay?"
    m 1eua "And lastly..."
    m 1ekc "Please be careful with me. It's so easy to delete files after all..."
    m 1eua "Anyway..."
    return

label mas_dockstat_abort_post_show:


    python:

        _curr_drink = MASConsumable._getCurrentDrink()
        if _curr_drink and _curr_drink.portable:
            _curr_drink.acs.keep_on_desk = True

    return

label mas_dockstat_abort_gen:


    python:
        store.mas_dockstat.abort_gen_promise = True


        store.mas_dockstat.abortGenPromise()




label mas_dockstat_decrement_date_counts:

    $ persistent._mas_dockstat_going_to_leave = False


    if persistent._mas_player_bday_left_on_bday:
        $ persistent._mas_player_bday_left_on_bday = False
        $ persistent._mas_player_bday_date -= 1

    if persistent._mas_f14_on_date:
        $ persistent._mas_f14_on_date = False
        $ persistent._mas_f14_date_count -= 1

    if persistent._mas_bday_on_date:
        $ persistent._mas_bday_on_date = False
        $ persistent._mas_bday_date_count -= 1
    return



label mas_dockstat_empty_desk:


    if persistent._mas_o31_in_o31_mode:
        $ mas_globals.show_vignette = True

        if mas_current_weather != mas_weather_thunder:
            $ mas_changeWeather(mas_weather_thunder, True)





    $ set_to_weather = mas_shouldRain()
    if set_to_weather is not None:
        $ mas_changeWeather(set_to_weather)
        $ skip_setting_weather = True


    $ store.mas_sprites.reset_zoom()

    call spaceroom (hide_monika=True, scene_change=True) from _call_spaceroom_21
    $ mas_from_empty = True

    $ checkout_time = store.mas_dockstat.getCheckTimes()[0]

    if mas_isD25Season() and persistent._mas_d25_deco_active:
        $ store.mas_d25ShowVisuals()

    if mas_confirmedParty() and mas_isMonikaBirthday():
        $ persistent._mas_bday_visuals = True
        $ store.mas_surpriseBdayShowVisuals(cake=not persistent._mas_bday_sbp_reacted)


    elif persistent._mas_player_bday_decor:
        $ store.mas_surpriseBdayShowVisuals()


label mas_dockstat_empty_desk_preloop:


    $ import store.mas_dockstat as mas_dockstat
    $ mas_OVLHide()
    $ mas_calRaiseOverlayShield()
    $ mas_calShowOverlay()
    $ disable_esc()
    $ mas_enable_quit()
    $ promise = mas_dockstat.monikafind_promise

label mas_dockstat_empty_desk_from_empty:


    if promise.ready:
        $ promise.start()


    $ renpy.pause(1.0, hard=True)


    if mas_confirmedParty() and mas_isMonikaBirthday():
        $ persistent._mas_bday_visuals = True
        $ store.mas_surpriseBdayShowVisuals(cake=not persistent._mas_bday_sbp_reacted)


    if promise.done():

        $ _status, _data_line = promise.get()
        $ mas_dockstat.retmoni_status = _status
        $ mas_dockstat.retmoni_data = _data_line
        $ mas_dockstat.triageMonika(True)



    jump mas_dockstat_empty_desk_from_empty

define mas_dockstat.different_moni_flow = False


label mas_dockstat_different_monika:




    $ mas_dockstat.previous_vars["m_name"] = persistent._mas_monika_nickname
    $ mas_dockstat.previous_vars["playername"] = persistent.playername
    $ mas_dockstat.previous_vars["hair"] = persistent._mas_monika_hair
    $ mas_dockstat.previous_vars["clothes"] = persistent._mas_monika_clothes



    $ mas_dockstat.different_moni_flow = True






    $ moni_data = mas_dockstat.parseMoniData(mas_dockstat.retmoni_data)

    if moni_data is None:


        $ store.mas_utils.trydel(mas_docking_station._trackPackage("monika"))
        $ mas_dockstat.different_moni_flow = False
        jump mas_dockstat_empty_desk





    $ moni_sesh, player, m_name, aff_val, moni_hair, moni_clothes = moni_data
    $ monika_chr.change_outfit(moni_clothes, moni_hair, False)


    call mas_transition_from_emptydesk ("monika 1ekd") from _call_mas_transition_from_emptydesk_11

    m "[player]?"

    m "Wait, you're not [player]."



    $ mas_dockstat.retmoni_data = None
    $ startup_check = False

    jump ch30_post_exp_check



label mas_dockstat_found_monika_from_empty:
    if checkout_time is not None and checkout_time.date() == persistent._date_last_given_roses:
        $ monika_chr.wear_acs(mas_acs_roses)


    $ promise = None




label mas_dockstat_found_monika:
    $ store.mas_dockstat.retmoni_status = None
    $ store.mas_dockstat.retmoni_data = None
    $ store.mas_dockstat.checkinMonika()
    $ persistent._mas_pm_taken_monika_out = True
    $ checkout_time = store.mas_dockstat.getCheckTimes()[0]

    if checkout_time is not None and checkout_time.date() == persistent._date_last_given_roses:
        $ monika_chr.wear_acs(mas_acs_roses)

    python:
        selected_greeting = store.mas_dockstat.selectReturnHomeGreeting(
            persistent._mas_greeting_type
        ).eventlabel




        persistent._mas_greeting_type = None


        mas_docking_station.destroyPackage("monika")


        mas_OVLShow()
        mas_disable_quit()
        enable_esc()
        startup_check = False

    if persistent._mas_o31_in_o31_mode:
        $ store.mas_globals.show_vignette = True

        $ mas_changeWeather(mas_weather_thunder, True)

    elif mas_run_d25s_exit and not mas_lastSeenInYear("mas_d25_monika_d25_mode_exit"):
        call mas_d25_season_exit from _call_mas_d25_season_exit_2

    jump ch30_post_exp_check
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
