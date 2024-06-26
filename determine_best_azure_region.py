# Terms:
#  Azure Region: A place where Dynamics 365 can be hosted.
#  Latency: the time it takes for a network packet to travel between two places, i.e. a location to Azure Region.
#  Location: A place where workers work and need to access Dynamics 365
#  Workers: employees, contractors, or temporary employees working at a location

from ortools.sat.python import cp_model
import csv

# Define the model.
model = cp_model.CpModel()

##################################################################################
# Define Variables
##################################################################################

# The latency for each location MUST be less than ABSOLUTE_ACCEPTABLE_LATENCY milliseconds for all workers.
ABSOLUTE_ACCEPTABLE_LATENCY = 450
OUTPUT_CSV_NAME = 'latencies_to_suggestion.csv'

# These are the possible Azure Regions that Dynamics 365 can be deployed to.
azure_regions = [
    'Canada Central', 'France Central', 'Germany West Central', 'UK South', 'UK West',
    'North Europe', 'Italy North', 'Switzerland North', 'West Europe', 'East US', 'East US 2',
    'North Central US', 'South Central US', 'Norway East', 'Poland Central', 'Sweden Central',
    'Central US', 'West US 3', 'Canada East', 'UAE North', 'West US', 'West Central US',
    'Israel Central', 'Qatar Central', 'West US 2', 'South India', 'Central India',
    'Southeast Asia', 'West India', 'Japan West', 'Korea South', 'Korea Central',
    'Japan East', 'Brazil South', 'South Africa North', 'Australia Southeast',
    'Australia East', 'East Asia', 'Australia Central'
]
# The decision variables are 0-1 variables for each possible location.
azure_region_options = {location: model.NewBoolVar(location) for location in locations}

# Define the data.
workers = {
    'Location A': 92,
    'Location B': 72,
    'Location C': 61,
    'Location D': 62,
    'Location E': 93,
    'Location F': 81,
    'Location G': 73,
    'Location H': 67,
    'Location I': 142,
    'Location J': 142,
    'Location K': 103,
    'Location L': 76,
    'Location M': 121,
    'Location N': 89,
    'Location O': 142
}

