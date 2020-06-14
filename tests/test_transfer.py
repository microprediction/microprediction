
from microprediction.writer import MicroWriter



def test_put():
    write_key = '124d48f4f2484ef90aa59f0a89eba45b'  # "Fecal Boa"
    mw = MicroWriter(write_key=write_key)
    res = mw.put_balance(source_write_key="bb77318c1462e28220c1544eb0440d86") # tamas fox
    pass

