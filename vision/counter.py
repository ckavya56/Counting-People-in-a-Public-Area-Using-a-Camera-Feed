class PeopleCounter:
    def __init__(self, offset=15):
        self.offset = offset
        self.line_y = None

        # Remember which side of the line each person was on
        self.previous_side = {}

        self.total_in = 0
        self.total_out = 0

    def update(self, people, frame_height):
        self.line_y = frame_height // 2

        events = []

        for person in people:
            person_id = person["id"]

            x1, y1, x2, y2 = person["bbox"]

            # Find the center of the person
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            # Determine which side of the line the person is on
            if cy < self.line_y - self.offset:
                current_side = "above"

            elif cy > self.line_y + self.offset:
                current_side = "below"

            else:
                current_side = "middle"

            # Get where this person was previously
            previous_side = self.previous_side.get(person_id)

            # Save current side for the next frame
            if current_side != "middle":
                self.previous_side[person_id] = current_side

            # We need a previous position to detect a crossing
            if previous_side is None:
                continue

            # ABOVE → BELOW = ENTER
            if previous_side == "above" and current_side == "below":
                self.total_in += 1

                events.append({
                    "id": person_id,
                    "direction": "IN",
                    "centroid": (cx, cy)
                })

            # BELOW → ABOVE = EXIT
            elif previous_side == "below" and current_side == "above":
                self.total_out += 1

                events.append({
                    "id": person_id,
                    "direction": "OUT",
                    "centroid": (cx, cy)
                })

        return events