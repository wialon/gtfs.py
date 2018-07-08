from cStringIO import StringIO

from gtfspy.data_objects import UnknownFile
from gtfspy.transit_data_object import TransitData


def clone_transit_data(transit_data):
    """
    :rtype: TransitData
    :type transit_data: TransitData
    """

    new_transit_data = TransitData()
    for service in transit_data.calendar:
        new_transit_data.add_service_object(service, recursive=False)
    for shape in transit_data.shapes:
        new_transit_data.add_shape_object(shape)
    for stop in transit_data.stops:
        new_transit_data.add_stop_object(stop, recursive=False)
    for agency in transit_data.agencies:
        new_transit_data.add_agency_object(agency, recursive=False)
    for route in transit_data.routes:
        new_transit_data.add_route_object(route, recursive=False)
    for trip in transit_data.trips:
        new_transit_data.add_trip_object(trip, recursive=False)
        for stop_time in trip.stop_times:
            new_transit_data.add_stop_time_object(stop_time, recursive=False)
    for fare_attribute in transit_data.fare_attributes:
        new_transit_data.add_fare_attribute_object(fare_attribute, recursive=False)
    for fare_rule in transit_data.fare_rules:
        new_transit_data.add_fare_rule_object(fare_rule, recursive=False)

    for file_name, file_data in transit_data.unknown_files.iteritems():
        dome_file = StringIO()
        dome_file.write(file_data.data)
        new_transit_data.unknown_files[file_name] = UnknownFile(dome_file)
        dome_file.close()

    return new_transit_data


def create_partial_transit_data(transit_data, lines, add_unknown_files=True):
    """
    :rtype: TransitData
    :type transit_data: TransitData
    :type lines: dict[int, list[str]]
    :type add_unknown_files: bool
    """

    new_transit_data = TransitData()

    for agency_id, line_numbers in lines.iteritems():
        agency = transit_data.agencies[agency_id]
        new_transit_data.add_agency_object(agency, recursive=False)
        for line in transit_data.agencies[agency_id].lines:
            if line.line_number in line_numbers:
                for route in line.routes.itervalues():
                    new_transit_data.add_route_object(route, recursive=False)
                    for trip in route.trips:
                        new_transit_data.add_service_object(trip.service)
                        new_transit_data.add_shape_object(trip.shape)
                        new_transit_data.add_trip_object(trip)
                        for stop_time in trip.stop_times:
                            stop = stop_time.stop
                            if stop.parent_station is not None:
                                new_transit_data.add_stop_object(transit_data.stops[stop.parent_station])
                            new_transit_data.add_stop_object(stop)
                            new_transit_data.add_stop_time_object(stop_time)

    for fare_rule in transit_data.fare_rules:
        zone_ids = {stop.zone_id for stop in new_transit_data.stops}
        if (fare_rule.route is None or fare_rule.route.route_id in new_transit_data.routes) and \
                (fare_rule.origin_id is None or fare_rule.origin_id in zone_ids) and \
                (fare_rule.destination_id is None or fare_rule.destination_id in zone_ids) and \
                (fare_rule.contains_id is None or fare_rule.contains_id in zone_ids):
            new_transit_data.add_fare_rule_object(fare_rule, recursive=True)

    if add_unknown_files:
        for file_name, file_data in transit_data.unknown_files.iteritems():
            dome_file = StringIO()
            dome_file.write(file_data.data)
            new_transit_data.unknown_files[file_name] = UnknownFile(dome_file)
            dome_file.close()

    return new_transit_data
