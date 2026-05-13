from pycaw.pycaw import AudioUtilities
from pycaw.pycaw import IAudioMeterInformation
from types import NoneType

class Sound(object):
    dumps = None
    sound = 0

    def __init__(self):
        self.dumps = []
        self.sound = 0

    def current_sounds(self) -> float:
        sessions = AudioUtilities.GetAllSessions()
        x = []
        for session in sessions:
            if not session.Process:
                continue
            peak = session._ctl.QueryInterface(IAudioMeterInformation).GetPeakValue()
            volume = round(peak * 1000, 3)
            x.append(volume)

        return max(x) if len(x) > 0 else 0
    
    def add_in_dumps(self, data) -> None: 
        self.dumps.append(data)

    def get_dumps(self) -> int: 
        if len(self.dumps) != 0: 
            return sum(self.dumps) / len(self.dumps)
        else:
            return 0
        
    def get_len_dumps(self) -> int: return len(self.dumps)

    def set_zero(self) -> None: 
        self.dumps = []; 
        return None