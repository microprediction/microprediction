from microprediction import MicroWriter, MicroReader, new_key
from contexttimer import Timer
import muid

def test_client():
    with Timer() as t:
        write_key = new_key(difficulty=7)
        mw = MicroWriter(write_key=write_key)
    assert(t.elapsed < 15 )


def test_new():
    write_key = new_key(difficulty=7)
    assert MicroWriter.is_valid_key(write_key)

def test_is_valid():
    key = "4c3db49d3a291acad7bdedecfa787891"
    assert MicroWriter.is_valid_key(key)
    key = b"4c3db49d3a291acad7bdedecfa787891"
    assert MicroWriter.is_valid_key(key)==False, "Binary keys are not valid"
    key = "3c3db49d3a291acad7bdedecfa787891"
    assert not MicroWriter.is_valid_key(key)

