class GeochemResultSet:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def print_results(self) -> None:
        for item in self.__dict__.values():
            print(f"{item['label']} = {item['value']}")

    def update(self, **kwargs):
        self.__dict__.update(kwargs)

class GeochemTable:
    def __init__(self, results: list[GeochemResultSet]) -> None:
        with open("Templates/geochem_table.html") as file:
            self.template_body = file.read()
        with open("Templates/geochem_table_row.html") as file:
            self.template_row = file.read()
        self.results = results

    def generate_html(self) -> None:
        results = []
        for sample_universe in self.results:
            for result_set in sample_universe.items():
                key = result_set[0]
                value = result_set[1]
                results.append({key: value.__dict__})
        if (self.template_body and self.template_row and results): 
            table, rows = "" + self.template_body, ""
            for element_results in results:
                for result_set in element_results.items():
                    result_set[1]["sample_universe"] = {
                        "value": result_set[0], "label": "Sample Universe" 
                    }                        
                    new_row = "" + self.template_row
                    for tag in result_set[1].keys():
                        value = str(result_set[1][tag]["value"])
                        if(value is not None):
                            tag_full = f"#{tag}"
                            new_row = new_row.replace(tag_full, value)
                    rows += new_row + "\n"
            table = table.replace("#rows", rows)
            with open(f"Output/geochem_results_table_{result_set[1]['dataset']['value']}.html", mode="w") as file:
                file.write(table)
