def to_bin(h):
    return format(h, '016b')

def walk_map(m):
    address_width = 16 # 16-bit address bus size by default (Z80)

    max_address = max([offset for (offset, _) in m])
    if max_address >= 2 ** 16:
        address_width = 32 # 32-bit address bus size (68000)
        # TODO: I guess maybe we might one day have a 64-bit machine. That's not today, though

    for (start_offset, identifier) in sorted(m, key=lambda p: p[0]):
        print(to_bin(start_offset) + ' ' + identifier)

        # identify set bits
        set_bits = []

        address = 0
        while address < address_width:
            if(start_offset) & 1 != 0:
                set_bits.append(address)
            address += 1 # increment address line
            start_offset = start_offset >> 1 # shift out the lowest bit

        formatted_addresses = map(lambda a: f'A{a}', set_bits)
        print(' bits set:', ', '.join(formatted_addresses))



memory_map = [ # Sord M5, no expansion
    (0x0000, 'BIOS ROM'),
    (0x2000, 'Cart ROM, page A (16k max)'),
    (0x6000, 'Reserved area'),
    (0x7000, 'Internal RAM (4k)'),
    (0x8000, 'External RAM on cartridge')
]

io_map = [
    (0x00, 'Z80 CTC'),
]
    
print('Memory Map:')
walk_map(memory_map)

print('I/O Map:')
walk_map(io_map)