latencies = {
    'Location A': {'France Central': 211, 'Germany West Central': 150, 'UK South': 362, 'UK West': 69, 'Italy North': 139, 'North Europe': 265, 'Switzerland North': 394, 'West Europe': 393, 'Central US': 383, 'East US 2': 377, 'East US': 111, 'Norway East': 247, 'Poland Central': 323, 'West Central US': 208, 'North Central US': 232, 'South Central US': 81, 'Central India': 280, 'Sweden Central': 307, 'Canada Central': 205, 'West US 2': 194, 'Japan East': 333, 'South India': 110, 'Southeast Asia': 168, 'West India': 319, 'West US 3': 276, 'West US': 234, 'Canada East': 102, 'Israel Central': 402, 'Qatar Central': 100, 'East Asia': 393, 'UAE North': 220, 'Japan West': 109, 'Korea South': 315, 'Korea Central': 206, 'Australia Central': 360, 'Australia East': 277, 'Australia Southeast': 154, 'Brazil South': 355, 'South Africa North': 179},
    'Location B': {'France Central': 215, 'Germany West Central': 273, 'UK South': 158, 'UK West': 132, 'Italy North': 273, 'North Europe': 232, 'Switzerland North': 370, 'West Europe': 189, 'Central US': 118, 'East US 2': 284, 'East US': 230, 'Norway East': 112, 'Poland Central': 208, 'West Central US': 347, 'North Central US': 220, 'South Central US': 338, 'Central India': 368, 'Sweden Central': 168, 'Canada Central': 200, 'West US 2': 228, 'Japan East': 185, 'South India': 330, 'Southeast Asia': 393, 'West India': 288, 'West US 3': 159, 'West US': 83, 'Canada East': 337, 'Israel Central': 267, 'Qatar Central': 299, 'East Asia': 356, 'UAE North': 326, 'Japan West': 149, 'Korea South': 175, 'Korea Central': 237, 'Australia Central': 80, 'Australia East': 60, 'Australia Southeast': 400, 'Brazil South': 181, 'South Africa North': 183},
    'Location C': {'France Central': 296, 'Germany West Central': 402, 'UK South': 171, 'UK West': 197, 'Italy North': 128, 'North Europe': 316, 'Switzerland North': 114, 'West Europe': 161, 'Central US': 117, 'East US 2': 78, 'East US': 96, 'Norway East': 175, 'Poland Central': 74, 'West Central US': 216, 'North Central US': 237, 'South Central US': 205, 'Central India': 237, 'Sweden Central': 392, 'Canada Central': 217, 'West US 2': 98, 'Japan East': 333, 'South India': 188, 'Southeast Asia': 374, 'West India': 155, 'West US 3': 349, 'West US': 354, 'Canada East': 134, 'Israel Central': 83, 'Qatar Central': 210, 'East Asia': 85, 'UAE North': 278, 'Japan West': 348, 'Korea South': 220, 'Korea Central': 348, 'Australia Central': 161, 'Australia East': 264, 'Australia Southeast': 341, 'Brazil South': 224, 'South Africa North': 294},
    'Location D': {'France Central': 392, 'Germany West Central': 132, 'UK South': 145, 'UK West': 274, 'Italy North': 57, 'North Europe': 362, 'Switzerland North': 204, 'West Europe': 270, 'Central US': 161, 'East US 2': 390, 'East US': 333, 'Norway East': 308, 'Poland Central': 360, 'West Central US': 89, 'North Central US': 126, 'South Central US': 108, 'Central India': 400, 'Sweden Central': 357, 'Canada Central': 82, 'West US 2': 397, 'Japan East': 373, 'South India': 158, 'Southeast Asia': 55, 'West India': 183, 'West US 3': 236, 'West US': 346, 'Canada East': 254, 'Israel Central': 255, 'Qatar Central': 179, 'East Asia': 187, 'UAE North': 89, 'Japan West': 78, 'Korea South': 261, 'Korea Central': 304, 'Australia Central': 83, 'Australia East': 121, 'Australia Southeast': 395, 'Brazil South': 274, 'South Africa North': 312},
    'Location E': {'France Central': 402, 'Germany West Central': 305, 'UK South': 159, 'UK West': 197, 'Italy North': 83, 'North Europe': 236, 'Switzerland North': 171, 'West Europe': 179, 'Central US': 354, 'East US 2': 327, 'East US': 383, 'Norway East': 181, 'Poland Central': 344, 'West Central US': 105, 'North Central US': 128, 'South Central US': 133, 'Central India': 147, 'Sweden Central': 232, 'Canada Central': 86, 'West US 2': 252, 'Japan East': 322, 'South India': 355, 'Southeast Asia': 314, 'West India': 286, 'West US 3': 202, 'West US': 301, 'Canada East': 95, 'Israel Central': 173, 'Qatar Central': 336, 'East Asia': 257, 'UAE North': 195, 'Japan West': 196, 'Korea South': 285, 'Korea Central': 257, 'Australia Central': 110, 'Australia East': 166, 'Australia Southeast': 368, 'Brazil South': 238, 'South Africa North': 370},
    'Location F': {'France Central': 319, 'Germany West Central': 328, 'UK South': 90, 'UK West': 391, 'Italy North': 340, 'North Europe': 271, 'Switzerland North': 322, 'West Europe': 315, 'Central US': 263, 'East US 2': 90, 'East US': 219, 'Norway East': 112, 'Poland Central': 136, 'West Central US': 271, 'North Central US': 374, 'South Central US': 181, 'Central India': 196, 'Sweden Central': 282, 'Canada Central': 283, 'West US 2': 178, 'Japan East': 246, 'South India': 327, 'Southeast Asia': 162, 'West India': 383, 'West US 3': 338, 'West US': 382, 'Canada East': 77, 'Israel Central': 256, 'Qatar Central': 313, 'East Asia': 211, 'UAE North': 77, 'Japan West': 225, 'Korea South': 391, 'Korea Central': 263, 'Australia Central': 305, 'Australia East': 253, 'Australia Southeast': 327, 'Brazil South': 265, 'South Africa North': 314},
    'Location G': {'France Central': 74, 'Germany West Central': 385, 'UK South': 314, 'UK West': 299, 'Italy North': 171, 'North Europe': 244, 'Switzerland North': 398, 'West Europe': 357, 'Central US': 111, 'East US 2': 312, 'East US': 352, 'Norway East': 315, 'Poland Central': 100, 'West Central US': 244, 'North Central US': 261, 'South Central US': 230, 'Central India': 62, 'Sweden Central': 198, 'Canada Central': 344, 'West US 2': 301, 'Japan East': 312, 'South India': 381, 'Southeast Asia': 103, 'West India': 56, 'West US 3': 211, 'West US': 254, 'Canada East': 263, 'Israel Central': 226, 'Qatar Central': 374, 'East Asia': 287, 'UAE North': 108, 'Japan West': 167, 'Korea South': 347, 'Korea Central': 122, 'Australia Central': 285, 'Australia East': 206, 'Australia Southeast': 186, 'Brazil South': 363, 'South Africa North': 221},
    'Location H': {'France Central': 325, 'Germany West Central': 402, 'UK South': 273, 'UK West': 250, 'Italy North': 88, 'North Europe': 82, 'Switzerland North': 292, 'West Europe': 389, 'Central US': 188, 'East US 2': 67, 'East US': 338, 'Norway East': 246, 'Poland Central': 59, 'West Central US': 311, 'North Central US': 185, 'South Central US': 212, 'Central India': 270, 'Sweden Central': 165, 'Canada Central': 151, 'West US 2': 54, 'Japan East': 348, 'South India': 116, 'Southeast Asia': 97, 'West India': 242, 'West US 3': 189, 'West US': 360, 'Canada East': 358, 'Israel Central': 403, 'Qatar Central': 367, 'East Asia': 223, 'UAE North': 193, 'Japan West': 209, 'Korea South': 361, 'Korea Central': 279, 'Australia Central': 166, 'Australia East': 273, 'Australia Southeast': 375, 'Brazil South': 206, 'South Africa North': 350},
    'Location I': {'France Central': 222, 'Germany West Central': 310, 'UK South': 128, 'UK West': 280, 'Italy North': 321, 'North Europe': 84, 'Switzerland North': 292, 'West Europe': 349, 'Central US': 67, 'East US 2': 317, 'East US': 171, 'Norway East': 93, 'Poland Central': 251, 'West Central US': 79, 'North Central US': 188, 'South Central US': 165, 'Central India': 213, 'Sweden Central': 69, 'Canada Central': 393, 'West US 2': 320, 'Japan East': 150, 'South India': 76, 'Southeast Asia': 401, 'West India': 232, 'West US 3': 161, 'West US': 349, 'Canada East': 179, 'Israel Central': 102, 'Qatar Central': 280, 'East Asia': 89, 'UAE North': 371, 'Japan West': 180, 'Korea South': 321, 'Korea Central': 140, 'Australia Central': 137, 'Australia East': 186, 'Australia Southeast': 268, 'Brazil South': 86, 'South Africa North': 156},
    'Location J': {'France Central': 286, 'Germany West Central': 179, 'UK South': 77, 'UK West': 310, 'Italy North': 186, 'North Europe': 374, 'Switzerland North': 131, 'West Europe': 197, 'Central US': 368, 'East US 2': 323, 'East US': 354, 'Norway East': 324, 'Poland Central': 109, 'West Central US': 332, 'North Central US': 248, 'South Central US': 228, 'Central India': 154, 'Sweden Central': 106, 'Canada Central': 60, 'West US 2': 335, 'Japan East': 286, 'South India': 163, 'Southeast Asia': 92, 'West India': 252, 'West US 3': 358, 'West US': 376, 'Canada East': 269, 'Israel Central': 148, 'Qatar Central': 196, 'East Asia': 208, 'UAE North': 368, 'Japan West': 75, 'Korea South': 208, 'Korea Central': 191, 'Australia Central': 58, 'Australia East': 65, 'Australia Southeast': 164, 'Brazil South': 361, 'South Africa North': 292},
    'Location K': {'France Central': 112, 'Germany West Central': 212, 'UK South': 221, 'UK West': 257, 'Italy North': 369, 'North Europe': 177, 'Switzerland North': 112, 'West Europe': 390, 'Central US': 390, 'East US 2': 130, 'East US': 340, 'Norway East': 226, 'Poland Central': 342, 'West Central US': 264, 'North Central US': 288, 'South Central US': 401, 'Central India': 308, 'Sweden Central': 374, 'Canada Central': 365, 'West US 2': 240, 'Japan East': 187, 'South India': 323, 'Southeast Asia': 314, 'West India': 90, 'West US 3': 257, 'West US': 188, 'Canada East': 97, 'Israel Central': 157, 'Qatar Central': 53, 'East Asia': 292, 'UAE North': 286, 'Japan West': 104, 'Korea South': 104, 'Korea Central': 304, 'Australia Central': 363, 'Australia East': 189, 'Australia Southeast': 308, 'Brazil South': 247, 'South Africa North': 67},
    'Location L': {'France Central': 67, 'Germany West Central': 397, 'UK South': 370, 'UK West': 212, 'Italy North': 219, 'North Europe': 302, 'Switzerland North': 210, 'West Europe': 168, 'Central US': 314, 'East US 2': 89, 'East US': 107, 'Norway East': 121, 'Poland Central': 313, 'West Central US': 144, 'North Central US': 149, 'South Central US': 132, 'Central India': 269, 'Sweden Central': 246, 'Canada Central': 90, 'West US 2': 303, 'Japan East': 349, 'South India': 298, 'Southeast Asia': 295, 'West India': 165, 'West US 3': 148, 'West US': 354, 'Canada East': 204, 'Israel Central': 290, 'Qatar Central': 357, 'East Asia': 93, 'UAE North': 115, 'Japan West': 225, 'Korea South': 230, 'Korea Central': 294, 'Australia Central': 130, 'Australia East': 183, 'Australia Southeast': 349, 'Brazil South': 361, 'South Africa North': 172},
    'Location M': {'France Central': 240, 'Germany West Central': 259, 'UK South': 315, 'UK West': 169, 'Italy North': 105, 'North Europe': 93, 'Switzerland North': 356, 'West Europe': 156, 'Central US': 227, 'East US 2': 308, 'East US': 370, 'Norway East': 174, 'Poland Central': 106, 'West Central US': 216, 'North Central US': 381, 'South Central US': 117, 'Central India': 155, 'Sweden Central': 363, 'Canada Central': 377, 'West US 2': 107, 'Japan East': 53, 'South India': 258, 'Southeast Asia': 336, 'West India': 285, 'West US 3': 171, 'West US': 144, 'Canada East': 176, 'Israel Central': 286, 'Qatar Central': 85, 'East Asia': 135, 'UAE North': 126, 'Japan West': 375, 'Korea South': 109, 'Korea Central': 390, 'Australia Central': 390, 'Australia East': 129, 'Australia Southeast': 293, 'Brazil South': 71, 'South Africa North': 90},
    'Location N': {'France Central': 73, 'Germany West Central': 267, 'UK South': 54, 'UK West': 357, 'Italy North': 253, 'North Europe': 58, 'Switzerland North': 362, 'West Europe': 237, 'Central US': 281, 'East US 2': 107, 'East US': 111, 'Norway East': 86, 'Poland Central': 359, 'West Central US': 73, 'North Central US': 215, 'South Central US': 137, 'Central India': 357, 'Sweden Central': 333, 'Canada Central': 262, 'West US 2': 331, 'Japan East': 254, 'South India': 363, 'Southeast Asia': 86, 'West India': 158, 'West US 3': 100, 'West US': 126, 'Canada East': 391, 'Israel Central': 329, 'Qatar Central': 146, 'East Asia': 60, 'UAE North': 78, 'Japan West': 369, 'Korea South': 187, 'Korea Central': 231, 'Australia Central': 62, 'Australia East': 351, 'Australia Southeast': 217, 'Brazil South': 378, 'South Africa North': 380},
    'Location O': {'France Central': 181, 'Germany West Central': 129, 'UK South': 281, 'UK West': 136, 'Italy North': 252, 'North Europe': 397, 'Switzerland North': 207, 'West Europe': 315, 'Central US': 174, 'East US 2': 216, 'East US': 74, 'Norway East': 77, 'Poland Central': 354, 'West Central US': 205, 'North Central US': 345, 'South Central US': 360, 'Central India': 88, 'Sweden Central': 143, 'Canada Central': 295, 'West US 2': 198, 'Japan East': 179, 'South India': 362, 'Southeast Asia': 172, 'West India': 385, 'West US 3': 304, 'West US': 73, 'Canada East': 107, 'Israel Central': 239, 'Qatar Central': 264, 'East Asia': 254, 'UAE North': 291, 'Japan West': 103, 'Korea South': 146, 'Korea Central': 283, 'Australia Central': 181, 'Australia East': 237, 'Australia Southeast': 298, 'Brazil South': 223, 'South Africa North': 323}
}

