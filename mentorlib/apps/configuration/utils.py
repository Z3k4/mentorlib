def get_resource_name(resource):
    number = f"0{resource.number}" if resource.number <= 9 else resource.number
    return f"R{resource.semester.semester}.{number}"