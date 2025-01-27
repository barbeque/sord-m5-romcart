def to_bin(h):
    return format(h, '016b')

def walk_map(m, is_io = False):
    address_width = 16 if not is_io else 8 # 16-bit address bus size by default (Z80)

    max_address = max([offset for (offset, _) in m])
    if max_address >= 2 ** 16:
        address_width = 32 # 32-bit address bus size (68000)
        # TODO: I guess maybe we might one day have a 64-bit machine. That's not today, though

    sorted_mappings = sorted(m, key=lambda p: p[0])

    i = 0

    for (start_offset, identifier) in sorted_mappings:
        print(to_bin(start_offset) + ' ' + identifier)

        # identify set bits
        set_bits = []

        saved_start_offset = start_offset

        address = 0
        while address < address_width:
            if(start_offset) & 1 != 0:
                set_bits.append(address)
            address += 1 # increment address line
            start_offset = start_offset >> 1 # shift out the lowest bit

        formatted_addresses = map(lambda a: f'A{a}', set_bits)
        print(' bits set:', ', '.join(formatted_addresses))

        # try to figure out the length of this segment
        max_machine_address = 2 ** address_width
        if i + 1 >= len(sorted_mappings): # last one has to take up the rest of memory
            size_to_next = max_machine_address - saved_start_offset
        else: # someone is above this one, calculate the distance
            (next_offset, _) = sorted_mappings[i + 1]
            size_to_next = next_offset - saved_start_offset
        print(' length:', size_to_next)

        i += 1


memory_map = [ # Sord M5, no expansion
    (0x0000, 'BIOS ROM'),
    (0x2000, 'Cart ROM, page A'),
    (0x4000, 'Cart ROM, page B'),
    (0x6000, 'Cart ROM, page C (reserved area?)'),
    (0x7000, 'Internal RAM (4k)'),
    (0x8000, 'External RAM on cartridge')
]

io_map = [
    (0x00, 'Z80 CTC, SIO int.'),
    (0x01, 'Z80 CTC, peripheral timer'),
    (0x02, 'Z80 CTC, SIO clock generator'),
    (0x03, 'Z80 CTC, VDP blank interrupt'),
    (0x11, 'TMS9928, VDP status/control/address'),
    (0x10, 'TMS9928, VDP data'),
    (0x20, 'SN76489 PSG control'),
    (0x30, 'Keyboard, row 0'),
    (0x31, 'Keyboard, row 1'),
    (0x32, 'Keyboard, row 2'),
    (0x33, 'Keyboard, row 3'),
    (0x34, 'Keyboard, row 4'),
    (0x35, 'Keyboard, row 5'),
    (0x36, 'Keyboard, row 6'),
    (0x37, 'Joystick'),
    # $50 bit 7 is also reset/halt key data port
    (0x50, 'Tape data, parallel control')
]
    
print('Memory Map:')
walk_map(memory_map)

print('I/O Map:')
walk_map(io_map, True)
