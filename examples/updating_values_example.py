# Insertiing Values

import osisoftpy

webapi = osisoftpy.webapi('https://localhost/piwebapi', authtype='kerberos')

# <OSIsoft PI Web API [https://localhost/piwebapi]>

points = webapi.points(query='name:PythonRecordedAtTimeTest', count=100)
point = points[0]

# Insertion using default parameters
point.update_value('2017-03-15T07:00:00Z', 53)
value = point.recordedattime('2017-03-15T07:00:00Z')
print('The inserted value for {} is {} at {}'.format(point.name, value.value, value.timestamp))

# The inserted value for PythonRecordedAtTimeTest is 53.0 at 2017-03-15T07:00:00Z

# Insertion changing the updateoption parameter
point.update_value('2017-03-15T07:00:00Z', 53, updateoption = 'NoReplace')
value = point.recordedattime('2017-03-15T07:00:00Z')
print('The non-replaced value for {} is {} at {}'.format(point.name, value.value, value.timestamp))

# The non-replaced value for PythonRecordedAtTimeTest is 53.0 at 2017-03-15T07:00:00Z

# Multiple values Insertion
timestamps_to_be_inserted = ['2017-04-01T07:00:00Z', '2017-04-02T07:00:00Z', '2017-04-03T07:00:00Z']
values_to_be_inserted = [50, 95, 120]
point.update_values(timestamps_to_be_inserted, values_to_be_inserted)
values = point.interpolatedattimes(timestamps_to_be_inserted)
for value in values:
    print('The inserted value for {} is {} at {}'.format(point.name, value.value, value.timestamp))

# The inserted value for PythonRecordedAtTimeTest is 50.0 at 2017-04-01T07:00:00Z
# The inserted value for PythonRecordedAtTimeTest is 95.0 at 2017-04-02T07:00:00Z
# The inserted value for PythonRecordedAtTimeTest is 120.0 at 2017-04-03T07:00:00Z

# Multiple values Insertion with mismatched array
try:
    timestamps_to_be_inserted = ['2017-04-01T07:00:00Z', '2017-04-02T07:00:00Z', '2017-04-03T07:00:00Z', '2017-04-04T07:00:00Z']
    values_to_be_inserted = [50, 95, 120]
    point.update_values(timestamps_to_be_inserted, values_to_be_inserted)
except Exception as inst:
    print('{}: {}'.format(type(inst), inst))

# <class 'osisoftpy.exceptions.MismatchEntriesError'>: The length of timestamps and values lists are not equal.

