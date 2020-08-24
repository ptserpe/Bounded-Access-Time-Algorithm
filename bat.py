# Implementation of Bound Access Time algorithm
# Inputs:
    # C broadcast channels
    # AP(m) access pattern with m query sets
    # a = threshold <= length of Pi, used for large query sets
    # beta = last beta parts that are candidates to accomodate the excess query set of P1 in heuristic 3 (disjoint sets)
# Outputs:
    # a near optimal partition and a near optimal access time

def bat(qs, a, b, c):
    query_sets = qs

    initial_qs = []

    for q in query_sets:
        initial_qs.append(q)

    print "***********************"
    print "Query sets", query_sets
    print "***********************\n\n"
    print "########## INITIAL PHASE ##########\n\n"
    a = int(a)
    beta = int(b)

    num_of_channels = int(c)


    tmp = []
    for i in range(len(query_sets)):
        for j in range(len(query_sets[i])):
            tmp.append(query_sets[i][j])
        union_list = list(set().union(tmp))
    num_of_data = len(union_list)
    if num_of_data % num_of_channels != 0:
        boundary = num_of_data/num_of_channels + 1
    else:
        boundary = num_of_data/num_of_channels

    channels = []
    # initialization of channels to empty sets
    for i in range(num_of_channels):
        channels.append([])

    # Initial Phase
    ###########################################################################################################################
    ######### Heuristic about large query sets
    ###########################################################################################################################
    large = []

    # Check for every query set if there is a large one and assign it to a new list called large
    for i in range(len(initial_qs)):
        if len(initial_qs[i]) >= a:
            large.append(initial_qs[i])
            query_sets.remove(initial_qs[i])

    # Sort the large list in descending order
    large.sort(key=len, reverse=True)

    # ZIG - ZAG Assignment of query sets to the channels
    # first assignment to the channels from channels[0] to channels[num_of_channels-1]
    j = 0
    stop = False
    for i in range(num_of_channels):
        if j < len(large):
            channels[i].append(large[j])
            j += 1
        else:
            stop = True
            break;

    start = False
    end = True

    while stop == False:
        # if loop reaches end of large list
        if j == len(large) - 1:
            break;

        # Down phase
        if end == True:
            i = num_of_channels - 2
            channels[i].append(large[j])
            i -= 1

            # if start is reached
            if (i == -1):
                end = False
                start = True

        elif start == True:
            i = 1
            channels[i].append(large[j])
            i += 1

            # if end is reached
            if i == num_of_channels:
                start = False
                end = True

        j += 1

    print "***********************"
    print "Large query sets: ", large
    print "Channels after inserting large sets: "
    for c in channels:
        print c
    print "***********************\n\n"

    ###########################################################################################################################
    ############### Heuristic about overlapped query sets
    ###########################################################################################################################
    overlapped = []
    in_list = []

    # Check which channels are overlapped and save them in a list called overlapped
    for i in range(len(query_sets)):
        in_list.append(False)

    for i in range(len(query_sets)):
        for j in range(len(query_sets[i])):
            for k in range(i+1, len(query_sets)):
                # if two sets overlap
                if query_sets[i][j] in query_sets[k]:

                    # if query sets are already in the overlapped set
                    if in_list[i] == False:

                        in_list[i] = True
                        in_list[k] = True
                        tmp = []
                        tmp.append(query_sets[i])
                        tmp.append(query_sets[k])
                        overlapped.append(tmp)
                    elif in_list[i] == True:
                        if in_list[k] == False:
                            in_list[k] = True
                            tmp = []
                            tmp.append(query_sets[k])
                            overlapped.append(tmp)

    # Sort the overlapped by descending order according to the sum of the data items in every set of query sets

    for i in range(len(overlapped)):
        tmp = []
        for j in range(len(overlapped[i])):
            for k in range(len(overlapped[i][j])):
                tmp.append(overlapped[i][j][k])

    # Assign the overlapped sets by descending order in the channels starting from the beginning

    # Compute length of every channel
    channel_len = []
    for i in range(num_of_channels):
        tmp = []
        for j in range(len(channels[i])):
            for k in range(len(channels[i][j])):
                tmp.append(channels[i][j][k])
        union_list = list(set().union(tmp))
        channel_len.append(len(union_list))

    j = 0
    tmp_len = []
    for i in range(len(overlapped)):
        tmp = []
        # Compute the candidate overlapped list to be inserted in the channel
        for k in range(len(overlapped[i])):
            for m in range(len(overlapped[i][k])):
                tmp.append(overlapped[i][k][m])
        # Compute the length of the channel if the current overlapped[i] is inserted in the channel j

        tmp_len = []
        for t in tmp:
            tmp_len.append(t)
        for k in range(len(channels[j])):
            for m in range(len(channels[j][k])):
                tmp_len.append(channels[j][k][m])

        union_list = list(set().union(tmp_len))
        current_len = len(union_list)

        for k in range(len(overlapped[i])):
            channels[j].append(overlapped[i][k])
        channel_len[j] = current_len
        j += 1

        if j == num_of_channels:

            channel_len = []
            sorted_channels = []

            for c in range(num_of_channels):
                tmp = []
                for m in range(len(channels[c])):
                    for k in range(len(channels[c][m])):
                        tmp.append(channels[c][m][k])
                union_list = list(set().union(tmp))
                channel_len.append(len(union_list))
                sorted_channels.append({channel_len[c]:channels[c]})

            sorted_channels = sorted(sorted_channels, reverse = True)

            channels = []
            for c in sorted_channels:
                for key in c.keys():
                    channels.append(c[key])
            break





    print "***********************"
    print "overlapped query sets: ", overlapped
    print "Channels after inserting overlapped sets: "
    for c in channels:
        print c
    print "***********************\n\n"
    ###########################################################################################################################
    ############### Heuristic 3 about disjoint query sets
    ###########################################################################################################################

    disjoint_sets = []
    # Remove the overlapped query sets from initial query set
    for i in range(len(query_sets)):
        disjoint_sets.append(query_sets[i])

    for i in range(len(query_sets)):
        if in_list[i] == True:
            disjoint_sets.remove(query_sets[i])

    # sort list of disjoint query sets according to descending order of length
    disjoint_sets = sorted(disjoint_sets, key = len, reverse = True)

    j = 0

    #assign disjoint_sets to channels
    for d in disjoint_sets:
        flag = True
        #check if there exist channels with length < boundary
        while flag == True:
            if channel_len[j] < boundary:
                channels[j].append(d)

                j += 1
                channel_len = []
                sorted_channels = []

                #sort channels
                for c in range(num_of_channels):
                    tmp = []
                    for m in range(len(channels[c])):
                        for k in range(len(channels[c][m])):
                            tmp.append(channels[c][m][k])

                    union_list = list(set().union(tmp))

                    channel_len.append(len(union_list))
                    sorted_channels.append({channel_len[c]:channels[c]})

                sorted_channels = sorted(sorted_channels, reverse = True)
                channels = []
                for chan in sorted_channels:
                    for key in chan.keys():
                        channels.append(chan[key])

                if j == num_of_channels:
                    j = 0

                break;
            elif j == num_of_channels - 1:
                j = 0
                flag = False
                break;
            j += 1
    
        c = 0
        #if smaller channels do not exist
        if flag == False:
            channels[c].append(d)
            #sort channels
            channel_len = []
            sorted_channels = []

            for ch in range(num_of_channels):
                tmp = []
                for m in range(len(channels[ch])):
                    for k in range(len(channels[ch][m])):
                        tmp.append(channels[ch][m][k])

                union_list = list(set().union(tmp))
                channel_len.append(len(union_list))
                sorted_channels.append({channel_len[ch]:channels[ch]})

            sorted_channels = sorted(sorted_channels, reverse = True)
            channels = []
            for sk in sorted_channels:
                for key in sk.keys():
                    channels.append(sk[key])

            c += 1
            if c == num_of_channels:
                c = 0




    print "***********************"
    print "Disjoint query sets: ", disjoint_sets
    print "Channels after inserting disjoint sets: "
    for c in channels:
        print c

    ################################# TUNING PHASE ###############################################
    # use  a list of the last beta candidate channels
    print "########## TUNING PHASE ##########\n\n"

    done = False
    while done == False:
        candidates = []
        for i in range(num_of_channels - beta, num_of_channels):
            candidates.append(channels[i])

        print "***********************"
        print "Candidates channels: ",  candidates

        # For this phase we need to compute the delta1 and delta2 values
        # we will compute delta1 for every query set in the first channel and every possible last beta channels starting from the last one
        # we will relocate the excess query set from P1 to the one that fits without breaking the main condition

        #First compute delta 1 for each query set:


        initial_length = []
        new_p1 = []

        for i in range(len(channels[0])):
            for j in range(len(channels[0][i])):
                initial_length.append(channels[0][i][j])

        first_length = len(list(set().union(initial_length)))
        delta1 = []
        for excess_query_set in channels[0]:
            removed_length = []
            copy_channels = []

            for c in channels[0]:
                copy_channels.append(c)

            #remove current excess_query_set from channel 1
            copy_channels.remove(excess_query_set)

            for i in range(len(copy_channels)):
                for j in range(len(copy_channels[i])):
                    removed_length.append(copy_channels[i][j])

            new_p1_len = len(list(set().union(removed_length)))

            diff = first_length - new_p1_len
            new_p1.append({diff : new_p1_len})
            delta1.append({diff : excess_query_set})

        delta1 = sorted(delta1, reverse = True)
        new_p1 = sorted(new_p1, reverse = True)

        delta2 = []
        new_px = []
        for excess_query_set in delta1:
            tmp = []
            new_px_tmp = []
            for key in excess_query_set.keys():

                #add excess query set to candidate channel to compute new length
                for i in range(len(candidates)):

                    copy_channels = []
                    added_length = 0
                    temp_cc = []
                    for j in range(len(candidates[i])):
                        copy_channels.append(candidates[i][j])
                    copy_channels.append(excess_query_set[key])

                    # compute length if excess_query_set[key] is added in channel c
                    for j in range(len(copy_channels)):

                        for cc in range(len(copy_channels[j])):
                            temp_cc.append(copy_channels[j][cc])

                    added_length += len(list(set().union(temp_cc)))

                    new_len = abs(added_length - channel_len[i + len(channels) - beta])

                    tmp.append({new_len:candidates[i]})
                    new_px_tmp.append({new_len:added_length})
                new_px.append(new_px_tmp)

                delta2.append(tmp)


        max_key = 0
        max_qs = []
        for qs in delta1:
            for key in qs.keys():
                if key >= max_key:
                    max_key = key
                    max_qs.append(qs)

        min_keys = []

        for k in range(len(max_qs)):
            min_key = 100000
            for i in range(len(delta2[k])):
                tmp = []

                for key in delta2[k][i].keys():
                    if key < min_key:
                        min_key = key
                        tmp.append(min_key)

                min_keys.append(tmp)


            #find position of new_px with the min key
            for i in range(len(new_px[k])):
                if min_key in new_px[k][i]:
                    position = i
                    break;

            if new_p1[0][max_key] >= boundary and channel_len[0] > new_px[k][position][min_key]:
                # move excess query set p to channel px
                #1st remove p from p1
                channels[0].remove(delta1[0][max_key])

                for d in delta2[0]:
                    for key in d.keys():
                        if key == min_key:
                            px = d[min_key]
                            break;

                for i in range(num_of_channels):
                    if px == channels[i]:
                        pos = i

                # move to px
                channels[pos].append(delta1[0][max_key])


                channel_len = []
                sorted_channels = []

                for i in range(num_of_channels):
                    tmp = []
                    for j in range(len(channels[i])):
                        for k in range(len(channels[i][j])):
                            tmp.append(channels[i][j][k])
                    union_list = list(set().union(tmp))
                    channel_len.append(len(union_list))
                    sorted_channels.append({channel_len[i]:channels[i]})

                sorted_channels = sorted(sorted_channels, reverse = True)

                channels = []
                for c in sorted_channels:
                    for key in c.keys():
                        channels.append(c[key])

                print "***********************"
                print "Inserting excess query set ", delta1[0][max_key], "to channel ", pos
                print "Channels after inserting disjoint: "
                for c in channels:
                    print c
                print "***********************"

                channel_len = []
                for i in range(num_of_channels):
                    tmp = []
                    for j in range(len(channels[i])):
                        for k in range(len(channels[i][j])):
                            tmp.append(channels[i][j][k])
                    union_list = list(set().union(tmp))
                    channel_len.append(len(union_list))
                break
            else:
                print "\n\n\n\n***********************"
                print "Final Partitions(Pi): "
                for c in channels:
                    print c
                print "***********************"
                print "Worst access time: ", channel_len[0]
                done = True
                break;


def inputs():

    query_sets = []

    with open("input.txt", "r") as file:
        for line in file:
            line = line.rstrip('\n')
            tmp = eval(line)
            query_sets.append(tmp)

    a = raw_input("Enter threshold a, for large query sets: ")
    c = raw_input("Enter number of channels: ")

    beta = raw_input("Enter number of candidate channels for relocation: ")
    if beta >= c:
        print "Number of candidate channels should not be larger than number of channels.. Exiting.."
    else:
        # call bat algorithm
        bat(query_sets, a, beta, c)

inputs()
