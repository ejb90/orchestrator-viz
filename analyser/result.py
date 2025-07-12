"""Result class."""

import datetime
import pathlib
import uuid


class Result:
    def __init__(self):
        self.id = uuid.uuid4()
        self.version = "0.0.0"
        self.name = None
        self.model = None
        self.path = pathlib.Path()
        self.datetime = datetime.datetime.now()

        self.storage = 0.0
        self.runtime = 0.0
        self.cpuhours = 0.0
        self.memory_total_hwm = 0.0
        self.memory_max_node_hwm = 0.0
        self.memory_mean_node_hwm = 0.0
        self.memory_min_node_hwm = 0.0
        
        self.equilibriation_time = None
        self.equilibriation_temperature = None
        self.internal_energy = None
        self.total_ie = None
        self.total_er = None
        self.energy_conservation = None

        self.step = None


def make_collection_of_runs():
    """Dummy collection of runs."""
    import random 
    import viz.steps

    results = []
    for version in ("1.0.0", "2.0.0", "3.0.0", "4.0.0"):
        for model in ("model_a", "model_b", "model_c", "model_d", "model_e", "model_f", "model_g"):
            for step in ("mesh", "input", "simulate", "analyse"):
                
                if step in ("mesh", "analyse"):
                    runtime = random.randint(60, 300)
                    cpuhours = runtime / 60.0 / 60.0
                elif step == "input":
                    runtime = random.randint(20, 120)
                    cpuhours = runtime / 60.0 / 60.0
                elif step == "mesh":
                    runtime = random.randint(60*60*1, 60*60*8)
                    cpuhours = runtime / 60.0 / 60.0 * 128
                

                for i in range(1, random.randint(1, 4)):
                    result = Result()
                    result.version=version
                    result.name=step
                    result.model=model
                    result.path=pathlib.Path() / str(i) / version / model / step

                    result.storage = random.randint(1000, 10000)
                    result.runtime = runtime
                    result.cpuhours = cpuhours
                    result.memory_total_hwm = 0.0
                    result.memory_max_node_hwm = 0.0
                    result.memory_mean_node_hwm = 0.0
                    result.memory_min_node_hwm = 0.0
                    
                    result.equilibriation_time =  random.uniform(0.0, 0.2)
                    result.equilibriation_temperature =  random.uniform(3.0, 7.0)
                    result.internal_energy =  random.uniform(100, 4000)

                    result.total_ie = 0.0
                    result.total_er = 0.0
                    result.energy_conservation = random.uniform(0.0, 0.001)
                    result.step = viz.steps.Step(step, "success")
                    results.append(result)

    return results


def main():
    """"""
    import database as database

    results = make_collection_of_runs()
    database.setup_database()
    for result in results:
        database.add_result(result=result)


if __name__ == "__main__":
    main()