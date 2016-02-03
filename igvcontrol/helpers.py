"""Provide access through command line to IGV controlling."""
import telnetlib

import vcf


class TelnetManager():

    """A Context Manager to deal with Sockets through Telnet."""

    def __init__(self, host="localhost", port=23):
        self.host = host
        self.port = port
        self.telnet = None

    def __enter__(self):
        self.telnet = telnetlib.Telnet(self.host, self.port, 1)

        return self.telnet

    def __exit__(self, *exc_info):
        self.telnet.close()


class IGV():

    """IGV wrapper to control the program through a socket."""

    def __init__(self, host="localhost", port=60151):
        self.host = host
        self.port = port

    def check_igv(self):
        """Return True if a copy of IGV is reachable."""

        response = self.command("echo")

        if response.startswith("echo"):
            return True
        return False

    def command(self, command):
        """Return the response from IGV for command."""
        response = ""
        with TelnetManager(self.host, self.port) as t:
            try:
                t.write(bytes(command, "ascii"))
                response = str(t.read_all(), "ascii")
            except TypeError:
                t.write(command)
                response = t.read_all()

        return response

    def goto(self, position):
        """Return "True" if IGV answered "OK" to a goto command."""

        response = self.command("goto {}".format(position))

        if response.startswith("OK"):
            return True
        return False

    def load(self, filepath):
        """Return "True" if IGV answered "OK" to a load command."""

        response = self.command("load {}".format(filepath))

        if response.startswith("OK"):
            return True
        return False


class Variants():

    """A proxy to the variants contained in a VCF or TAB file.

    Initialize with a file name::

        >>> variants = Variants("path/to/file.vcf")
        >>>

    Get the variants through a generator at __next__::

        >>> for variant in variants:
        ...     print(variant)
        ("chr1", "123456")
        ("chr1", "456789")

    """

    def __init__(self, filename):
        self.filename = filename
        self.variants = None
        self.load()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.variants)

    def next(self):
        return self.__next__()

    def load(self):
        """Set a generator from a filetab if it's a VCF or a TAB file."""
        if self.filename.endswith((".xls", ".xlsx")):
            self.loadxls()
        elif not self.loadvcf():
            self.loadtab()

    def loadtab(self):
        """Return a generator if the filepath is a valid VCF 4.0 file."""
        with open(self.filename) as tabfile:
            first_line = tabfile.readline().split("\t")
            if len(first_line) < 5:
                # This doesn't seem to be a valid tab file.
                return False

        self.variants = self.tab_generator()
        return True

    def loadvcf(self):
        """Return a generator if the filepath is a valid VCF 4.0 file."""
        vcf_reader = vcf.Reader(open(self.filename), prepend_chr=True)

        if vcf_reader.infos:
            # It seems to be a valid VCF file
            self.variants = self.vcf_generator(vcf_reader)
            return True

        return False

    def loadxls(self):
        """Return True if it can set a generator with the filename."""
        from xlrd import open_workbook

        book = open_workbook(self.filename)

        self.variants = self.xls_generator(book.sheet_by_index(0))

        return True

    def tab_generator(self):
        """Yield line by line from a tab file except the header line."""
        first_line = False
        with open(self.filename) as tabfile:
            for line in tabfile:
                s_line = tuple(line.split("\t")[:2])
                if first_line:
                    yield s_line
                else:
                    first_line = line.lower().split("\t")
                    if not any([_ in first_line for _ in
                                ["start", "end", "alt", "ref"]]):
                        # This file doesn't have a header
                        yield s_line

    @staticmethod
    def vcf_generator(generator):
        """Yield only the fields we are interested in from the VCF."""
        for variant in generator:
            yield (variant.CHROM, str(variant.POS))

    @staticmethod
    def xls_generator(sheet):
        """Yield only the fields we are interested in from the XLS."""
        first_line = False
        for row in sheet.get_rows():
            chrom = row[0].value
            try:
                position = int(row[1].value)
            except ValueError:
                # This must be the header with "Start"
                position = row[1].value
            s_line = tuple([chrom, str(position)])
            if first_line:
                yield s_line
            else:
                first_line = [_.value.lower() for _ in row]
                if not any([_ in first_line for _ in
                            ["start", "end", "alt", "ref"]]):
                    # This file doesn't have a header
                    yield s_line
