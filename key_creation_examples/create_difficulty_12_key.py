from microconventions import new_key, animal_from_key

# Create a key that can create streams

DIFFICULTY=12

if __name__=='__main__':
    write_key = new_key(difficulty=DIFFICULTY)
    print({'write_key':write_key,'nom de plume':animal_from_key(write_key)})

