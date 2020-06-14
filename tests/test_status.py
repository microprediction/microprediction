from microprediction.reader import MicroReaderStatus

def test_reader_status():
    status = MicroReaderStatus().reader_status()
    for row in status:
        assert row[1]=='up', row[0]+" is down "
