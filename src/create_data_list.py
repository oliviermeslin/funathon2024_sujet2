def create_data_list(source_file):
    with open(source_file, "r") as my_file:
        sources = yaml.safe_load(my_file)
    return(sources)