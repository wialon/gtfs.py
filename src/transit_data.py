import csv
from zipfile import ZipFile

from data_objects import *
from utils.lines_factory import LinesFactory


class TransitData:
    def __init__(self, file_path):
        with open(file_path, "rb") as gtfs_file:
            zip_file = ZipFile(gtfs_file)

            with zip_file.open("agency.txt", "r") as agency_file:
                reader = csv.DictReader(agency_file)
                self.agencies = {agency.agency_id: agency for agency in (Agency(**row) for row in reader)}

            self._lines_factory = LinesFactory()
            with zip_file.open("routes.txt", "r") as routes_file:
                reader = csv.DictReader(routes_file)
                self.routes = {route.route_id: route for route in
                               (Route(transit_data=self, **row) for row in reader)}
            for agency_id, agency_lines in self._lines_factory.lines.iteritems():
                self.agencies[agency_id].lines = agency_lines

            with zip_file.open("shapes.txt", "r") as shapes_file:
                reader = csv.DictReader(shapes_file)
                self.shapes = {shape.shape_id: shape for shape in
                               (Shape(**row) for row in reader)}

            with zip_file.open("calendar.txt", "r") as calendar_file:
                reader = csv.DictReader(calendar_file)
                self.calendar = {service.service_id: service for service in
                                 (Service(**row) for row in reader)}

            with zip_file.open("trips.txt", "r") as trips_file:
                reader = csv.DictReader(trips_file)
                self.trips = {trip.trip_id: trip for trip in
                              (Trip(transit_data=self, **row) for row in reader)}
            for trip in self.trips.itervalues():
                trip.route.trips.append(trip)

            with zip_file.open("stops.txt", "r") as stops_file:
                reader = csv.DictReader(stops_file)
                self.stops = {stop.stop_id: stop for stop in
                              (Stop(transit_data=self, **row) for row in reader)}

            with zip_file.open("stop_times.txt", "r") as stop_times_file:
                reader = csv.DictReader(stop_times_file)
                for row in reader:
                    stop_time = StopTime(transit_data=self, **row)
                    stop_time.trip.stop_times.append(stop_time)
                    stop_time.stop.stop_times.append(stop_time)
