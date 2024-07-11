def allocate_rooms(group_info, hostel_info):
    allocation_results = []



    
    for group in group_info:
        group_id = group['Group ID']
        members = int(group['Members'])
        gender = group['Gender']

        suitable_hostels = [h for h in hostel_info if h['Gender'] == gender]
        suitable_hostels.sort(key=lambda x: int(x['Cap']))

        allocated = False

        for hostel in suitable_hostels:
            room_capacity = int(hostel['Cap'])
            if room_capacity >= members:
                allocation_results.append({
                    'Group ID': group_id,
                    'HostelName': hostel['HostelName'],
                    'Room Number': hostel['Room Number'],
                    'Members Allocated': members
                })
                allocated = True
                break

        if not allocated:
            allocation_results.append({
                'Group ID': group_id,
                'HostelName': 'Unallocated',
                'Room Number': 'N/A',
                'Members Allocated': members
            })

    return allocation_results
