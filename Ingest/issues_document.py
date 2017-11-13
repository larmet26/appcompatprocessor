import settings
import logging
from ingest import Ingest
from appAux import loadFile

try:
    import xml.etree.cElementTree as etree
except ImportError:
    print "No cElementTree available falling back to python implementation!"
    settings.__CELEMENTREE__ = False
    import xml.etree.ElementTree as etree
else: settings.__CELEMENTREE__ = True

logger = logging.getLogger(__name__)
# Module to ingest issues documents generated by HX


class Issues_document(Ingest):
    ingest_type = "issues_document"
    file_name_filter = "(?:.*)(?:\/|\\)(.*)_[a-zA-Z0-9]{22}\.xml$"

    def __init__(self):
        super(Issues_document, self).__init__()

    def checkMagic(self, file_name_fullpath):
        # Check magic
        magic_id = self.id_filename(file_name_fullpath)
        if 'XML' in magic_id:
            file_object = loadFile(file_name_fullpath)
            try:
                # todo: Issue documents are declared as UTF-8 but not encoded as such, etree may fail to parse them
                # root = etree.parse(file_object).getroot()
                # if root.tag == 'IssueList': return True
                if 'IssueList' in magic_id or 'batchresult' in magic_id: return True
            except Exception as e:
                logger.exception("[%s] Failed to parse XML for: %s" % (self.ingest_type, file_name_fullpath))
            finally:
                file_object.close()

        return False

    def calculateID(self, file_name_fullpath):
        # We don't have to process these files
        return 1

    def processFile(self, file_fullpath, hostID, instanceID, rowsData):
        # We don't have to process these files
        return True