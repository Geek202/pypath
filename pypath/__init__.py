import math


class PathfindingMapOld:
    def __init__(self, mp, mapsize, solid_ids = None):
        if solid_ids is None:
            solid_ids = [1]
        self.map = mp
        self.solids = solid_ids
        self.pathmap = []
        self.mapsize = mapsize

    def findPath(self, startpos, endpos, pos_callback = None, solid_pos_callback = None, iter_callback = None, path_update_callback = None, path_complete_callback = None):

        if startpos[1] >= self.mapsize[1] or startpos[1] < 0:
            raise RuntimeError("X position cannot be outside the map {0}, it must be at most: {1}".format(startpos, len(self.map)))
        elif startpos[0] >= self.mapsize[0] or startpos[0] < 0:
            raise RuntimeError("Y position cannot be outside the map {0}, it must be at most: {1}".format(startpos, len(self.map)))

        scanned_positions = {startpos : 0}
        solid_positions = []
        reached_dest = False
        tmp = scanned_positions.copy()
        for x in range(self.mapsize[1]):
            for y in range(self.mapsize[0]):
                try:
                    if (x, y) in tmp:
                        pass
                    elif (x, y) in solid_positions:
                        pass
                    elif self.map[x][y] in self.solids:
                        solid_positions.append((x, y))
                        if solid_pos_callback is not None:
                            solid_pos_callback(x, y)
                    else:
                        xdif = abs(startpos[1] - x)
                        ydif = abs(startpos[0] - y)
                        tmp[(x, y)] = math.sqrt((xdif ** 2) + (ydif ** 2))
                        if (x, y) == endpos:
                            reached_dest = True
                        if pos_callback is not None:
                            pos_callback(x, y)
                except IndexError: print("!!! E !!!")
        if iter_callback is not None:
            iter_callback()
        scanned_positions = tmp

        print("Map exploring complete!")

        found_route = False
        current_pos = endpos
        route = [endpos[::-1]]
        c = 0
        while not found_route:
            options = {}
            for x in range(current_pos[0] - 1, current_pos[0] + 2):
                print("Current pos:", current_pos)
                for y in range(current_pos[0] - 1, current_pos[0] + 2):
                    if (x, y) in solid_positions:
                        # print((x, y), "Solid!")
                        pass
                    elif (x, y) in route:
                        # print((x, y), "In route!")
                        pass
                    elif y < 0 or y >= self.mapsize[0]:
                        # print((x, y), "Outside of map!")
                        pass
                    elif x < 0 or x >= self.mapsize[1]:
                        # print((x, y), "Outside of map!")
                        pass
                    elif (y, x) == current_pos:
                        # print((x, y), "Same space!")
                        pass
                    else:
                        try:
                            options[scanned_positions[(x, y)]] = (x, y)
                        except KeyError: pass
                    # print(x, y)
                    # print("({0}, {1}) == {2} : ".format(x, y, current_pos), (x, y) == current_pos)

            print("Available options", options)
            try:
                nextpos = options[min(options)]
            except ValueError:
                found_route = True
            route.append(nextpos)
            current_pos = nextpos
            print("Next pos:", nextpos)
            print("Current route:", route)
            if nextpos == startpos:
                found_route = True
            if path_update_callback is not None:
                path_update_callback(current_pos[0], current_pos[1], c)
            c += 1
        if path_complete_callback is not None:
            path_complete_callback(route[::-1])
        return route[::-1]
                

class PathFindingMap:
    def __init__(self, mp, mapsize, solid_ids = None):
        if solid_ids is None:
            self.solid_ids = [1]
        else:
            self.solid_ids = solid_ids
        self.mp = mp
        self.mpsize = mapsize

    def move(self, pos, move):
        return (pos[0] + move[0], pos[1] + move[1])

    def inMap(self, pos):
        if pos[0] >= self.mpsize[0] or pos[0] < 0:
            return False
        elif pos[1] >= self.mpsize[1] or pos[1] < 0:
            return False
        else:
            return True

    def solid(self, pos):
        return self.mp[pos[1]][pos[0]] in self.solid_ids

    def mapcells(self):
        return self.mpsize[0] * self.mpsize[1]

    def findpath(self, start, end, pos_callback = None, solid_pos_callback = None, iter_callback = None, path_update_callback = None, path_complete_callback = None):
        moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        costlookup = {start : 0}
        scanned_route = False
        solidlookup = []
        loops = 1
        scannedpos = [start]

        if pos_callback is not None:
            pos_callback(start)

        postoscanfrom = [start]
        
        while not scanned_route:
            tmp = costlookup.copy()
            scannedposold = scannedpos.copy()
            scannedpos = []
            postoscanfromtmp = []
            for pos in postoscanfrom:
                for move in moves:
                    p = self.move(pos, move)
                    if not self.inMap(p):
                        pass
                    elif self.solid(p):
                        if solid_pos_callback is not None:
                            solid_pos_callback(p)
                        solidlookup.append(p)
                    elif p in tmp.keys():
                        print("DEBUG: SCANNED ALREADY")
                    else:
                        tmp[p] = loops
                        scannedpos.append(p)
                        if pos_callback is not None:
                            pos_callback(p)
                        postoscanfromtmp.append(p)
                    if p == end:
                        scanned_route = True
            postoscanfrom = postoscanfromtmp.copy()
            costlookup = tmp.copy()
            if iter_callback is not None:
                iter_callback()
            loops += 1
            

        self.trace_route(costlookup, solidlookup, start, end, path_update_callback)

        if path_complete_callback is not None:
            path_complete_callback(self.route)
        
        return self.route

    def trace_route(self, costlookup, solidlookup, start, end, path_update_callback = None):
        moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        route_found = False

        current_pos = end

        if path_update_callback is not None:
            path_update_callback(end)

        route = [end]

        while not route_found:
            options = []
            for move in moves:
                pos = self.move(current_pos, move)
                if pos in solidlookup:
                    pass
                elif not self.inMap(pos):
                    pass
                elif pos in route:
                    pass
                elif pos not in costlookup.keys():
                    print("DEBUG: CELL NOT SCANNED")
                else:
                    options.append(pos)

            costs = []
            print(options)
            for pos in options:
                try:
                    costs.append(costlookup[pos])
                except KeyError: print("DEBUG: CELL NOT SCANNED")

            newpos = options[costs.index(min(costs))]

            if path_update_callback is not None:
                path_update_callback(newpos)

            route.append(newpos)
            current_pos = newpos
            if current_pos == start:
                route_found = True

            self.route = route.copy()[::-1]
