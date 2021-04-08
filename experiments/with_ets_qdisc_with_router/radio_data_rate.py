# class RadioDataRate(object):
#     r1_to_h2 = '9.6'
#     r1_to_h3 = '240'
#     r1_to_h4 = '512'
#
#     @classmethod
#     def set_r1_to_h2_data_rate(cls, data_rate):
#         cls.r1_to_h2 = data_rate
#
#     @classmethod
#     def set_r1_to_h3_data_rate(cls, data_rate):
#         cls.r1_to_h3 = data_rate
#
#     @classmethod
#     def set_r1_to_h4_data_rate(cls, data_rate):
#         cls.r1_to_h4 = data_rate
#
#     @classmethod
#     def get_r1_to_h2_data_rate(cls):
#         return cls.r1_to_h2
#
#     @classmethod
#     def get_r1_to_h3_data_rate(cls):
#         return cls.r1_to_h3
#
#     @classmethod
#     def get_r1_to_h4_data_rate(cls):
#         return cls.r1_to_h4

r1_to_h2 = '9.6'
r1_to_h3 = '240'
r1_to_h4 = '512'

def set_r1_to_h2_data_rate(data_rate):
    global r1_to_h2
    r1_to_h2 = data_rate

def set_r1_to_h3_data_rate(data_rate):
    global r1_to_h3
    r1_to_h3 = data_rate

def set_r1_to_h4_data_rate(data_rate):
    global r1_to_h4
    r1_to_h4 = data_rate

def get_r1_to_h2_data_rate():
    global r1_to_h2
    return r1_to_h2

def get_r1_to_h3_data_rate():
    global r1_to_h3
    return r1_to_h3

def get_r1_to_h4_data_rate():
    global r1_to_h4
    return r1_to_h4

if __name__ == '__main__':
    try:
        while True:
            time.sleep(2)
            print("\n\n\nCurrent VHF data rate is: ", get_r1_to_h2_data_rate())
            print("\n\n\nCurrent UHF data rate is: ", get_r1_to_h3_data_rate())
            print("\n\n\nCurrent SatComm data rate is: ", get_r1_to_h4_data_rate())

    except KeyboardInterrupt:
        sys.exit(1)