##################################################################################
# Data Validation
##################################################################################

# Check if each region has at least one location with a latency less than 130
for region, region_latencies in latencies.items():
    if all(latency >= 130 for latency in region_latencies.values()):
        print(f"No location with latency less than 130 for region: {region}.  Recommend increasing internet connection.")

#########################################
# Constraints
#########################################
# The sum of the azure_region_options must be 1, meaning only one location can be chosen.
model.Add(sum(azure_region_options.values()) == 2)

# The latency for each location must be less than ABSOLUTE_ACCEPTABLE_LATENCY for all workers, or return that there is no solution.
# Likely the person needs to enable more (2+) production locations instead of one to fulfil the requirements.
# Personally, I'd like to keep it to less than 300ms.
for worker_location, worker_count in workers.items():
    for location, location_var in azure_region_options.items():
        model.Add(latencies[worker_location][location] * location_var <= ABSOLUTE_ACCEPTABLE_LATENCY)

#########################################
# Objective Function
#########################################
# The objective is to minimize the total latency for all workers.
total_latency = sum(latencies[worker_location][location] * worker_count * location_var
                    for worker_location, worker_count in workers.items()
                    for location, location_var in azure_region_options.items())
model.Minimize(total_latency)

#########################################
# Solve the Model
#########################################
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Print the solution.
print()
if status == cp_model.OPTIMAL:
    #print('Minimum total latency:', solver.ObjectiveValue())
    #print()
    print('Location:')
    for region_name, region_var in azure_region_options.items():
        if solver.Value(region_var) == 1:
            print("  " + region_name)
else:
    print('No solution found.')
    exit(1)

##################################################################################
# Export data based on assumption above
##################################################################################

print()
print('Answer results in the following latencies')
# Export data to CSV
with open(OUTPUT_CSV_NAME, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['Location', 'Number of Workers', 'Latency', 'Hosting Location'])
    writer.writeheader()
    for region_name, region_var in azure_region_options.items():
        if solver.Value(region_var) == 1:
            for location, location_latency in latencies.items():
                #print(location, location_latency)
                worker_count = workers[location]
                print("{} workers in {} with latency of {}ms to {}".format(worker_count, location, location_latency[region_name], region_name))
                writer.writerow({'Location': location, 'Number of Workers': worker_count, 'Latency': location_latency[region_name], 'Hosting Location': region_name})

print()
print("Saved latencies to {} for reporting.".format(OUTPUT_CSV_NAME))
