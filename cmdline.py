"""Provide access through command line to IGV controlling."""
import socket

import vcf


class SocketManager():

    """A Context Manager to deal with Sockets."""

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.socket.settimeout(1)

        return self.socket

    def __exit__(self, *exc_info):
        self.socket.close()


class IGV():

    """IGV wrapper to control the program through a socket."""

    def __init__(self, host="", port=60151):
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
        with SocketManager(self.host, self.port) as s:
            s.sendall(bytes(command, "ascii"))
            response = str(s.recv(1024), "ascii")

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

    def load(self):
        """Return a generator from a filetab if it's a VCF or a TAB file."""
        vcf_generator = self.loadvcf()

        if not vcf_generator:
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

    def vcf_generator(self, generator):
        """Yield only the fields we are interested in from the VCF."""
        for variant in generator:
            yield (variant.CHROM, str(variant.POS))


def tab_generator(filepath):
    """Yield line by line from a tab file except the header line."""
    first_line = False
    with open(filepath) as tabfile:
        for line in tabfile:
            s_line = tuple(line.split("\t")[:2])
            if first_line:
                yield s_line
            else:
                first_line = line.lower().split("\t")
                if not any(
                    [_ in first_line for _ in ["start", "end", "alt", "ref"]]):
                    # This file doesn't have a header
                    yield s_line


def load(filepath):
    """Return a generator from a filetab if it's a VCF or a TAB file."""
    vcf_generator = loadvcf(filepath)

    if vcf_generator:
        for variant in vcf_generator:
            yield (variant.CHROM, str(variant.POS))
    else:
        for variant in loadtab(filepath):
            yield variant


def loadtab(filepath):
    """Return a generator if the filepath is a valid VCF 4.0 file."""
    with open(filepath) as tabfile:
        first_line = tabfile.readline().split("\t")
        if len(first_line) < 5:
            # This doesn't seem to be a valid tab file.
            return False

    return tab_generator(filepath)


def loadvcf(filepath):
    """Return a generator if the filepath is a valid VCF 4.0 file."""
    vcf_reader = vcf.Reader(open(filepath), prepend_chr=True)

    if vcf_reader.infos:
        # It seems to be a valid VCF file
        return vcf_reader

    return False
