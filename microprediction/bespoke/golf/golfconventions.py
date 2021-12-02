
def player_classifier(ability):
     return {'great': abs(ability -1.67) < 0.33,
               'good': abs(ability -1.0) < 0.33,
               'okay': abs(ability -0.0) < 0.25,
               'bad': abs(ability+1.0) < 0.33}

# Strokes gained statistics
GOLF_SG_CATEGORIES = ['total','ott','app','arg','putt']
